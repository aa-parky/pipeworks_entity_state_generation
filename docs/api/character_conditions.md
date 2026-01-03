# `character_conditions` - Character Physical & Social State Generation

**Module**: `condition_axis.character_conditions`

**Purpose**: Generate coherent character state descriptions across physical and social dimensions.

This module implements a structured, rule-based system for generating character states using weighted probability distributions, semantic exclusion rules, and mandatory/optional axis policies. It's designed for procedural character generation in both visual (AI image prompts) and narrative (MUD/game) contexts.

---

## Overview

The character conditions system generates state descriptions across five axes:

1. **Physique** - Body structure and build
2. **Wealth** - Economic and social status
3. **Health** - Physical condition
4. **Demeanor** - Behavioral presentation
5. **Age** - Life stage

Unlike simple random selection or text file lookups, this system:
- Uses **weighted probability** for realistic populations
- Enforces **semantic coherence** through exclusion rules
- Distinguishes **mandatory** vs **optional** axes
- Provides **reproducible generation** via seeds

---

## Quick Start

```python
from condition_axis import generate_condition, condition_to_prompt

# Generate a character state
character = generate_condition(seed=42)
print(character)
# {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'}

# Convert to prompt format
prompt = condition_to_prompt(character)
print(prompt)
# 'wiry, poor, weary'

# Use in image generation
full_prompt = f"illustration of a goblin, {prompt}, weathered face"
```

---

## Architecture

The system operates in three phases:

### Phase 1: Mandatory Axes Selection
Always includes **physique** and **wealth** to establish baseline character state.

### Phase 2: Optional Axes Selection
Randomly includes 0-2 axes from **health**, **demeanor**, **age** to add narrative detail without prompt dilution.

### Phase 3: Semantic Exclusions
Removes illogical combinations (e.g., wealthy + frail, ancient + timid).

---

## Axis Definitions

### `CONDITION_AXES`

Dictionary defining all possible values for each axis.

**Type**: `dict[str, list[str]]`

**Structure**:
```python
CONDITION_AXES = {
    "physique": ["skinny", "wiry", "stocky", "hunched", "frail", "broad"],
    "wealth": ["poor", "modest", "well-kept", "wealthy", "decadent"],
    "health": ["sickly", "scarred", "weary", "hale", "limping"],
    "demeanor": ["timid", "suspicious", "resentful", "alert", "proud"],
    "age": ["young", "middle-aged", "old", "ancient"],
    "facial_signal": ["understated", "pronounced", "exaggerated", "asymmetrical",
                      "weathered", "soft-featured", "sharp-featured"]
}
```

#### Axis Details

##### `physique` - Body Structure
Physical build and appearance.

| Value | Description | Relative Frequency |
|-------|-------------|--------------------|
| `skinny` | Thin, undernourished | Common (3.0) |
| `wiry` | Lean but strong | Moderate (2.0) |
| `stocky` | Compact, sturdy | Uncommon (1.0) |
| `hunched` | Bent, poor posture | Moderate (2.0) |
| `frail` | Weak, delicate | Uncommon (1.0) |
| `broad` | Wide, powerful | Rare (0.5) |

**Design Notes**:
- Skewed toward survival builds (skinny, wiry, hunched)
- "Broad" is rare (requires resources to develop/maintain)
- Frail is uncommon but possible (age, illness, hardship)

##### `wealth` - Economic Status
Social and economic standing.

| Value | Description | Relative Frequency |
|-------|-------------|--------------------|
| `poor` | Destitute, struggling | Very Common (4.0) |
| `modest` | Working class, stable | Common (3.0) |
| `well-kept` | Middle class, comfortable | Moderate (2.0) |
| `wealthy` | Upper class, affluent | Uncommon (1.0) |
| `decadent` | Extremely wealthy, ostentatious | Rare (0.5) |

**Design Notes**:
- Realistic socioeconomic distribution (most are poor/modest)
- Wealth is mandatory axis (always visible in presentation)
- Influences exclusions (wealth enables healthcare, nutrition)

##### `health` - Physical Condition
Current physical state and wellness.

| Value | Description | Frequency |
|-------|-------------|-----------|
| `sickly` | Ill, unwell | Uniform |
| `scarred` | Marked by injury | Uniform |
| `weary` | Tired, worn down | Uniform |
| `hale` | Healthy, vigorous | Uniform |
| `limping` | Injured, impaired movement | Uniform |

**Design Notes**:
- Optional axis (may or may not appear)
- Uniform distribution (no inherent bias)
- Subject to exclusions (wealth/physique can prevent sickness)

##### `demeanor` - Behavioral Presentation
Outward attitude and manner.

| Value | Description | Frequency |
|-------|-------------|-----------|
| `timid` | Fearful, hesitant | Uniform |
| `suspicious` | Distrustful, wary | Uniform |
| `resentful` | Bitter, angry | Uniform |
| `alert` | Watchful, attentive | Uniform |
| `proud` | Confident, dignified | Uniform |

**Design Notes**:
- Optional axis (adds personality detail)
- Uniform distribution (no psychological bias)
- Subject to exclusions (age can prevent timidity)

##### `age` - Life Stage
Character's position in life cycle.

| Value | Description | Frequency |
|-------|-------------|-----------|
| `young` | Early adulthood | Uniform |
| `middle-aged` | Prime of life | Uniform |
| `old` | Advanced years | Uniform |
| `ancient` | Extremely old | Uniform |

**Design Notes**:
- Optional axis (narrative flavor)
- Uniform distribution (no demographic modeling)
- Triggers exclusions (ancient excludes timidity)

##### `facial_signal` - Facial Perception Modifiers
Perception modifiers that bias how a character's face is interpreted (merged from facial_conditions in v1.1.0).

| Value | Description | Relative Frequency |
|-------|-------------|--------------------|
| `understated` | Reduces feature prominence; subtle, unremarkable | Common (3.0) |
| `soft-featured` | Rounded interpretation; gentle, approachable | Fairly Common (2.5) |
| `pronounced` | Strong features; distinctive, memorable | Moderate (2.0) |
| `sharp-featured` | Angular interpretation; defined, striking | Moderate (2.0) |
| `weathered` | Wear/age texture; experienced, hardship | Less Common (1.5) |
| `asymmetrical` | Irregular features; unique character | Uncommon (1.0) |
| `exaggerated` | Extreme features; caricature-like | Rare (0.5) |

**Design Notes**:
- **Optional axis** (may or may not appear, part of the 0-2 optional axes pool)
- **Perception modifiers, not anatomy**: Signals bias interpretation rather than prescribing specific features
- **Species-agnostic**: "weathered" works for goblins, humans, elves, etc.
- **Weighted toward subtle signals**: Most faces aren't remarkable (understated, soft-featured are most common)
- **Cross-system exclusions**: Prevented combinations with age, health, and wealth axes (see EXCLUSIONS)

**Signal Meanings**:
- `understated` → Features blend harmoniously, unremarkable
- `soft-featured` → Rounded contours, gentle impression
- `pronounced` → Strong bone structure, clearly defined
- `sharp-featured` → Angular lines, aristocratic or severe
- `weathered` → Lines and texture from time/hardship
- `asymmetrical` → Uneven features adding character
- `exaggerated` → Striking, almost caricatured proportions

**Integration Note** (v1.1.0):
Prior to v1.1.0, facial signals were a separate `facial_conditions` module. They are now integrated into `character_conditions` with cross-system exclusion rules to maintain coherence with other character axes.

---

## Configuration Constants

### `AXIS_POLICY`

Controls which axes are mandatory vs. optional and limits complexity.

**Type**: `dict[str, Any]`

**Structure**:
```python
AXIS_POLICY = {
    "mandatory": ["physique", "wealth"],
    "optional": ["health", "demeanor", "age", "facial_signal"],
    "max_optional": 2
}
```

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `mandatory` | `list[str]` | Axes always included (baseline state) |
| `optional` | `list[str]` | Axes conditionally included (narrative detail) |
| `max_optional` | `int` | Maximum number of optional axes (prevents prompt dilution) |

**Design Rationale**:

**Why physique and wealth are mandatory:**
- These are immediately visible in character presentation
- Establish baseline for interpretation of other traits
- Provide minimum viable character description

**Why health/demeanor/age/facial_signal are optional:**
- Add nuance without overwhelming the prompt
- Not always relevant to the scene
- Keep diffusion models focused on core attributes
- Facial signals provide perception modifiers when relevant

**Why max_optional = 2:**
- Prevents "Christmas tree" effect (too many adjectives)
- Maintains clarity for image generation
- Forces prioritization of narrative detail

---

### `WEIGHTS`

Probability distributions for realistic population modeling.

**Type**: `dict[str, dict[str, float]]`

**Structure**:
```python
WEIGHTS = {
    "wealth": {
        "poor": 4.0,
        "modest": 3.0,
        "well-kept": 2.0,
        "wealthy": 1.0,
        "decadent": 0.5
    },
    "physique": {
        "skinny": 3.0,
        "wiry": 2.0,
        "hunched": 2.0,
        "frail": 1.0,
        "stocky": 1.0,
        "broad": 0.5
    },
    "facial_signal": {
        "understated": 3.0,
        "soft-featured": 2.5,
        "pronounced": 2.0,
        "sharp-featured": 2.0,
        "weathered": 1.5,
        "asymmetrical": 1.0,
        "exaggerated": 0.5
    }
}
```

**Interpretation**:
- Higher weight = more frequent occurrence
- Weights are relative (doubled values double frequency)
- Missing axes use uniform distribution (all values equally likely)

**Examples**:

```python
# Wealth distribution
# poor: 40% (4.0 / 10.5)
# modest: 28.6% (3.0 / 10.5)
# well-kept: 19% (2.0 / 10.5)
# wealthy: 9.5% (1.0 / 10.5)
# decadent: 4.8% (0.5 / 10.5)

# Physique distribution
# skinny: 31.6% (3.0 / 9.5)
# wiry: 21.1% (2.0 / 9.5)
# hunched: 21.1% (2.0 / 9.5)
# frail: 10.5% (1.0 / 9.5)
# stocky: 10.5% (1.0 / 9.5)
# broad: 5.3% (0.5 / 9.5)
```

**Design Philosophy**:
- Wealth heavily skewed (realistic socioeconomics)
- Physique moderately skewed (survival builds more common)
- Facial signals weighted toward subtle (most faces aren't remarkable)
- Health/demeanor/age uniform (no inherent bias)

---

### `EXCLUSIONS`

Semantic coherence rules that prevent illogical combinations.

**Type**: `dict[tuple[str, str], dict[str, list[str]]]`

**Structure**:
```python
EXCLUSIONS = {
    ("wealth", "decadent"): {
        "physique": ["frail"],
        "health": ["sickly"],
        "facial_signal": ["weathered"]
    },
    ("age", "ancient"): {
        "demeanor": ["timid"],
        "facial_signal": ["understated"]
    },
    ("age", "young"): {
        "facial_signal": ["weathered"]
    },
    ("physique", "broad"): {
        "health": ["sickly"]
    },
    ("health", "hale"): {
        "physique": ["frail"],
        "facial_signal": ["weathered"]
    },
    ("health", "sickly"): {
        "facial_signal": ["soft-featured"]
    }
}
```

**Format**: `{(trigger_axis, trigger_value): {blocked_axis: [blocked_values]}}`

**Rules Explained**:

#### Rule 1: Wealth enables healthcare
```python
("wealth", "decadent"): {
    "physique": ["frail"],
    "health": ["sickly"]
}
```
**Rationale**: Extremely wealthy characters have access to nutrition, medicine, and care that prevent frailty and sickness.

**Effect**: If a character is generated as `wealth=decadent`, any `physique=frail` or `health=sickly` will be removed.

#### Rule 2: Age brings confidence
```python
("age", "ancient"): {
    "demeanor": ["timid"]
}
```
**Rationale**: Characters who have lived to extreme age have accumulated experience and confidence. Timidity is inconsistent with survival to ancient age.

**Effect**: If `age=ancient`, any `demeanor=timid` is removed.

#### Rule 3: Strength prevents sickness
```python
("physique", "broad"): {
    "health": ["sickly"]
}
```
**Rationale**: Broad, powerful physiques indicate robust constitution that resists illness.

**Effect**: If `physique=broad`, any `health=sickly` is removed.

#### Rule 4: Health requires constitution
```python
("health", "hale"): {
    "physique": ["frail"]
}
```
**Rationale**: Being hale (healthy and vigorous) is incompatible with frail physique.

**Effect**: If `health=hale`, any `physique=frail` is removed.

#### Rule 5: Youth contradicts weathering (v1.1.0+)
```python
("age", "young"): {
    "facial_signal": ["weathered"]
}
```
**Rationale**: Young characters have not lived long enough to develop the lines, texture, and wear associated with "weathered" faces.

**Effect**: If `age=young`, any `facial_signal=weathered` is removed.

#### Rule 6: Ancient age is rarely subtle (v1.1.0+)
```python
("age", "ancient"): {
    "demeanor": ["timid"],
    "facial_signal": ["understated"]
}
```
**Rationale**: Extreme age leaves visible marks. Ancient faces are rarely unremarkable or understated.

**Effect**: If `age=ancient`, any `facial_signal=understated` is removed (in addition to `demeanor=timid`).

#### Rule 7: Wealth preserves appearance (v1.1.0+)
```python
("wealth", "decadent"): {
    "physique": ["frail"],
    "health": ["sickly"],
    "facial_signal": ["weathered"]
}
```
**Rationale**: Extreme wealth provides access to healthcare, nutrition, and cosmetic care that preserves appearance and prevents weathering.

**Effect**: If `wealth=decadent`, any `facial_signal=weathered` is removed (in addition to existing exclusions).

#### Rule 8: Health shows in appearance (v1.1.0+)
```python
("health", "hale"): {
    "physique": ["frail"],
    "facial_signal": ["weathered"]
}
```
**Rationale**: Hale characters are healthy and vigorous, which prevents weathered appearance.

**Effect**: If `health=hale`, any `facial_signal=weathered` is removed.

#### Rule 9: Sickness contradicts softness (v1.1.0+)
```python
("health", "sickly"): {
    "facial_signal": ["soft-featured"]
}
```
**Rationale**: Sickness typically gaunt or drawn appearance, which contradicts soft, rounded features.

**Effect**: If `health=sickly`, any `facial_signal=soft-featured` is removed.

**Design Philosophy**:
- Exclusions happen **after** generation (transparent, debuggable)
- Rules encode domain knowledge (not arbitrary)
- Allow rare edge cases (scarred + wealthy is valid)
- Balance coherence with variety

---

## Functions

### `generate_condition()`

Generate a coherent character condition using the full rule system.

#### Signature

```python
def generate_condition(seed: int | None = None) -> dict[str, str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seed` | `int \| None` | **Optional.** Random seed for reproducible generation. If `None`, uses system entropy (non-reproducible). |

#### Returns

| Type | Description |
|------|-------------|
| `dict[str, str]` | Dictionary mapping axis names to selected values. Keys are axis names from `CONDITION_AXES`. Values are the selected condition values. |

#### Generation Process

1. **Seed RNG** (if seed provided)
2. **Select mandatory axes** (physique, wealth)
3. **Select 0-2 optional axes** (randomly chosen from health, demeanor, age)
4. **Apply weighted selection** for each chosen axis
5. **Apply exclusion rules** to remove conflicts
6. **Return structured dict**

#### Examples

**Reproducible generation**
```python
from condition_axis import generate_condition

# Same seed = same result
cond1 = generate_condition(seed=42)
cond2 = generate_condition(seed=42)
assert cond1 == cond2  # True

print(cond1)
# {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'}
```

**Non-reproducible generation**
```python
# Different each time
char1 = generate_condition()
char2 = generate_condition()
# Results will differ

print(char1)
# {'physique': 'stocky', 'wealth': 'modest', 'demeanor': 'alert'}

print(char2)
# {'physique': 'skinny', 'wealth': 'poor', 'age': 'old', 'health': 'scarred'}
```

**Batch generation**
```python
# Generate a population
population = [generate_condition(seed=i) for i in range(100)]

# Count wealth distribution
from collections import Counter
wealth_counts = Counter(char['wealth'] for char in population)
print(wealth_counts)
# Counter({'poor': 39, 'modest': 28, 'well-kept': 19, 'wealthy': 10, 'decadent': 4})
# Reflects 4.0:3.0:2.0:1.0:0.5 weight ratio
```

**Observing exclusions**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Generate many characters
for i in range(1000):
    char = generate_condition(seed=i)

    # Check for excluded combinations
    if char.get('wealth') == 'decadent' and char.get('health') == 'sickly':
        print("Found excluded combination!")
        break
else:
    print("No excluded combinations found (as expected)")
# Output: "No excluded combinations found (as expected)"
```

#### Return Value Structure

The returned dictionary always includes:
- **physique** (mandatory)
- **wealth** (mandatory)

And may include 0-2 of:
- **health** (optional)
- **demeanor** (optional)
- **age** (optional)

**Minimum return**: `{"physique": "...", "wealth": "..."}`
**Maximum return**: `{"physique": "...", "wealth": "...", "health": "...", "demeanor": "..."}`
(or any 2 optional axes)

#### Performance

- **Complexity**: O(1) average case (fixed number of axes)
- **Seed setting**: Negligible overhead
- **Typical time**: < 1ms per generation
- **Thread safety**: Not thread-safe (uses global `random` module)

#### Common Patterns

**Pattern 1: Reproducible test data**
```python
def test_character_generation():
    char = generate_condition(seed=42)
    assert char['physique'] == 'wiry'
    assert char['wealth'] == 'poor'
```

**Pattern 2: Generate until condition met**
```python
# Generate until we get a wealthy character
while True:
    char = generate_condition()
    if char['wealth'] in ['wealthy', 'decadent']:
        break

print(f"Found wealthy character: {char}")
```

**Pattern 3: Population statistics**
```python
population = [generate_condition(seed=i) for i in range(10000)]

# Calculate physique distribution
physiques = [c['physique'] for c in population]
distribution = {p: physiques.count(p) / len(physiques)
                for p in set(physiques)}
print(distribution)
# Matches WEIGHTS distribution
```

---

### `condition_to_prompt()`

Convert structured condition data to a comma-separated prompt fragment.

This is the canonical serialization format for character conditions, designed for diffusion models and narrative text.

#### Signature

```python
def condition_to_prompt(condition_dict: dict[str, str]) -> str
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `condition_dict` | `dict[str, str]` | **Required.** Dictionary mapping axis names to values (output from `generate_condition()`) |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Comma-separated string of condition values. Order follows dict insertion order. Empty dict returns empty string. |

#### Examples

**Basic usage**
```python
from condition_axis import generate_condition, condition_to_prompt

char = generate_condition(seed=42)
prompt = condition_to_prompt(char)
print(prompt)
# 'wiry, poor, weary'
```

**Image generation**
```python
char = generate_condition(seed=123)
char_prompt = condition_to_prompt(char)

full_prompt = f"portrait of a goblin, {char_prompt}, fantasy art"
print(full_prompt)
# 'portrait of a goblin, skinny, poor, limping, alert, fantasy art'
```

**Multiple characters**
```python
characters = [generate_condition(seed=i) for i in range(3)]
prompts = [condition_to_prompt(c) for c in characters]

for i, prompt in enumerate(prompts):
    print(f"Character {i+1}: {prompt}")
# Character 1: wiry, poor, weary
# Character 2: skinny, modest, scarred, suspicious
# Character 3: hunched, poor, old
```

**Combining with other systems**
```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    condition_to_prompt,
    facial_condition_to_prompt
)

char = generate_condition(seed=42)
face = generate_facial_condition(seed=42)

combined = f"{condition_to_prompt(char)}, {facial_condition_to_prompt(face)}"
print(combined)
# 'wiry, poor, weary, weathered'
```

#### Design Notes

- **Values only** (not keys) for cleaner prompts
- **Comma-separated** for diffusion model compatibility
- **Deterministic order** (follows generation order)
- **No axis names** (values are semantically clear)

---

### `get_available_axes()`

Get list of all defined condition axes.

Useful for introspection, validation, and UI generation.

#### Signature

```python
def get_available_axes() -> list[str]
```

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List of axis names (e.g., `['physique', 'wealth', 'health', 'demeanor', 'age', 'facial_signal']`) |

#### Examples

**List all axes**
```python
from condition_axis import get_available_axes

axes = get_available_axes()
print(axes)
# ['physique', 'wealth', 'health', 'demeanor', 'age', 'facial_signal']
```

**Build UI selector**
```python
axes = get_available_axes()
for axis in axes:
    print(f"<select name='{axis}'>")
    values = get_axis_values(axis)
    for value in values:
        print(f"  <option>{value}</option>")
    print("</select>")
```

**Validate custom conditions**
```python
def validate_condition(cond: dict) -> bool:
    """Check if condition uses valid axes."""
    valid_axes = set(get_available_axes())
    return all(axis in valid_axes for axis in cond.keys())

# Valid
assert validate_condition({'physique': 'wiry', 'wealth': 'poor'})

# Invalid
assert not validate_condition({'strength': 'high'})  # 'strength' not defined
```

---

### `get_axis_values()`

Get all possible values for a specific axis.

#### Signature

```python
def get_axis_values(axis: str) -> list[str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `axis` | `str` | **Required.** Name of the axis (e.g., `'physique'`, `'wealth'`) |

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List of possible values for that axis |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `KeyError` | If `axis` is not defined in `CONDITION_AXES` |

#### Examples

**Get values for an axis**
```python
from condition_axis import get_axis_values

wealth_values = get_axis_values('wealth')
print(wealth_values)
# ['poor', 'modest', 'well-kept', 'wealthy', 'decadent']

physique_values = get_axis_values('physique')
print(physique_values)
# ['skinny', 'wiry', 'stocky', 'hunched', 'frail', 'broad']
```

**Build dropdown UI**
```python
from condition_axis import get_available_axes, get_axis_values

for axis in get_available_axes():
    print(f"{axis.title()}:")
    for value in get_axis_values(axis):
        print(f"  - {value}")
    print()
# Physique:
#   - skinny
#   - wiry
#   - stocky
#   ...
```

**Validate value is in axis**
```python
def is_valid_value(axis: str, value: str) -> bool:
    """Check if value is valid for the given axis."""
    try:
        return value in get_axis_values(axis)
    except KeyError:
        return False

assert is_valid_value('wealth', 'poor')  # True
assert not is_valid_value('wealth', 'rich')  # False ('rich' not defined)
assert not is_valid_value('strength', 'high')  # False ('strength' axis not defined)
```

**Error handling**
```python
try:
    values = get_axis_values('invalid_axis')
except KeyError as e:
    print(f"Axis not found: {e}")
# Output: Axis not found: 'invalid_axis'
```

---

## Module Exports

```python
__all__ = [
    "AXIS_POLICY",
    "CONDITION_AXES",
    "EXCLUSIONS",
    "WEIGHTS",
    "condition_to_prompt",
    "generate_condition",
    "get_available_axes",
    "get_axis_values",
]
```

### Exported Constants
- `CONDITION_AXES` - Axis definitions
- `AXIS_POLICY` - Mandatory/optional rules
- `WEIGHTS` - Probability distributions
- `EXCLUSIONS` - Semantic rules

### Exported Functions
- `generate_condition()` - Main generation function
- `condition_to_prompt()` - Serialization
- `get_available_axes()` - Introspection
- `get_axis_values()` - Introspection

---

## Advanced Usage

### Custom Weights

You can modify weights at runtime for specialized populations:

```python
from condition_axis import character_conditions

# Save original
original_weights = character_conditions.WEIGHTS.copy()

# Modify for wealthy population
character_conditions.WEIGHTS['wealth'] = {
    'poor': 1.0,
    'modest': 2.0,
    'well-kept': 3.0,
    'wealthy': 4.0,
    'decadent': 2.0
}

# Generate wealthy characters
char = character_conditions.generate_condition()

# Restore original
character_conditions.WEIGHTS = original_weights
```

**Warning**: Modifying module-level constants affects all subsequent generations. Consider creating a custom generator function instead.

### Custom Exclusions

Add temporary exclusions for specific scenarios:

```python
from condition_axis import character_conditions

# Save original
original_exclusions = character_conditions.EXCLUSIONS.copy()

# Add temporary rule: young characters can't be weary
character_conditions.EXCLUSIONS[('age', 'young')] = {
    'health': ['weary']
}

char = character_conditions.generate_condition()

# Restore
character_conditions.EXCLUSIONS = original_exclusions
```

### Filtering Results

Generate characters matching specific criteria:

```python
from condition_axis import generate_condition

def generate_with_criteria(criteria: dict, max_attempts: int = 100):
    """Generate character matching specific criteria."""
    for _ in range(max_attempts):
        char = generate_condition()
        if all(char.get(k) == v for k, v in criteria.items()):
            return char
    raise ValueError(f"Could not generate character matching {criteria}")

# Generate a wealthy, broad character
char = generate_with_criteria({'wealth': 'wealthy', 'physique': 'broad'})
print(char)
```

### Population Statistics

Analyze generation patterns:

```python
from condition_axis import generate_condition
from collections import Counter

def analyze_population(size: int = 10000):
    """Analyze distribution of generated characters."""
    population = [generate_condition(seed=i) for i in range(size)]

    # Wealth distribution
    wealth = Counter(c['wealth'] for c in population)
    print("Wealth distribution:")
    for value, count in wealth.most_common():
        pct = count / size * 100
        print(f"  {value:12} {count:5} ({pct:5.2f}%)")

    # Optional axis frequency
    has_health = sum(1 for c in population if 'health' in c)
    has_demeanor = sum(1 for c in population if 'demeanor' in c)
    has_age = sum(1 for c in population if 'age' in c)

    print(f"\nOptional axis frequency:")
    print(f"  health:   {has_health/size*100:.1f}%")
    print(f"  demeanor: {has_demeanor/size*100:.1f}%")
    print(f"  age:      {has_age/size*100:.1f}%")

analyze_population()
```

---

## Testing Recommendations

### Test Reproducibility

```python
def test_reproducibility():
    """Same seed produces same result."""
    char1 = generate_condition(seed=42)
    char2 = generate_condition(seed=42)
    assert char1 == char2
```

### Test Mandatory Axes

```python
def test_mandatory_axes():
    """All generated conditions include mandatory axes."""
    for i in range(100):
        char = generate_condition(seed=i)
        assert 'physique' in char
        assert 'wealth' in char
```

### Test Exclusion Rules

```python
def test_exclusions():
    """Exclusion rules prevent illogical combinations."""
    for i in range(1000):
        char = generate_condition(seed=i)

        # Test wealth=decadent excludes health=sickly
        if char.get('wealth') == 'decadent':
            assert char.get('health') != 'sickly'
            assert char.get('physique') != 'frail'

        # Test age=ancient excludes demeanor=timid
        if char.get('age') == 'ancient':
            assert char.get('demeanor') != 'timid'
```

### Test Optional Axes Count

```python
def test_optional_axes_count():
    """Optional axes count respects max_optional policy."""
    for i in range(100):
        char = generate_condition(seed=i)

        # Count optional axes present
        optional_count = sum(
            1 for axis in ['health', 'demeanor', 'age']
            if axis in char
        )

        assert 0 <= optional_count <= 2
```

### Test Prompt Serialization

```python
def test_prompt_format():
    """Prompt format is comma-separated values."""
    char = {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'}
    prompt = condition_to_prompt(char)

    assert prompt == 'wiry, poor, weary'
    assert ', ' in prompt  # Comma-space separator
    assert 'physique' not in prompt  # No axis names
```

---

## Integration Examples

### With Image Generation

```python
from condition_axis import generate_condition, condition_to_prompt

def generate_character_prompt(species: str = "goblin", seed: int | None = None):
    """Generate a complete character image prompt."""
    char = generate_condition(seed=seed)
    char_desc = condition_to_prompt(char)

    return f"portrait of a {species}, {char_desc}, fantasy art, detailed"

prompt = generate_character_prompt(seed=42)
print(prompt)
# 'portrait of a goblin, wiry, poor, weary, fantasy art, detailed'
```

### With Narrative Systems

```python
def generate_character_description(name: str, seed: int):
    """Generate narrative character description."""
    char = generate_condition(seed=seed)

    template = "{name} is a {physique} {wealth} character"

    desc = template.format(name=name, **char)

    if 'age' in char:
        desc += f", {char['age']} in years"
    if 'demeanor' in char:
        desc += f", with a {char['demeanor']} manner"

    return desc + "."

print(generate_character_description("Grax", 42))
# 'Grax is a wiry poor character, with a weary health.'
```

### With Game Systems

```python
class Character:
    def __init__(self, name: str, seed: int | None = None):
        self.name = name
        self.condition = generate_condition(seed=seed)

    def get_stat_modifier(self, stat: str) -> int:
        """Apply condition-based modifiers."""
        physique = self.condition.get('physique')
        wealth = self.condition.get('wealth')

        modifiers = {
            'strength': {
                'broad': +2, 'stocky': +1,
                'skinny': -1, 'frail': -2
            },
            'charisma': {
                'wealthy': +2, 'well-kept': +1,
                'poor': -1
            }
        }

        return modifiers.get(stat, {}).get(
            physique if stat == 'strength' else wealth,
            0
        )

char = Character("Grax", seed=42)
print(f"Strength modifier: {char.get_stat_modifier('strength')}")
```

---

## Performance Considerations

### Generation Speed
- **Average**: < 1ms per character
- **Bottleneck**: RNG calls (unavoidable)
- **Optimization**: Use batch generation with sequential seeds

### Memory Usage
- **Per character**: ~200 bytes (dict with 2-4 string entries)
- **Module constants**: ~1KB (negligible)
- **Batch generation**: Linear with population size

### Thread Safety
**Not thread-safe** - uses global `random` module state.

For concurrent generation:
```python
import random
from concurrent.futures import ThreadPoolExecutor

def generate_with_thread_local_rng(seed):
    """Thread-safe generation using Random instance."""
    rng = random.Random(seed)
    # Would need to modify generate_condition to accept rng parameter
    # Current implementation uses global random
    pass
```

**Recommendation**: Use process-based parallelism or generate serially.

---

## Version History

- **v1.0.0**: Initial stable release
  - Five-axis character generation
  - Weighted probability distributions
  - Semantic exclusion rules
  - Mandatory/optional axis policy

---

## See Also

- [Base Utilities API](./_ base.md) - Shared generation functions
- [Facial Conditions API](./facial_conditions.md) - Facial perception modifiers
- [Occupation Axis API](./occupation_axis.md) - Occupation characteristics
- [Character State Model](../design/01_character_state_model.md) - Conceptual foundation
- [Condition Axis Spec](../design/specifications/condition_axis.md) - Technical specification
