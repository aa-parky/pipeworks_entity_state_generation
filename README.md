[![CI](https://github.com/pipe-works/pipeworks_entity_state_generation/actions/workflows/ci.yml/badge.svg)](https://github.com/pipe-works/pipeworks_entity_state_generation/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/pipe-works/pipeworks_entity_state_generation/branch/main/graph/badge.svg)](https://codecov.io/gh/pipe-works/pipeworks_entity_state_generation)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

# PipeWorks Conditional Axis

`pipeworks_entity_state_generation` provides the structured, rule-based entity
state generation library used for procedural character and occupation
descriptions across the PipeWorks ecosystem. It is a Python package first, not
the canonical runtime authority for game state.

## PipeWorks Workspace

These repositories are designed to live inside a shared PipeWorks workspace
rooted at `/srv/work/pipeworks`.

- `repos/` contains source checkouts only.
- `venvs/` contains per-project virtual environments such as `pw-mud-server`.
- `runtime/` contains mutable runtime state such as databases, exports, session
  files, and caches.
- `logs/` contains service-owned log output when a project writes logs outside
  the process manager.
- `config/` contains workspace-level configuration files that should not be
  treated as source.
- `bin/` contains optional workspace helper scripts.
- `home/` is reserved for workspace-local user data when a project needs it.

Across the PipeWorks ecosphere, the rule is simple: keep source in `repos/`,
keep mutable state outside the repo checkout, and use explicit paths between
repos when one project depends on another.

## What This Repo Owns

This repository is the source of truth for:

- character-condition and occupation-condition axis definitions
- weighted generation, exclusion rules, and reproducible seeded output
- prompt-serialization helpers such as `condition_to_prompt`
- examples showing integration with image-generation and narrative workflows

This repository does not own:

- canonical mud-server policy/runtime state
- browser UIs or admin tools
- package-import or artifact-exchange workflows

## Public API

The public package is `condition_axis`.

Common entry points include:

- `generate_condition`
- `generate_occupation_condition`
- `condition_to_prompt`
- `occupation_condition_to_prompt`
- `get_available_axes`
- `get_axis_values`
- `get_available_occupation_axes`
- `get_occupation_axis_values`

The package is designed for reproducible generation via explicit seeds and for
inspection of the underlying axis/weight/exclusion structures.

## Repository Layout

- `src/condition_axis/character_conditions.py` character-state axes and helpers
- `src/condition_axis/occupation_axis.py` occupation-state axes and helpers
- `examples/` runnable examples for basic, advanced, batch, and image-prompt
  usage
- `tests/` pytest coverage, including example validation
- `docs/` project documentation
- `deploy/` example deployment assets for API-style integration surfaces

## Quick Start

Create a dedicated workspace venv and install the package:

```bash
python3 -m venv /srv/work/pipeworks/venvs/pw-entity-state-generation
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/pip install -e ".[dev]"
```

Minimal usage:

```python
from condition_axis import (
    condition_to_prompt,
    generate_condition,
    generate_occupation_condition,
    occupation_condition_to_prompt,
)

character = generate_condition(seed=42)
occupation = generate_occupation_condition(seed=42)

character_prompt = condition_to_prompt(character)
occupation_prompt = occupation_condition_to_prompt(occupation)
```

Run the bundled examples from the repo root:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python examples/basic_usage.py
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python examples/integration_example.py
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/python examples/image_prompt_generation.py
```

## Integration Role

This package is suitable for:

- deterministic pre-generation of entity descriptors
- prompt-building for image or text rendering systems
- optional integration behind service boundaries such as `pipeworks_mud_server`

It is not a substitute for runtime authority. If a host application needs to
store, validate, or expose generated state over HTTP, that responsibility stays
with the consuming service.

## Validation And Development

Run the main checks from the repo root:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/pytest
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/ruff check src tests examples
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/black --check src tests examples
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/mypy src
```

If you need the docs toolchain:

```bash
/srv/work/pipeworks/venvs/pw-entity-state-generation/bin/pip install -e ".[docs]"
make -C docs html
```

## Documentation

Additional documentation lives in `docs/`.

The runnable example set is summarized in [examples/README.md](examples/README.md).

## License

[GPL-3.0-or-later](LICENSE)
