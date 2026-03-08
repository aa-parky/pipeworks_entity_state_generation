# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`pipeworks-conditional-axis` is a structured, rule-based Python framework for generating coherent state descriptions across multiple semantic dimensions (axes). It generates character conditions, facial features, and occupation characteristics for procedural content generation in both visual (AI image prompts) and narrative (game development, MUDs, interactive fiction) contexts.

**Core Philosophy**: Conditions exist on axes (e.g., `Stable ↔ Precarious`) rather than binary flags. The system asks *"Where along this axis does interpretation tilt?"* rather than *"Do you have the condition?"* This modulates resolution margins, biases outcomes, and colors narrative interpretation without prescribing specific outcomes.

## Essential Commands

### Development Setup

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=condition_axis --cov-report=term-missing

# Run specific test file
pytest tests/test_character_conditions_axis.py -v

# Run specific test function
pytest tests/test_character_conditions_axis.py::test_generate_condition_with_seed -v

# Run tests with specific marker
pytest -m unit
pytest -m integration
pytest -m slow
```

### Code Quality

```bash
# Format code with black (line length: 100)
black src/ tests/ --line-length=100

# Lint with ruff (auto-fix)
ruff check src/ tests/ --line-length=100 --fix

# Lint with unsafe fixes enabled
ruff check src/ tests/ --line-length=100 --fix --unsafe-fixes

# Type check with mypy
mypy src/ --python-version=3.12 --ignore-missing-imports

# Run all pre-commit hooks manually
pre-commit run --all-files
```

## Code Architecture

### Core Modules Structure

The package is organized around two primary generation systems, all sharing common utilities:

```
src/condition_axis/
├── _base.py                    # Shared utilities for all generators
├── character_conditions.py     # Physical, social & facial character states
└── occupation_axis.py          # Occupation characteristics
```

**Note**: The `facial_conditions.py` module has been deprecated and merged into `character_conditions.py`. It is kept in the repository for historical reference but should not be used in new code.

### The Axis Pattern

All three systems follow the same architectural pattern:

1. **AXES Definition**: Dictionary mapping axis names to possible values
   - Example: `"physique": ["skinny", "wiry", "stocky", "hunched", "frail", "broad"]`

2. **POLICY**: Rules for mandatory vs optional axes
   - `mandatory`: Always included axes (baseline state)
   - `optional`: Conditionally included axes (narrative detail)
   - `max_optional`: Prevents prompt dilution

3. **WEIGHTS**: Probability distributions for realistic populations
   - Example: `"poor": 4.0, "wealthy": 1.0` (poor is 4x more common)
   - Unweighted axes use uniform distribution

4. **EXCLUSIONS**: Semantic coherence rules preventing illogical combinations
   - Format: `{(axis, value): {blocked_axis: [blocked_values]}}`
   - Example: `{("wealth", "decadent"): {"health": ["sickly", "frail"]}}` - wealth enables healthcare

### Shared Utilities (_base.py)

All generators use three core functions:

- `weighted_choice(options, weights)`: Core selection mechanism with probability distributions
- `apply_exclusion_rules(chosen, exclusions)`: Applies semantic constraints to prevent nonsense
- `values_to_prompt(condition_dict)`: Serializes to comma-separated prompt format

### Generation Flow

Each system follows this sequence:

1. Seed the random number generator (optional, for reproducibility)
2. Select mandatory axes using weighted_choice()
3. Randomly select 0-N optional axes (up to max_optional)
4. For each selected axis, use weighted_choice() to pick a value
5. Apply exclusion rules to remove incompatible combinations
6. Return structured dict {axis: value}

### Serialization

All systems provide `<type>_condition_to_prompt()` functions that convert structured dicts to comma-separated strings suitable for diffusion models and narrative text.

## Important Constraints

### Python Version

- **Minimum**: Python 3.12
- Uses modern type hints (`dict[str, str]`, not `Dict[str, str]`)
- Relies on dict insertion order (guaranteed in Python 3.7+)

### Zero Runtime Dependencies

- Pure Python implementation
- No external libraries required for core functionality
- Dev dependencies (pytest, black, ruff, mypy) only for development

### Code Style

- Line length: 100 characters (enforced by black and ruff)
- Type hints required for all public APIs
- Docstrings follow Google style
- All modules use structured logging (`import logging`)

### Testing Philosophy

- All tests use seeds for reproducibility
- Tests verify both structure (dict keys) and determinism (exact values with seed)
- Exclusion rules are tested with specific triggered combinations
- Coverage target: high coverage on core generation logic

## Cross-System Integration

Facial signals are integrated into the character conditions system. Cross-system exclusion rules are implemented between character axes (including facial):

**Implemented exclusions:**

- `age="young"` + `facial_signal="weathered"` (contradiction)
- `age="ancient"` + `facial_signal="understated"` (ancient is rarely subtle)
- `wealth="decadent"` + `facial_signal="weathered"` (wealth preserves appearance)
- `health="hale"` + `facial_signal="weathered"` (health affects appearance)
- `health="sickly"` + `facial_signal="soft-featured"` (redundant signal)

**Future integration:**

- Cross-validation with occupation axes (e.g., `demeanor="timid"` + `visibility="conspicuous"`)
- Weighted preferences for complementary combinations

## GitHub Actions

### CI/CD Workflows

- **test.yml**: Runs pytest on Python 3.12 and 3.13, uploads coverage to Codecov
- **lint.yml**: Runs ruff (auto-fixes and commits), black (check-only), and mypy
- **publish.yml**: Publishes to PyPI on release tags

### Pre-commit Hooks

The repository uses pre-commit hooks for:

- Trailing whitespace removal
- End-of-file fixing
- YAML/TOML/JSON validation
- Black formatting (100 chars)
- Ruff linting with auto-fix
- MyPy type checking (excludes tests/)

## Extension Guidelines

### Adding New Axes to Existing Systems

1. Add axis values to the AXES dict
2. Decide if mandatory or optional (update POLICY)
3. Add weights if non-uniform distribution desired
4. Define exclusion rules for semantic coherence
5. Add tests with seeds to verify deterministic behavior

### Creating New Condition Systems

1. Copy the pattern from character_conditions.py
2. Define your AXES, POLICY, WEIGHTS, EXCLUSIONS
3. Use `weighted_choice()` and `apply_exclusion_rules()` from _base
4. Write `generate_<type>_condition()` and `<type>_condition_to_prompt()` functions
5. Export via **init**.py
6. Add comprehensive tests

### Exclusion Rule Design

Exclusions encode domain knowledge about incompatible combinations:

- Physical impossibilities (e.g., "broad + frail")
- Socioeconomic contradictions (e.g., "wealthy + sickly")
- Behavioral incoherence (e.g., "ancient + timid")

Exclusions are applied **after** random selection, removing conflicts rather than preventing selection. This allows for transparent debugging and maintains generative variety.
