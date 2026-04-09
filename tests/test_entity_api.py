"""Unit tests for the FastAPI entity state service.

These tests validate that the HTTP API layer:
- exposes expected endpoints
- enforces request schema constraints
- returns deterministic output for seeded requests
- produces stable batch semantics
"""

from __future__ import annotations

import importlib.util
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

import httpx
import pytest

# Skip cleanly when API-specific dependencies are not installed in the active
# environment (for example, minimal library-only installs).
pytest.importorskip("fastapi")
pytest.importorskip("httpx")

pytestmark = pytest.mark.anyio


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
async def api_client(entity_api_module: Any) -> AsyncIterator[httpx.AsyncClient]:
    """Provide an async ASGI-backed client for endpoint tests."""

    transport = httpx.ASGITransport(app=entity_api_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


async def test_health_endpoint_returns_expected_payload(api_client: httpx.AsyncClient) -> None:
    """`GET /api/health` should confirm service liveness."""

    response = await api_client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "pipeworks-entity-state-api"}


async def test_axes_endpoint_returns_character_and_occupation(
    api_client: httpx.AsyncClient,
) -> None:
    """`GET /api/axes` should return current axis definitions from library helpers."""

    response = await api_client.get("/api/axes")

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


async def test_generate_entity_seeded_is_reproducible(api_client: httpx.AsyncClient) -> None:
    """Seeded POST requests should generate identical payloads."""

    request_payload = {"seed": 42, "include_prompts": True}

    response_a = await api_client.post("/api/entity", json=request_payload)
    response_b = await api_client.post("/api/entity", json=request_payload)

    assert response_a.status_code == 200
    assert response_b.status_code == 200
    assert response_a.json() == response_b.json()

    entity = response_a.json()
    assert entity["seed"] == 42
    assert entity["axis_profile"] == "character_full"
    assert "character" in entity
    assert "occupation" in entity
    assert "axes" in entity
    assert "prompts" in entity
    assert "full" in entity["prompts"]


async def test_generate_entity_without_prompts_omits_prompt_block(
    api_client: httpx.AsyncClient,
) -> None:
    """Setting include_prompts=false should remove prompt fields from response."""

    response = await api_client.post(
        "/api/entity",
        json={
            "seed": 7,
            "include_prompts": False,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["seed"] == 7
    assert payload["axis_profile"] == "character_full"
    assert "character" in payload
    assert "occupation" in payload
    assert "axes" in payload
    assert "prompts" not in payload


async def test_generate_entity_includes_generator_metadata(
    api_client: httpx.AsyncClient,
    entity_api_module: Any,
) -> None:
    """`POST /api/entity` should include adapter-facing generator metadata."""

    response = await api_client.post("/api/entity", json={"seed": 42, "include_prompts": False})

    assert response.status_code == 200
    payload = response.json()
    assert payload["generator_version"] == entity_api_module.GENERATOR_VERSION
    assert payload["generator_capabilities"] == entity_api_module.GENERATOR_CAPABILITIES
    assert all(isinstance(capability, str) for capability in payload["generator_capabilities"])


async def test_generate_entity_includes_numeric_axes_with_labels(
    api_client: httpx.AsyncClient,
) -> None:
    """`POST /api/entity` should include normalized numeric axis scores."""

    response = await api_client.post("/api/entity", json={"seed": 42, "include_prompts": False})

    assert response.status_code == 200
    payload = response.json()
    axes = payload["axes"]

    assert isinstance(axes, dict)
    assert axes

    for axis_name, axis_payload in axes.items():
        assert isinstance(axis_name, str)
        assert isinstance(axis_payload, dict)
        assert isinstance(axis_payload["label"], str)
        assert isinstance(axis_payload["score"], (int, float))
        assert 0.0 <= float(axis_payload["score"]) <= 1.0

    # Spot-check representative character + occupation axes.
    assert "physique" in axes
    assert "wealth" in axes
    assert "legitimacy" in axes
    assert "visibility" in axes


async def test_generate_entity_defaults_to_full_axis_profile(
    api_client: httpx.AsyncClient,
) -> None:
    """Default profile should emit the full character+occupation axis set."""

    axes_response = await api_client.get("/api/axes")
    assert axes_response.status_code == 200
    axes_payload = axes_response.json()
    expected_character_axes = set(axes_payload["character"]["axes"])
    expected_occupation_axes = set(axes_payload["occupation"]["axes"])
    expected_all_axes = expected_character_axes | expected_occupation_axes

    for seed in (1, 7, 42, 4242, 99999):
        response = await api_client.post(
            "/api/entity",
            json={"seed": seed, "include_prompts": False},
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["axis_profile"] == "character_full"
        assert set(payload["character"].keys()) == expected_character_axes
        assert set(payload["occupation"].keys()) == expected_occupation_axes
        assert set(payload["axes"].keys()) == expected_all_axes


async def test_generate_entity_subset_legacy_profile_preserves_sparse_behavior(
    api_client: httpx.AsyncClient,
) -> None:
    """Legacy profile should preserve sparse optional-axis generation behavior."""

    axes_response = await api_client.get("/api/axes")
    assert axes_response.status_code == 200
    axes_payload = axes_response.json()
    expected_all_axes = set(axes_payload["character"]["axes"]) | set(
        axes_payload["occupation"]["axes"]
    )

    response = await api_client.post(
        "/api/entity",
        json={
            "seed": 42,
            "include_prompts": False,
            "axis_profile": "subset_legacy",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["axis_profile"] == "subset_legacy"
    assert set(payload["axes"].keys()) < expected_all_axes
    assert set(payload["character"].keys()) < set(axes_payload["character"]["axes"])
    assert set(payload["occupation"].keys()) < set(axes_payload["occupation"]["axes"])


async def test_generate_entity_is_deterministic_per_seed_and_profile(
    api_client: httpx.AsyncClient,
) -> None:
    """Determinism should hold for each (seed, axis_profile) pair."""

    full_request = {"seed": 1234, "include_prompts": False, "axis_profile": "character_full"}
    legacy_request = {"seed": 1234, "include_prompts": False, "axis_profile": "subset_legacy"}

    full_a = await api_client.post("/api/entity", json=full_request)
    full_b = await api_client.post("/api/entity", json=full_request)
    legacy_a = await api_client.post("/api/entity", json=legacy_request)
    legacy_b = await api_client.post("/api/entity", json=legacy_request)

    assert full_a.status_code == 200
    assert full_b.status_code == 200
    assert legacy_a.status_code == 200
    assert legacy_b.status_code == 200
    assert full_a.json() == full_b.json()
    assert legacy_a.json() == legacy_b.json()

    # Profiles are intentionally distinct contracts.
    assert full_a.json()["axis_profile"] != legacy_a.json()["axis_profile"]
    assert set(full_a.json()["axes"].keys()) != set(legacy_a.json()["axes"].keys())


async def test_generate_entity_without_seed_returns_integer_seed(
    api_client: httpx.AsyncClient,
) -> None:
    """Unseeded generation should still return a concrete replayable seed."""

    response = await api_client.post("/api/entity", json={"include_prompts": False})

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["seed"], int)
    assert payload["seed"] >= 0


async def test_generate_entity_rejects_unknown_fields(api_client: httpx.AsyncClient) -> None:
    """Request models should reject extra fields (extra='forbid')."""

    response = await api_client.post(
        "/api/entity",
        json={"seed": 1, "include_prompts": True, "unknown_field": "not-allowed"},
    )

    assert response.status_code == 422


async def test_batch_endpoint_uses_sequential_seeds(api_client: httpx.AsyncClient) -> None:
    """Batch endpoint should use start_seed + index sequencing."""

    response = await api_client.post(
        "/api/entities/batch",
        json={"start_seed": 100, "count": 3, "include_prompts": False},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["start_seed"] == 100
    assert payload["count"] == 3
    assert payload["axis_profile"] == "character_full"
    assert len(payload["entities"]) == 3

    seeds = [entity["seed"] for entity in payload["entities"]]
    assert seeds == [100, 101, 102]

    for entity in payload["entities"]:
        assert entity["axis_profile"] == "character_full"
        assert "character" in entity
        assert "occupation" in entity
        assert "prompts" not in entity


async def test_batch_endpoint_accepts_subset_legacy_profile(
    api_client: httpx.AsyncClient,
) -> None:
    """Batch endpoint should preserve explicit legacy profile selection."""

    response = await api_client.post(
        "/api/entities/batch",
        json={
            "start_seed": 10,
            "count": 2,
            "include_prompts": False,
            "axis_profile": "subset_legacy",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["axis_profile"] == "subset_legacy"
    assert [entity["axis_profile"] for entity in payload["entities"]] == [
        "subset_legacy",
        "subset_legacy",
    ]


async def test_batch_endpoint_rejects_out_of_range_count(
    api_client: httpx.AsyncClient,
) -> None:
    """Batch `count` validation should enforce lower/upper bounds."""

    response_too_small = await api_client.post("/api/entities/batch", json={"count": 0})
    response_too_large = await api_client.post("/api/entities/batch", json={"count": 501})

    assert response_too_small.status_code == 422
    assert response_too_large.status_code == 422
