[![Tests](https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/test.yml/badge.svg)](https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/test.yml) [![Lint & Type Check](https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/lint.yml/badge.svg)](https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/lint.yml) [![codecov](https://codecov.io/gh/aa-parky/pipeworks_entity_state_generation/branch/main/graph/badge.svg)](https://codecov.io/gh/aa-parky/pipeworks_entity_state_generation)[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# Pipeworks Conditional Axis

A structured, rule-based Python framework for generating coherent character and entity state descriptions across multiple semantic dimensions. Designed for procedural content generation in both visual contexts (AI image prompts) and narrative systems (game development, MUDs, interactive fiction).

**Core Philosophy**: Conditions exist on axes (e.g., `Stable ↔ Precarious`) rather than binary flags. The system asks *"Where along this axis does interpretation tilt?"* rather than *"Do you have the condition?"* This modulates resolution margins, biases outcomes, and colors narrative interpretation without prescribing specific outcomes.

---

## What This Library Does

This library generates **structured, interpretable state** for entities during generation time.

It is not a rendering system, a simulation engine, or a narrative framework.

Its sole responsibility is to answer the question:

> **"What is the state of this thing, and where does it behave slightly off-pattern?"**

State is expressed through **conditional axes**—structured, population-weighted descriptors that bias probability and interpretation without dictating outcomes.

---

## Installation

```bash
# Install from PyPI (when published)
pip install pipeworks-conditional-axis

# Install from source for development
git clone https://github.com/aa-parky/pipeworks_entity_state_generation.git
cd pipeworks_entity_state_generation
pip install -e ".[dev]"
```

**Requirements**: Python 3.12+

---

## Quick Start

```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    generate_occupation_condition,
    condition_to_prompt,
    facial_condition_to_prompt,
    occupation_condition_to_prompt,
)

# Generate character physical and social state
character_state = generate_condition(seed=42)
print(character_state)
# {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'}

# Generate facial perception modifiers
facial_state = generate_facial_condition(seed=42)
print(facial_state)
# {'overall_impression': 'weathered'}

# Generate occupation characteristics
occupation_state = generate_occupation_condition(seed=42)
print(occupation_state)
# {'legitimacy': 'tolerated', 'visibility': 'discreet', 'moral_load': 'burdened'}

# Convert to comma-separated prompts (for image generation, text, etc.)
char_prompt = condition_to_prompt(character_state)
face_prompt = facial_condition_to_prompt(facial_state)
occ_prompt = occupation_condition_to_prompt(occupation_state)

full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
print(full_prompt)
# "wiry, poor, weary, weathered, tolerated, discreet, burdened"
```

---

## What Are Conditional Axes?

Conditional axes describe the **current lived state** of an entity.

They are:

- **Mutually exclusive within an axis**: A character can't be both "wealthy" and "poor"
- **Population-weighted**: Poor characters are more common than wealthy ones
- **Explainable and auditable**: Every value comes from a traceable rule
- **Resolved once during generation**: Deterministic given the same seed

### Available Axis Systems

The library currently provides three independent axis systems:

#### 1. Character Conditions (`character_conditions`)
Physical and social states that establish baseline character presentation:

- **Physique**: `skinny`, `wiry`, `stocky`, `hunched`, `frail`, `broad`
- **Wealth**: `poor`, `modest`, `well-kept`, `wealthy`, `decadent`
- **Health**: `sickly`, `scarred`, `weary`, `hale`, `limping`
- **Demeanor**: `timid`, `suspicious`, `resentful`, `alert`, `proud`
- **Age**: `young`, `middle-aged`, `old`, `ancient`

#### 2. Facial Conditions (`facial_conditions`)
Perception modifiers that bias how faces are interpreted:

- **Overall Impression**: `youthful`, `weathered`, `stern`, `gentle`, `marked`, `unremarkable`

#### 3. Occupation Conditions (`occupation_axis`)
Labor pressures and social positioning (not job titles):

- **Legitimacy**: `sanctioned`, `tolerated`, `questioned`, `illicit`
- **Visibility**: `hidden`, `discreet`, `routine`, `conspicuous`
- **Moral Load**: `neutral`, `burdened`, `conflicted`, `corrosive`
- **Dependency**: `optional`, `useful`, `necessary`, `unavoidable`
- **Risk Exposure**: `benign`, `straining`, `hazardous`, `eroding`

---

## Key Features

### Weighted Probability Distributions

Axes use realistic population weights rather than uniform randomness:

```python
# Wealth distribution (from WEIGHTS)
"poor": 4.0      # Most common
"modest": 3.0
"well-kept": 2.0
"wealthy": 1.0
"decadent": 0.5  # Rare
```

This creates believable populations where most characters are poor or modest.

### Semantic Exclusion Rules

The system prevents illogical combinations through exclusion rules:

- Decadent characters can't be frail or sickly (wealth enables healthcare)
- Ancient characters aren't timid (age brings confidence)
- Broad, strong physiques don't pair with sickness
- Hale (healthy) characters shouldn't have frail physiques

Exclusions are applied **after** random selection, removing conflicts rather than preventing selection. This allows for transparent debugging and maintains generative variety.

### Mandatory and Optional Axes

Axes are categorized as **mandatory** (always included) or **optional** (conditionally included):

- Character conditions: Physique and wealth are mandatory; health, demeanor, and age are optional (0-2 selected)
- Facial conditions: Overall impression is mandatory
- Occupation conditions: All five axes are mandatory

This prevents prompt dilution while maintaining narrative clarity.

### Reproducible Generation

All generation functions accept an optional `seed` parameter for deterministic output:

```python
# Same seed = same result
char1 = generate_condition(seed=42)
char2 = generate_condition(seed=42)
assert char1 == char2  # True
```

---

## Repository Structure

```text
pipeworks_entity_state_generation/
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant development guide
├── LICENSE                      # GPL-3.0
├── pyproject.toml              # Package configuration
├── pytest.ini                  # Test configuration
│
├── src/condition_axis/         # Main package
│   ├── __init__.py             # Public API exports
│   ├── _base.py                # Shared utilities
│   ├── character_conditions.py # Physical & social states
│   ├── facial_conditions.py    # Facial perception modifiers
│   └── occupation_axis.py      # Occupation characteristics
│
├── tests/                      # Test suite (90%+ coverage)
│   ├── test_character_conditions_axis.py
│   ├── test_facial_conditions_axis.py
│   └── test_occupation_axis_axis.py
│
├── docs/                       # Documentation & guides
│   ├── README.md               # Documentation overview
│   ├── api/                    # API reference documentation
│   │   ├── _base.md
│   │   ├── character_conditions.md
│   │   ├── facial_conditions.md
│   │   └── occupation_axis.md
│   ├── design/                 # Philosophy & architecture
│   │   ├── 00_goblin_laws.md
│   │   ├── 01_character_state_model.md
│   │   ├── 02_pipeworks_system_architecture.md
│   │   ├── 03_pipeworks_components.md
│   │   └── 04_characters_first_narrow_door.md
│   ├── specifications/         # Technical specifications
│   │   ├── condition_axis.md
│   │   ├── occupation_axis.md
│   │   └── Obey_the_Verb.md
│   ├── guides/                 # Setup & process guides
│   │   ├── GitHub Actions CI Setup Guide.md
│   │   └── Pre-Commit Hooks Setup Guide.md
│   └── images/                 # Documentation images
│       ├── condition_axis.jpg
│       ├── miss_filed.jpg
│       └── verbs_conditions.jpg
│
└── .github/workflows/          # CI/CD
    ├── test.yml                # Test runner
    ├── lint.yml                # Code quality checks
    └── publish.yml             # PyPI publishing
```

---

## Design Principles

### Interpretation Over Prescription

Conditions **bias** interpretation rather than dictate outcomes:

- "weary" suggests fragility, hesitation, or cost—it doesn't prevent action
- "wealthy" biases confidence and access—it doesn't guarantee success

### Bias Over Randomness

Weighted distributions reflect population realism:

- Most characters are poor or modest
- Ancient characters are rare
- Sickly and frail conditions cluster at population margins

### Structure With Room for Failure

Exclusion rules prevent nonsense, but edge cases are allowed:

- A "decadent" character might be "scarred" (past injury despite current wealth)
- An "ancient" character can be "limping" (age brings wear)

The system aims for **coherence**, not perfection.

### Explainable State, Inexplicable Detail

Generated state is fully traceable (seed, weights, exclusions), but the **why** remains interpretive:

- Why is this character suspicious? The axis doesn't say—narrative fills the gap.
- Why is this occupation burdensome? The pressure exists, the story provides context.

---

## What This Repository Is Not

This repository does **not**:

- Render text or images
- Simulate behavior over time
- Implement progression systems
- Resolve narrative outcomes
- Balance gameplay
- Define UI or player interaction

Those concerns belong downstream. This library produces **generation-time primitives** for consumption by rendering, simulation, and narrative systems.

---

## Advanced Usage

### Combining Multiple Axis Systems

```python
# Generate complete character with all three systems
character = generate_condition(seed=123)
facial = generate_facial_condition(seed=123)
occupation = generate_occupation_condition(seed=123)

# Serialize for image prompt
image_prompt = (
    f"illustration of a pale blue-green goblin, "
    f"{condition_to_prompt(character)}, "
    f"{facial_condition_to_prompt(facial)}, "
    f"whose work operates under the following conditions: "
    f"{occupation_condition_to_prompt(occupation)}"
)
```

### Inspecting Available Axes and Values

```python
from condition_axis import (
    get_available_axes,
    get_axis_values,
    CONDITION_AXES,
    WEIGHTS,
)

# List all character condition axes
print(get_available_axes())
# ['physique', 'wealth', 'health', 'demeanor', 'age']

# Get possible values for an axis
print(get_axis_values('wealth'))
# ['poor', 'modest', 'well-kept', 'wealthy', 'decadent']

# Access raw data structures
print(CONDITION_AXES['physique'])
# ['skinny', 'wiry', 'stocky', 'hunched', 'frail', 'broad']

print(WEIGHTS['wealth'])
# {'poor': 4.0, 'modest': 3.0, 'well-kept': 2.0, 'wealthy': 1.0, 'decadent': 0.5}
```

### Adding Cross-System Exclusions (Future Work)

Currently, each axis system operates independently. When combining systems, you may want to implement cross-system validation:

- `age="young"` + `facial="weathered"` (contradiction)
- `wealth="decadent"` + `legitimacy="illicit"` (possible, adds criminal wealth angle)
- `demeanor="timid"` + `visibility="conspicuous"` (behavioral contradiction)

See [CLAUDE.md](./CLAUDE.md) for extension guidelines.

---

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/aa-parky/pipeworks_entity_state_generation.git
cd pipeworks_entity_state_generation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=condition_axis --cov-report=term-missing

# Run specific test file
pytest tests/test_character_conditions_axis.py -v
```

### Code Quality

```bash
# Format code (line length: 100)
black src/ tests/ --line-length=100

# Lint with auto-fix
ruff check src/ tests/ --line-length=100 --fix

# Type check
mypy src/ --python-version=3.12 --ignore-missing-imports

# Run all pre-commit hooks
pre-commit run --all-files
```

---

## Future Work

### Planned Enhancements

- **Cross-system exclusion rules**: Validate compatibility between character, facial, and occupation axes
- **Unified generator**: Single function to generate complete entity state with cross-system coherence
- **Quirks system**: Persistent, localized irregularities that introduce structured deviation (see "Quirks" below)
- **Serialization/deserialization**: JSON and YAML support for storing and reloading states
- **Condition history tracking**: Ledger-based system for tracking state evolution over time

### The Quirks System (Planned)

Future versions will introduce **quirks**—small, persistent deviations that:

- Remain local to an entity
- Do not resolve into system-wide rules
- Bias attention and interpretation
- Repeat without fully explaining themselves

Quirks will answer:

> **"Where does this entity fail to behave like a clean model?"**

They will complicate situations but must never resolve them. Quirks will be intentionally **orthogonal** to conditional axes:

- Axes resolve state; quirks annotate state
- Axes bias probability; quirks bias attention
- Quirks must not influence axis resolution or weighting

This separation ensures axes push toward coherence while quirks prevent the system from becoming too clean.

---

## Integration with Pipeworks Ecosystem

This library is part of the broader [Pipeworks](https://github.com/aa-parky) project:

| Repository | Role | Relationship to This Library |
|-----------|------|------------------------------|
| **pipeworks-artefact** | Canonical registry and memory layer | Stores generated states and provides persistent identity |
| **pipeworks_entity_state_generation** | Generation engine (this repo) | Produces entity state snapshots |
| **pipeworks_mud_server** | Interactive runtime and game logic | Consumes entity states during play |
| **pipeworks_image_generator** | Visualization and image synthesis | Interprets entity states for visual representation |
| **the_daily_undertaking_ui** | Narrative and user-facing interface | Surfaces entity states to players |

See [docs/design/02_pipeworks_system_architecture.md](./docs/design/02_pipeworks_system_architecture.md) for detailed integration documentation.

---

## License

GPL-3.0

This repository is part of the broader Pipeworks project.

---

## Documentation

### Main Documentation
- [CLAUDE.md](./CLAUDE.md) - Development guide for AI assistants and contributors
- [Project TODO List](./Project_TODO_List.md) - Development roadmap and progress tracking
- [docs/README.md](./docs/README.md) - Complete documentation index with reading paths

### API Reference
- [Base Utilities](./docs/api/_base.md) - Core utilities (weighted_choice, apply_exclusion_rules, values_to_prompt)
- [Character Conditions](./docs/api/character_conditions.md) - Physical & social character state generation
- [Facial Conditions](./docs/api/facial_conditions.md) - Facial perception modifiers
- [Occupation Axis](./docs/api/occupation_axis.md) - Occupation characteristics generation

### Design & Philosophy
- [Goblin Laws](./docs/design/00_goblin_laws.md) - Architectural principles and design philosophy
- [Character State Model](./docs/design/01_character_state_model.md) - Conceptual foundation for state representation
- [Pipeworks System Architecture](./docs/design/02_pipeworks_system_architecture.md) - How this library fits into the larger ecosystem
- [Pipeworks Components](./docs/design/03_pipeworks_components.md) - The five load-bearing parts of the system
- [Characters First](./docs/design/04_characters_first_narrow_door.md) - Design decision rationale

### Technical Specifications
- [Character Conditions](./docs/specifications/condition_axis.md) - Character condition system specification
- [Occupation Axis](./docs/specifications/occupation_axis.md) - Occupation characteristics specification
- [Obey the Verb](./docs/specifications/Obey_the_Verb.md) - AI image generation prompting strategy

### Setup Guides
- [Pre-Commit Hooks Setup](./docs/guides/Pre-Commit%20Hooks%20Setup%20Guide.md) - Local development setup
- [GitHub Actions CI Setup](./docs/guides/GitHub%20Actions%20CI%20Setup%20Guide.md) - CI/CD configuration

---

## Contributing

Contributions are welcome! Please see [CLAUDE.md](./CLAUDE.md) for:

- Code architecture and patterns
- Testing philosophy
- Code style guidelines (Black, Ruff, MyPy)
- How to add new axes or condition systems

Before submitting a PR:

1. Ensure all tests pass: `pytest`
2. Verify code quality: `pre-commit run --all-files`
3. Add tests for new functionality
4. Update documentation as needed

---

## Status

This library is in active development (v1.0.0).

Core generation systems (character, facial, occupation) are **stable and production-ready**.

Interfaces, schemas, and axis definitions may evolve, but the core separation between state resolution (axes) and state interpretation (downstream systems) is considered foundational.
