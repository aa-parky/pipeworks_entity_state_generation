HTTP API Service
================

The repository includes a FastAPI service entrypoint at ``entity_api.py`` that
wraps the ``condition_axis`` generators for HTTP clients.

This adapter can be exercised locally with ``uvicorn`` and may later be
promoted into a host-managed service behind nginx, but that hosted-service
shape should be treated as an explicit rollout step rather than as a default
assumption.

Overview
--------

The API exposes:

- health checks for monitoring and load balancers
- discoverability for available axes and values
- single entity generation
- deterministic batch generation

All generation logic is delegated to library functions in
``condition_axis`` so HTTP responses stay aligned with library behavior.

Run Locally
-----------

From the repository root:

.. code-block:: bash

   pip install -e ".[dev]"
   python -m uvicorn entity_api:app --host 127.0.0.1 --port 8400

Then verify:

.. code-block:: bash

   curl -sS http://127.0.0.1:8400/api/health

Endpoints
---------

GET ``/api/health``
^^^^^^^^^^^^^^^^^^^

Purpose:
Returns a minimal status payload to confirm process responsiveness.

Example response:

.. code-block:: json

   {
     "status": "ok",
     "service": "pipeworks-entity-state-api"
   }

GET ``/api/axes``
^^^^^^^^^^^^^^^^^

Purpose:
Returns available axis names and valid values for both systems:

- character
- occupation

Example response (truncated):

.. code-block:: json

   {
     "character": {
       "axes": ["physique", "wealth", "health", "demeanor", "age", "facial_signal"],
       "values": {
         "physique": ["frail", "hunched", "skinny", "..."]
       }
     },
     "occupation": {
       "axes": ["legitimacy", "visibility", "moral_load", "dependency", "risk_exposure"],
       "values": {
         "legitimacy": ["sanctioned", "tolerated", "questioned", "illicit"]
       }
     }
   }

POST ``/api/entity``
^^^^^^^^^^^^^^^^^^^^

Purpose:
Generate one entity payload.

Request body:

.. code-block:: json

   {
     "seed": 42,
     "include_prompts": true,
     "axis_profile": "character_full"
   }

Notes:

- ``seed`` is optional. If omitted, the API generates a random replayable seed.
- ``include_prompts`` defaults to ``true``.
- ``axis_profile`` defaults to ``character_full``.
- ``axis_profile="subset_legacy"`` preserves sparse optional-axis output.

Example response (truncated):

.. code-block:: json

   {
     "seed": 42,
     "axis_profile": "character_full",
     "generator_version": "0.11.4",
     "generator_capabilities": [
       "character_conditions",
       "occupation_conditions",
       "seeded_generation",
       "numeric_axis_scores",
       "prompt_serialization"
     ],
     "character": {
       "physique": "wiry",
       "wealth": "poor",
       "health": "hale",
       "demeanor": "alert",
       "age": "old",
       "facial_signal": "weathered"
     },
     "occupation": {
       "legitimacy": "tolerated",
       "visibility": "routine",
       "moral_load": "neutral",
       "dependency": "necessary",
       "risk_exposure": "straining"
     },
     "axes": {
       "physique": {"label": "wiry", "score": 0.6},
       "visibility": {"label": "routine", "score": 0.67}
     },
     "prompts": {
       "character": "wiry, poor, hale, alert, old, weathered",
       "occupation": "tolerated, routine, neutral, necessary, straining",
       "full": "wiry, poor, hale, alert, old, weathered, tolerated, routine, neutral, necessary, straining"
     }
   }

Notes:

- The library generators may return sparse optional-axis outputs.
- The HTTP adapter's default ``axis_profile="character_full"`` mode emits the
  full canonical character and occupation axis sets.
- ``generator_version`` and ``generator_capabilities`` are part of the
  adapter-facing metadata contract consumed by downstream PipeWorks services.

POST ``/api/entities/batch``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Purpose:
Generate multiple entities using deterministic sequential seeds.

Request body:

.. code-block:: json

   {
     "start_seed": 100,
     "count": 3,
     "include_prompts": false,
     "axis_profile": "character_full"
   }

Validation:

- ``count`` must be between ``1`` and ``500`` (inclusive).

Seed behavior:

- entity ``0`` uses seed ``start_seed``
- entity ``1`` uses seed ``start_seed + 1``
- etc.

Example response (truncated):

.. code-block:: json

   {
     "start_seed": 100,
     "count": 3,
     "axis_profile": "character_full",
     "entities": [
       {"seed": 100, "axis_profile": "character_full", "character": {"physique": "..."}, "occupation": {"legitimacy": "..."}},
       {"seed": 101, "axis_profile": "character_full", "character": {"physique": "..."}, "occupation": {"legitimacy": "..."}},
       {"seed": 102, "axis_profile": "character_full", "character": {"physique": "..."}, "occupation": {"legitimacy": "..."}}
     ]
   }

Test Coverage
-------------

API behavior tests live in ``tests/test_entity_api.py`` and cover:

- endpoint availability and payload shape
- request validation behavior
- deterministic seeded responses
- batch sequencing semantics
