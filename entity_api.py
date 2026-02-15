"""FastAPI service for Pipeworks entity state generation.

This module exposes HTTP endpoints around the existing `condition_axis` library.
It keeps API behavior intentionally thin:

1. Validate request payloads with Pydantic models.
2. Delegate generation logic to the library.
3. Return JSON payloads in a stable structure.

The service is designed to be reverse-proxied by Nginx and run under systemd.
"""

from __future__ import annotations

import random
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

from condition_axis import (
    condition_to_prompt,
    generate_condition,
    generate_occupation_condition,
    get_available_axes,
    get_available_occupation_axes,
    get_axis_values,
    get_occupation_axis_values,
    occupation_condition_to_prompt,
)

app = FastAPI(title="Pipeworks Entity State API", version="0.1.0")


class EntityRequest(BaseModel):
    """Request payload for generating a single entity.

    `seed` is optional. If omitted, the API generates a random replayable seed.
    `include_prompts` controls whether prompt-form strings are included.
    """

    model_config = ConfigDict(extra="forbid")
    seed: int | None = Field(default=None)
    include_prompts: bool = True


class BatchRequest(BaseModel):
    """Request payload for generating multiple entities.

    `start_seed` sets the first deterministic seed in the sequence.
    `count` is bounded to protect service health.
    `include_prompts` controls whether each entity includes prompt strings.
    """

    model_config = ConfigDict(extra="forbid")
    start_seed: int = 0
    count: int = Field(default=10, ge=1, le=500)
    include_prompts: bool = True


def _build_entity(seed: int, include_prompts: bool) -> dict[str, Any]:
    """Build one entity payload from library generators.

    Args:
        seed: Deterministic seed used by generation functions.
        include_prompts: Whether to attach serialized prompt strings.

    Returns:
        Response-ready dictionary for one entity.
    """
    # Generate both axis systems from the same seed so payloads are
    # reproducible and easy to reference/debug by seed.
    character = generate_condition(seed=seed)
    occupation = generate_occupation_condition(seed=seed)

    # Keep response schema explicit and stable for frontend/API consumers.
    payload: dict[str, Any] = {
        "seed": seed,
        "character": character,
        "occupation": occupation,
    }

    # Prompts are optional because some clients only want structured axis data.
    if include_prompts:
        character_prompt = condition_to_prompt(character)
        occupation_prompt = occupation_condition_to_prompt(occupation)
        payload["prompts"] = {
            "character": character_prompt,
            "occupation": occupation_prompt,
            "full": f"{character_prompt}, {occupation_prompt}",
        }
    return payload


def _resolve_seed(requested_seed: int | None) -> int:
    """Resolve a request seed into a concrete integer.

    Args:
        requested_seed: User-provided seed or ``None``.

    Returns:
        A concrete seed integer for generation.
    """
    # If the caller sends a seed, preserve it exactly for deterministic output.
    if requested_seed is not None:
        return requested_seed

    # For unseeded requests, generate a broad-range positive integer so clients
    # can store/replay the returned seed later if desired.
    return random.SystemRandom().randrange(0, 2_147_483_647)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Health endpoint for load balancers and monitoring systems.

    Returns:
        A minimal status object proving process responsiveness.
    """

    return {"status": "ok", "service": "pipeworks-entity-state-api"}


@app.get("/api/axes")
def axes() -> dict[str, Any]:
    """Return available axes and values for all supported generation systems.

    Returns:
        Nested dictionary with axis names and permitted values for:
        - character state generation
        - occupation state generation
    """

    # Pull canonical definitions from the library so this endpoint always
    # mirrors the actual generator configuration.
    character_axes = get_available_axes()
    occupation_axes = get_available_occupation_axes()
    return {
        "character": {
            "axes": character_axes,
            "values": {axis: get_axis_values(axis) for axis in character_axes},
        },
        "occupation": {
            "axes": occupation_axes,
            "values": {axis: get_occupation_axis_values(axis) for axis in occupation_axes},
        },
    }


@app.post("/api/entity")
def generate_entity(req: EntityRequest) -> dict[str, Any]:
    """Generate one entity state payload.

    Args:
        req: Parsed request body.

    Returns:
        One generated entity, optionally with prompt strings.
    """
    seed = _resolve_seed(req.seed)
    return _build_entity(seed=seed, include_prompts=req.include_prompts)


@app.post("/api/entities/batch")
def generate_entities(req: BatchRequest) -> dict[str, Any]:
    """Generate a sequential batch of entity state payloads.

    Args:
        req: Parsed batch request body.

    Returns:
        A dictionary containing metadata plus generated entities.
    """

    # Use sequential seeds to make batch generation deterministic and simple to
    # replay (start_seed + index for each element).
    entities = [
        _build_entity(seed=req.start_seed + index, include_prompts=req.include_prompts)
        for index in range(req.count)
    ]
    return {"start_seed": req.start_seed, "count": req.count, "entities": entities}
