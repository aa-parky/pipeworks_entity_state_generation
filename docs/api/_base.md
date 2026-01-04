# `_base` - Shared Utilities for Condition Axis Generation

**Module**: `condition_axis._base`

**Purpose**: Core utilities shared across all condition axis generators (character, facial, occupation).

This module provides the foundational functions used by all generation systems to maintain consistency, reduce code duplication, and implement the core axis pattern: weighted probability selection, semantic exclusion rules, and serialization.

---

## Overview

The condition axis system generates structured state descriptions across multiple semantic dimensions. This module contains three essential utilities:

1. **`weighted_choice()`** - Probabilistic selection with optional weights
2. **`apply_exclusion_rules()`** - Semantic coherence enforcement
3. **`values_to_prompt()`** - Serialization to prompt format

All condition generators (character, facial, occupation) use these functions to ensure consistent behavior.

---

## Core Concepts

### Axes
Semantic dimensions with discrete values (e.g., `physique: [skinny, wiry, stocky, hunched, frail, broad]`)

### Weights
Probability distributions that create realistic populations (e.g., `poor: 4.0, wealthy: 1.0` makes poverty 4x more common)

### Exclusions
Semantic constraints that prevent illogical combinations (e.g., `wealth=decadent` excludes `health=sickly`)

### Policy
Rules defining which axes are mandatory (always included) vs. optional (conditionally included)

---

## Functions

### `weighted_choice()`

Select a random option with optional weighted probabilities.

This is the core selection mechanism for all condition axis generators. It enables both uniform and weighted probability distributions, allowing for realistic population modeling.

#### Signature

```python
def weighted_choice(
    options: list[str],
    weights: dict[str, float] | None = None
) -> str
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `list[str]` | **Required.** List of possible values to choose from. Must be non-empty. |
| `weights` | `dict[str, float] \| None` | **Optional.** Dictionary mapping options to weights. If `None` or missing entries, defaults to uniform distribution. Weights must be non-negative (zero weight means never selected). |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Randomly selected option from the input list |

#### Behavior

- **Uniform distribution**: When `weights=None`, all options are equally likely (uses `random.choice()`)
- **Weighted distribution**: When `weights` is provided, selection probability is proportional to weight values
- **Partial weights**: Options missing from weights dict default to weight of `1.0`
- **Performance**: Fast path for uniform distribution avoids weight calculation overhead

#### Examples

**Uniform distribution (all equally likely)**
```python
from condition_axis._base import weighted_choice

result = weighted_choice(["a", "b", "c"])
# Result: 'a', 'b', or 'c' with equal probability (33.3% each)
```

**Weighted distribution (biased toward common values)**
```python
result = weighted_choice(
    ["rare", "common"],
    {"rare": 1.0, "common": 5.0}
)
# Result: 'rare' 16.7% of the time, 'common' 83.3% of the time
```

**Partial weights (missing options default to 1.0)**
```python
result = weighted_choice(
    ["a", "b", "c"],
    {"a": 3.0}  # a=3.0, b=1.0 (default), c=1.0 (default)
)
# Result: 'a' 60% of the time, 'b' 20%, 'c' 20%
```

**Realistic population modeling**
```python
wealth_options = ["poor", "modest", "well-kept", "wealthy", "decadent"]
wealth_weights = {
    "poor": 4.0,      # 40% of population
    "modest": 3.0,    # 30%
    "well-kept": 2.0, # 20%
    "wealthy": 1.0,   # 5%
    "decadent": 0.5   # 5%
}

wealth = weighted_choice(wealth_options, wealth_weights)
# Creates believable economic distributions
```

#### Implementation Notes

- Uses Python's `random.choices()` for weighted selection
- Uses `random.choice()` for uniform distribution (performance optimization)
- Thread-safety depends on Python's random module (uses thread-local RNG)
- RNG state is controlled by `random.seed()` for reproducibility

#### Common Use Cases

1. **Population realism**: Make common conditions appear more frequently
2. **Rarity systems**: Create rare but possible combinations
3. **Bias without hard rules**: Influence without prescribing outcomes
4. **Deterministic testing**: Use with seed for reproducible generation

---

### `apply_exclusion_rules()`

Apply semantic exclusion rules to remove illogical combinations from generated state.

Exclusion rules encode domain knowledge about incompatible combinations. For example: "wealthy + frail" is unlikely (wealth enables healthcare), or "ancient + timid" is incoherent (age brings confidence).

#### Signature

```python
def apply_exclusion_rules(
    chosen: dict[str, str],
    exclusions: dict[tuple[str, str], dict[str, list[str]]]
) -> dict[str, str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `chosen` | `dict[str, str]` | **Required.** Dictionary mapping axis names to selected values. **Modified in-place** as exclusions are applied. |
| `exclusions` | `dict[tuple[str, str], dict[str, list[str]]]` | **Required.** Dictionary of exclusion rules. Format: `{(axis, value): {blocked_axis: [blocked_values]}}` |

#### Returns

| Type | Description |
|------|-------------|
| `dict[str, str]` | The modified `chosen` dictionary (same reference, returned for convenience) |

#### Behavior

- **In-place modification**: The `chosen` dict is modified directly
- **Triggered by presence**: Rules activate when `chosen[axis] == value`
- **Cascade removal**: All conflicting values are removed from the dict
- **Deterministic order**: Removal order follows dict iteration order (insertion order in Python 3.7+)
- **Logging**: All exclusions are logged at DEBUG level for debugging

#### Exclusion Rule Format

```python
exclusions = {
    (trigger_axis, trigger_value): {
        blocked_axis_1: [blocked_value_1, blocked_value_2],
        blocked_axis_2: [blocked_value_3]
    }
}
```

**Interpretation**: If `chosen[trigger_axis] == trigger_value`, remove any entries where the axis matches a blocked axis and the value is in the blocked values list.

#### Examples

**Basic exclusion (wealth excludes poor health)**
```python
from condition_axis._base import apply_exclusion_rules

chosen = {"wealth": "decadent", "health": "sickly"}
exclusions = {
    ("wealth", "decadent"): {
        "health": ["sickly", "frail"]
    }
}

result = apply_exclusion_rules(chosen, exclusions)
# Result: {'wealth': 'decadent'}
# 'health' removed because decadent wealth excludes sickness
```

**No exclusion triggered**
```python
chosen = {"age": "young", "demeanor": "alert"}
exclusions = {
    ("age", "ancient"): {
        "demeanor": ["timid"]
    }
}

result = apply_exclusion_rules(chosen, exclusions)
# Result: {'age': 'young', 'demeanor': 'alert'}
# No change - exclusion only applies to age=ancient
```

**Multiple exclusions**
```python
chosen = {
    "physique": "broad",
    "health": "sickly",
    "demeanor": "timid"
}
exclusions = {
    ("physique", "broad"): {
        "health": ["sickly", "frail"],
        "demeanor": ["timid"]
    }
}

result = apply_exclusion_rules(chosen, exclusions)
# Result: {'physique': 'broad'}
# Both health and demeanor removed due to conflict
```

**Real-world example (character conditions)**
```python
chosen = {
    "physique": "wiry",
    "wealth": "decadent",
    "health": "frail",
    "age": "ancient",
    "demeanor": "timid"
}

exclusions = {
    ("wealth", "decadent"): {
        "health": ["sickly", "frail"]  # Wealth enables healthcare
    },
    ("age", "ancient"): {
        "demeanor": ["timid"]  # Age brings confidence
    }
}

result = apply_exclusion_rules(chosen, exclusions)
# Result: {'physique': 'wiry', 'wealth': 'decadent', 'age': 'ancient'}
# Removed: health=frail, demeanor=timid (both excluded)
```

#### Design Rationale

**Why exclusions happen after generation, not before:**

1. **Transparency**: You can see what was generated before exclusions
2. **Debugging**: Logs show exactly what was removed and why
3. **Flexibility**: Same generation code works with different exclusion sets
4. **Variety**: Rare but valid combinations can still emerge

**Why in-place modification:**

1. **Performance**: Avoids copying dictionaries
2. **Simplicity**: Single source of truth for the state
3. **Chainability**: Return value allows method chaining

#### Common Use Cases

1. **Semantic coherence**: Prevent nonsensical combinations
2. **Domain knowledge**: Encode expert understanding of the domain
3. **Cross-axis validation**: Ensure multiple axes are mutually compatible
4. **Debugging generation**: Log what combinations are being rejected

#### Logging

When exclusions are applied, you'll see DEBUG-level logs:

```
DEBUG: Exclusion rule triggered: wealth=decadent
DEBUG:   Removed health=frail (conflicts with wealth=decadent)
INFO: Applied 1 exclusion rule(s)
```

Enable with:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

### `values_to_prompt()`

Convert structured condition data to a comma-separated prompt fragment.

This is the canonical serialization format for condition axis data. The output is designed to be human-readable, diffusion model friendly, and consistent across all condition axis types.

#### Signature

```python
def values_to_prompt(condition_dict: dict[str, str]) -> str
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `condition_dict` | `dict[str, str]` | **Required.** Dictionary mapping axis names to values (output from any `generate_*` function) |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Comma-separated string of condition values. Order is deterministic (follows dict insertion order). Empty dict returns empty string. |

#### Behavior

- **Values only**: Only includes values, not axis names (for prompt clarity)
- **Deterministic order**: Maintains insertion order from generation (Python 3.7+ guarantee)
- **Comma-separated**: Standard diffusion model format
- **Empty safe**: Returns `""` for empty dicts (not `None` or error)

#### Examples

**Basic usage**
```python
from condition_axis._base import values_to_prompt

prompt = values_to_prompt({"physique": "wiry", "wealth": "poor"})
# Result: 'wiry, poor'
```

**Multiple axes**
```python
condition = {
    "physique": "stocky",
    "wealth": "modest",
    "health": "hale",
    "age": "old"
}
prompt = values_to_prompt(condition)
# Result: 'stocky, modest, hale, old'
```

**Empty dict**
```python
prompt = values_to_prompt({})
# Result: ''
```

**Order preservation**
```python
condition = {"a": "first", "b": "second", "c": "third"}
prompt = values_to_prompt(condition)
# Result: 'first, second, third'
# Order matches insertion order
```

**Image generation integration**
```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    condition_to_prompt,
    facial_condition_to_prompt
)

char = generate_condition(seed=42)
face = generate_facial_condition(seed=42)

char_prompt = condition_to_prompt(char)  # Uses values_to_prompt internally
face_prompt = facial_condition_to_prompt(face)

full_prompt = f"illustration of a goblin, {char_prompt}, {face_prompt}"
# Result: "illustration of a goblin, wiry, poor, weary, weathered"
```

#### Design Rationale

**Why values only, not keys:**

Good: `"wiry, poor, weathered"`
Bad: `"physique: wiry, wealth: poor, impression: weathered"`

The values are semantically meaningful on their own. Including axis names adds noise for image generation and narrative use.

**Why comma-separated:**

1. Standard format for diffusion models (Stable Diffusion, DALL-E, etc.)
2. Human-readable for debugging
3. Easy to concatenate multiple sources
4. Can be parsed back if needed

**Why deterministic order:**

1. Reproducible prompts given same input
2. Testable behavior
3. Predictable concatenation

#### Common Use Cases

1. **Image generation**: Convert state to diffusion model prompts
2. **Narrative text**: Use values in procedural descriptions
3. **Logging/debugging**: Human-readable state representation
4. **Serialization**: Simple format for storage or transmission

#### Type Aliases

The module uses this pattern for consistency:

```python
# Each module provides a typed wrapper
def condition_to_prompt(condition: dict[str, str]) -> str:
    """Character condition to prompt."""
    return values_to_prompt(condition)

def facial_condition_to_prompt(facial: dict[str, str]) -> str:
    """Facial condition to prompt."""
    return values_to_prompt(facial)
```

This provides better type hints and module-specific naming while using the same underlying implementation.

---

## Module Exports

```python
__all__ = [
    "apply_exclusion_rules",
    "values_to_prompt",
    "weighted_choice",
]
```

Only these three functions are part of the public API. Other module contents are internal implementation details.

---

## Usage Patterns

### Pattern 1: Basic Weighted Generation

```python
from condition_axis._base import weighted_choice

PHYSIQUE_OPTIONS = ["skinny", "wiry", "stocky", "hunched", "frail", "broad"]
PHYSIQUE_WEIGHTS = {
    "skinny": 2.0,
    "wiry": 3.0,
    "stocky": 3.0,
    "hunched": 1.0,
    "frail": 1.0,
    "broad": 2.0
}

physique = weighted_choice(PHYSIQUE_OPTIONS, PHYSIQUE_WEIGHTS)
```

### Pattern 2: Generate with Exclusions

```python
from condition_axis._base import weighted_choice, apply_exclusion_rules

# Step 1: Generate independently
chosen = {
    "physique": weighted_choice(["skinny", "broad"], {"skinny": 1, "broad": 1}),
    "health": weighted_choice(["sickly", "hale"], {"sickly": 1, "hale": 1})
}

# Step 2: Apply semantic rules
exclusions = {
    ("physique", "broad"): {
        "health": ["sickly"]  # Strong physique excludes sickness
    }
}
chosen = apply_exclusion_rules(chosen, exclusions)
```

### Pattern 3: Full Generation Pipeline

```python
import random
from condition_axis._base import weighted_choice, apply_exclusion_rules, values_to_prompt

def generate_simple_character(seed=None):
    """Example generation function using all three utilities."""
    if seed is not None:
        random.seed(seed)

    # Step 1: Select axes
    chosen = {}

    # Step 2: Generate values
    chosen["physique"] = weighted_choice(
        ["skinny", "wiry", "broad"],
        {"skinny": 1.0, "wiry": 2.0, "broad": 1.5}
    )
    chosen["wealth"] = weighted_choice(
        ["poor", "modest", "wealthy"],
        {"poor": 4.0, "modest": 3.0, "wealthy": 1.0}
    )

    # Step 3: Apply exclusions
    exclusions = {
        ("wealth", "wealthy"): {
            "physique": ["skinny"]  # Wealth enables nutrition
        }
    }
    chosen = apply_exclusion_rules(chosen, exclusions)

    # Step 4: Serialize
    return chosen, values_to_prompt(chosen)

# Usage
character, prompt = generate_simple_character(seed=42)
print(f"State: {character}")
print(f"Prompt: {prompt}")
# State: {'physique': 'wiry', 'wealth': 'poor'}
# Prompt: 'wiry, poor'
```

---

## Thread Safety

All functions in this module are thread-safe with the following considerations:

- **`weighted_choice()`**: Uses Python's thread-local RNG (`random` module)
- **`apply_exclusion_rules()`**: Pure function, but modifies input in-place (caller must ensure exclusive access)
- **`values_to_prompt()`**: Pure function, fully thread-safe

For concurrent generation, use separate `random.Random()` instances per thread or use process-based parallelism.

---

## Performance Considerations

### `weighted_choice()`

- **Uniform path**: O(1) - single call to `random.choice()`
- **Weighted path**: O(n) - builds weight list, calls `random.choices()`
- Use uniform distribution when weights are not needed

### `apply_exclusion_rules()`

- **Complexity**: O(r × a) where r = number of rules, a = average blocked axes per rule
- **In-place**: Avoids dict copying overhead
- Negligible cost for typical rule counts (<20)

### `values_to_prompt()`

- **Complexity**: O(n) where n = number of axes
- String join operation, very fast
- No allocations beyond result string

---

## Testing Recommendations

### Test weighted_choice() determinism

```python
import random
from condition_axis._base import weighted_choice

def test_weighted_choice_reproducible():
    random.seed(42)
    result1 = weighted_choice(["a", "b", "c"], {"a": 1.0, "b": 2.0})

    random.seed(42)
    result2 = weighted_choice(["a", "b", "c"], {"a": 1.0, "b": 2.0})

    assert result1 == result2
```

### Test exclusion application

```python
from condition_axis._base import apply_exclusion_rules

def test_exclusion_removes_conflict():
    chosen = {"wealth": "decadent", "health": "sickly"}
    exclusions = {("wealth", "decadent"): {"health": ["sickly"]}}

    result = apply_exclusion_rules(chosen, exclusions)

    assert "health" not in result
    assert result["wealth"] == "decadent"
```

### Test prompt serialization

```python
from condition_axis._base import values_to_prompt

def test_prompt_order():
    # Dict insertion order is guaranteed in Python 3.7+
    condition = {"a": "first", "b": "second", "c": "third"}
    prompt = values_to_prompt(condition)

    assert prompt == "first, second, third"
```

---

## Version History

- **v1.0.0**: Initial stable release
  - Core utilities for all condition axis generators
  - Python 3.12+ type hints
  - Comprehensive docstrings

---

## See Also

- [Character Conditions API](./character_conditions.md) - Physical and social states
- [Occupation Axis API](./occupation_axis.md) - Occupation characteristics
