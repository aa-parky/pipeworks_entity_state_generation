"""Unit tests for the FastAPI entity state service.

These tests validate that the HTTP API layer:
- exposes expected endpoints
- enforces request schema constraints
- returns deterministic output for seeded requests
- produces stable batch semantics
"""

from __future__ import annotations

import importlib.util
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

# Skip cleanly when API-specific dependencies are not installed in the active
# environment (for example, minimal library-only installs).
pytest.importorskip("fastapi")
pytest.importorskip("httpx")
testclient_mod = pytest.importorskip("fastapi.testclient")
TestClient = testclient_mod.TestClient


@pytest.fixture
def entity_api_module() -> Any:
    """Import the API module under test.

    Keeping import inside a fixture makes it explicit that tests target the
    repository-local ``entity_api.py`` module.
    """

    # Load the module by absolute file path so tests do not depend on how
    # `PYTHONPATH` is configured by the calling environment.
    module_path = Path(__file__).resolve().parent.parent / "entity_api.py"
    spec = importlib.util.spec_from_file_location("entity_api_under_test", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def api_client(entity_api_module: Any) -> Iterator[TestClient]:
    """Provide a FastAPI test client for endpoint tests."""

    with TestClient(entity_api_module.app) as client:
        yield client


def test_health_endpoint_returns_expected_payload(api_client: TestClient) -> None:
    """`GET /api/health` should confirm service liveness."""

    response = api_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pipeworks-entity-state-api"}


def test_axes_endpoint_returns_character_and_occupation(api_client: TestClient) -> None:
    """`GET /api/axes` should return current axis definitions from library helpers."""

    response = api_client.get("/api/axes")

    assert response.status_code == 200
    payload = response.json()

    assert "character" in payload
    assert "occupation" in payload
    assert "axes" in payload["character"]
    assert "values" in payload["character"]
    assert "axes" in payload["occupation"]
    assert "values" in payload["occupation"]

    # Spot-check well-known axes to ensure response shape is meaningful.
    assert "physique" in payload["character"]["axes"]
    assert "wealth" in payload["character"]["axes"]
    assert "legitimacy" in payload["occupation"]["axes"]
    assert "visibility" in payload["occupation"]["axes"]


def test_generate_entity_seeded_is_reproducible(api_client: TestClient) -> None:
    """Seeded POST requests should generate identical payloads."""

    request_payload = {"seed": 42, "include_prompts": True}

    response_a = api_client.post("/api/entity", json=request_payload)
    response_b = api_client.post("/api/entity", json=request_payload)

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert response_a.json() == response_b.json()

    entity = response_a.json()
    assert entity["seed"] == 42
    assert "character" in entity
    assert "occupation" in entity
    assert "prompts" in entity
    assert "full" in entity["prompts"]


def test_generate_entity_without_prompts_omits_prompt_block(api_client: TestClient) -> None:
    """Setting include_prompts=false should remove prompt fields from response."""

    response = api_client.post(
        "/api/entity",
        json={
            "seed": 7,
            "include_prompts": False,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["seed"] == 7
    assert "character" in payload
    assert "occupation" in payload
    assert "prompts" not in payload


def test_generate_entity_includes_generator_metadata(
    api_client: TestClient,
    entity_api_module: Any,
) -> None:
    """`POST /api/entity` should include adapter-facing generator metadata."""

    response = api_client.post("/api/entity", json={"seed": 42, "include_prompts": False})

    assert response.status_code == 200
    payload = response.json()
    assert payload["generator_version"] == entity_api_module.GENERATOR_VERSION
    assert payload["generator_capabilities"] == entity_api_module.GENERATOR_CAPABILITIES
    assert all(isinstance(capability, str) for capability in payload["generator_capabilities"])


def test_generate_entity_without_seed_returns_integer_seed(api_client: TestClient) -> None:
    """Unseeded generation should still return a concrete replayable seed."""

    response = api_client.post("/api/entity", json={"include_prompts": False})

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["seed"], int)
    assert payload["seed"] >= 0


def test_generate_entity_rejects_unknown_fields(api_client: TestClient) -> None:
    """Request models should reject extra fields (extra='forbid')."""

    response = api_client.post(
        "/api/entity",
        json={"seed": 1, "include_prompts": True, "unknown_field": "not-allowed"},
    )

    assert response.status_code == 422


def test_batch_endpoint_uses_sequential_seeds(api_client: TestClient) -> None:
    """Batch endpoint should use start_seed + index sequencing."""

    response = api_client.post(
        "/api/entities/batch",
        json={"start_seed": 100, "count": 3, "include_prompts": False},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["start_seed"] == 100
    assert payload["count"] == 3
    assert len(payload["entities"]) == 3

    seeds = [entity["seed"] for entity in payload["entities"]]
    assert seeds == [100, 101, 102]

    for entity in payload["entities"]:
        assert "character" in entity
        assert "occupation" in entity
        assert "prompts" not in entity


def test_batch_endpoint_rejects_out_of_range_count(api_client: TestClient) -> None:
    """Batch `count` validation should enforce lower/upper bounds."""

    response_too_small = api_client.post("/api/entities/batch", json={"count": 0})
    response_too_large = api_client.post("/api/entities/batch", json={"count": 501})

    assert response_too_small.status_code == 422
    assert response_too_large.status_code == 422
