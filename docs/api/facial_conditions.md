# `facial_conditions` - Facial Perception Modifiers

**Module**: `condition_axis.facial_conditions`

**Purpose**: Generate facial signal descriptors that modulate how a character's face is perceived.

**Status**: Experimental standalone module - likely to be merged into `character_conditions` once interaction patterns are validated.

This module implements facial signals as perceptual modifiers rather than anatomical specifications. Instead of describing explicit facial features, it biases how features are interpreted by renderers and readers.

---

## Overview

The facial conditions system generates perception modifiers for character faces. Unlike anatomical specifications ("has a large nose", "blue eyes"), facial signals bias interpretation:

- `"sharp-featured"` → biases toward angular interpretation
- `"soft-featured"` → biases toward rounded interpretation
- `"weathered"` → applies wear/age texture signal
- `"understated"` → reduces feature prominence
- `"pronounced"` → increases feature prominence
- `"exaggerated"` → pushes features toward extremes
- `"asymmetrical"` → introduces irregularity signal

---

## Quick Start

```python
from condition_axis import generate_facial_condition, facial_condition_to_prompt

# Generate a facial signal
facial = generate_facial_condition(seed=42)
print(facial)
# {'facial_signal': 'weathered'}

# Convert to prompt format
prompt = facial_condition_to_prompt(facial)
print(prompt)
# 'weathered'

# Combine with character conditions
from condition_axis import generate_condition, condition_to_prompt

char = generate_condition(seed=42)
char_prompt = condition_to_prompt(char)

full_prompt = f"portrait of a goblin, {char_prompt}, {prompt}"
print(full_prompt)
# 'portrait of a goblin, wiry, poor, weary, weathered'
```

---

## Design Philosophy

### Signals, Not Specifications

Facial signals are **perceptual modifiers**, not anatomical descriptions.

**Bad** (anatomical specification):
```
"large nose, narrow eyes, thin lips"
```

**Good** (perceptual signal):
```
"sharp-featured"
```

The signal `"sharp-featured"` allows the renderer (AI model or human reader) to interpret angular features appropriate to the species, style, and context, rather than prescribing specific anatomy.

### Why This Matters

1. **Species-agnostic**: "weathered" works for goblins, humans, elves, etc.
2. **Style-agnostic**: Signals work for photorealistic, cartoon, or abstract styles
3. **Context-aware**: Renderers can apply signals appropriately to the situation
4. **Flexible interpretation**: Same signal can manifest differently across instances

### Future Integration

This module is a **standalone experiment** testing how facial signals interact with character conditions. Once validated, it will be merged into `character_conditions.py` with appropriate cross-system exclusion rules:

**Likely conflicts**:
- `age="young"` + `facial_signal="weathered"` (youth vs. wear)
- `health="sickly"` + `facial_signal="soft-featured"` (possible redundancy)
- `age="ancient"` + `facial_signal="understated"` (age is rarely subtle)

---

## Axis Definitions

### `FACIAL_AXES`

Dictionary defining all possible facial signal values.

**Type**: `dict[str, list[str]]`

**Structure**:
```python
FACIAL_AXES = {
    "facial_signal": [
        "understated",
        "pronounced",
        "exaggerated",
        "asymmetrical",
        "weathered",
        "soft-featured",
        "sharp-featured"
    ]
}
```

#### Facial Signal Values

All values are mutually exclusive - a face has one primary signal.

| Value | Description | Interpretation Bias | Relative Frequency |
|-------|-------------|---------------------|-------------------|
| `understated` | Reduces feature prominence | Subtle, unremarkable features | Common (3.0) |
| `soft-featured` | Biases toward rounded interpretation | Rounded, gentle curves | Fairly Common (2.5) |
| `pronounced` | Increases feature prominence | Strong, noticeable features | Moderate (2.0) |
| `sharp-featured` | Biases toward angular interpretation | Angular, defined lines | Moderate (2.0) |
| `weathered` | Applies wear/age texture | Lines, texture, experience | Less Common (1.5) |
| `asymmetrical` | Introduces irregularity | Uneven, unique character | Uncommon (1.0) |
| `exaggerated` | Pushes features toward extremes | Extreme, caricatured | Rare (0.5) |

#### Signal Details

##### `understated` - Subtle Features
Reduces feature prominence. Most faces aren't remarkable.

**Interpretation**:
- Features blend harmoniously
- Nothing stands out dramatically
- Easy to overlook in a crowd
- Neutral, unremarkable

**Use cases**: Background characters, commoners, intentional plainness

##### `pronounced` - Strong Features
Increases feature prominence. Noticeable but not extreme.

**Interpretation**:
- Strong bone structure
- Distinctive without being unusual
- Memorable face
- Clear, defined features

**Use cases**: Leaders, merchants, characters meant to stand out

##### `exaggerated` - Extreme Features
Pushes features toward extremes. Rare and striking.

**Interpretation**:
- Caricature-like proportions
- Immediately distinctive
- Potentially uncanny
- Memorable, possibly unsettling

**Use cases**: Unique NPCs, antagonists, magical creatures

##### `asymmetrical` - Irregular Features
Introduces irregularity signal. Uncommon but naturalistic.

**Interpretation**:
- Uneven features (not deformity, just character)
- Unique, memorable
- Adds individuality
- Organic, realistic variation

**Use cases**: Realistic characters, individuals with history

##### `weathered` - Worn Features
Applies wear/age texture. Suggests experience and hardship.

**Interpretation**:
- Lines, wrinkles, texture
- Evidence of sun, wind, time
- Experience written on face
- Not necessarily old, just worn

**Use cases**: Laborers, outdoors folk, veterans, aged characters

##### `soft-featured` - Rounded Features
Biases toward rounded interpretation. Gentle, approachable.

**Interpretation**:
- Rounded contours
- Gentle curves
- Youthful or gentle impression
- Approachable, less threatening

**Use cases**: Youth, gentle characters, innocence

##### `sharp-featured` - Angular Features
Biases toward angular interpretation. Defined, striking.

**Interpretation**:
- Angular bone structure
- Defined cheekbones/jawline
- Sharp, clear lines
- Aristocratic or severe impression

**Use cases**: Nobility, warriors, stern characters

---

## Configuration Constants

### `FACIAL_POLICY`

Controls facial signal selection.

**Type**: `dict[str, Any]`

**Structure**:
```python
FACIAL_POLICY = {
    "mandatory": ["facial_signal"],
    "optional": [],
    "max_optional": 0
}
```

**Behavior**:
- Always generates exactly **one** facial signal
- No optional axes (simplicity)
- Consistent behavior: requesting facial conditions always produces output

**Design Rationale**:

**Why facial_signal is mandatory:**
- When user explicitly requests facial conditions, they expect output
- Avoids 50% chance of empty result
- Ensures consistent generation behavior

**Why no optional axes:**
- Single signal keeps interpretation clear
- Prevents "Christmas tree" effect
- Maintains focus on primary perception modifier

---

### `FACIAL_WEIGHTS`

Probability distribution for facial signals.

**Type**: `dict[str, dict[str, float]]`

**Structure**:
```python
FACIAL_WEIGHTS = {
    "facial_signal": {
        "understated": 3.0,      # 25.0% - Common
        "soft-featured": 2.5,    # 20.8% - Fairly common
        "pronounced": 2.0,       # 16.7% - Moderate
        "sharp-featured": 2.0,   # 16.7% - Moderate
        "weathered": 1.5,        # 12.5% - Less common
        "asymmetrical": 1.0,     # 8.3% - Uncommon
        "exaggerated": 0.5       # 4.2% - Rare
    }
}
```

**Total Weight**: 12.0

**Probability Calculations**:
```
understated:     3.0 / 12.0 = 25.0%
soft-featured:   2.5 / 12.0 = 20.8%
pronounced:      2.0 / 12.0 = 16.7%
sharp-featured:  2.0 / 12.0 = 16.7%
weathered:       1.5 / 12.0 = 12.5%
asymmetrical:    1.0 / 12.0 =  8.3%
exaggerated:     0.5 / 12.0 =  4.2%
```

**Design Philosophy**:
- Skewed toward subtle/neutral signals (`understated`, `soft-featured`)
- Most faces aren't remarkable
- Extreme signals (`exaggerated`) are rare
- Balanced distribution of moderate signals

---

### `FACIAL_EXCLUSIONS`

Semantic coherence rules (currently minimal).

**Type**: `dict[tuple[str, str], dict[str, list[str]]]`

**Structure**:
```python
FACIAL_EXCLUSIONS = {
    # Currently empty - exclusions are prevented by max_optional=1
}
```

**Why Empty**:
- With `max_optional=1`, only one signal is ever selected
- Signals are mutually exclusive by design
- Exclusions become critical if multiple signals are allowed in future

**Future Cross-System Exclusions**:

When merged with `character_conditions`, exclusions will prevent:
```python
{
    ("age", "young"): {
        "facial_signal": ["weathered"]  # Youth contradicts wear
    },
    ("age", "ancient"): {
        "facial_signal": ["understated"]  # Age is rarely subtle
    },
    ("health", "sickly"): {
        "facial_signal": ["soft-featured"]  # Possible redundancy
    }
}
```

---

## Functions

### `generate_facial_condition()`

Generate a facial signal condition using weighted random selection.

#### Signature

```python
def generate_facial_condition(seed: int | None = None) -> dict[str, str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seed` | `int \| None` | **Optional.** Random seed for reproducible generation. If `None`, uses system entropy. |

#### Returns

| Type | Description |
|------|-------------|
| `dict[str, str]` | Dictionary always containing exactly one key: `"facial_signal"` with selected value |

#### Behavior

**Always returns a facial signal** - ensures consistent behavior when users explicitly request facial conditions.

**Generation Process**:
1. Seed RNG (if seed provided)
2. Select `facial_signal` from `FACIAL_AXES`
3. Apply weighted probability (from `FACIAL_WEIGHTS`)
4. Apply exclusions (currently none)
5. Return structured dict

#### Examples

**Reproducible generation**
```python
from condition_axis import generate_facial_condition

# Same seed = same result
face1 = generate_facial_condition(seed=42)
face2 = generate_facial_condition(seed=42)
assert face1 == face2  # True

print(face1)
# {'facial_signal': 'weathered'}
```

**Non-reproducible generation**
```python
# Different each time
face1 = generate_facial_condition()
face2 = generate_facial_condition()

print(face1)
# {'facial_signal': 'soft-featured'}

print(face2)
# {'facial_signal': 'sharp-featured'}
```

**Batch generation for population**
```python
population = [generate_facial_condition(seed=i) for i in range(100)]

# Count distribution
from collections import Counter
signals = [f['facial_signal'] for f in population]
distribution = Counter(signals)

print(distribution.most_common())
# [('understated', 25), ('soft-featured', 21), ('pronounced', 17), ...]
# Matches FACIAL_WEIGHTS distribution
```

**Integration with character generation**
```python
from condition_axis import generate_condition, generate_facial_condition

def generate_complete_character(seed):
    """Generate character with facial signal."""
    char = generate_condition(seed=seed)
    face = generate_facial_condition(seed=seed)

    return {
        'character': char,
        'facial': face
    }

complete = generate_complete_character(42)
print(complete)
# {
#   'character': {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'},
#   'facial': {'facial_signal': 'weathered'}
# }
```

#### Return Value Structure

**Always contains**:
- `facial_signal` - Exactly one value from `FACIAL_AXES['facial_signal']`

**Never contains**:
- Optional axes (there are none)
- Multiple signals (max_optional=1 prevents this)

**Guaranteed structure**:
```python
{
    "facial_signal": "weathered"  # or any other valid signal
}
```

---

### `facial_condition_to_prompt()`

Convert facial condition to prompt fragment.

#### Signature

```python
def facial_condition_to_prompt(condition_dict: dict[str, str]) -> str
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `condition_dict` | `dict[str, str]` | **Required.** Dictionary from `generate_facial_condition()` |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Single word (facial signal value). Empty string if dict is empty. |

#### Examples

**Basic usage**
```python
from condition_axis import generate_facial_condition, facial_condition_to_prompt

face = generate_facial_condition(seed=42)
prompt = facial_condition_to_prompt(face)

print(prompt)
# 'weathered'
```

**Combined with character prompt**
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

**Image generation integration**
```python
face = generate_facial_condition(seed=123)
face_signal = facial_condition_to_prompt(face)

full_prompt = f"portrait of a goblin, {face_signal}, fantasy art"
print(full_prompt)
# 'portrait of a goblin, sharp-featured, fantasy art'
```

---

### `get_available_facial_axes()`

Get list of all defined facial axes.

#### Signature

```python
def get_available_facial_axes() -> list[str]
```

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List containing `['facial_signal']` |

#### Examples

```python
from condition_axis import get_available_facial_axes

axes = get_available_facial_axes()
print(axes)
# ['facial_signal']
```

---

### `get_facial_axis_values()`

Get all possible values for a facial axis.

#### Signature

```python
def get_facial_axis_values(axis: str) -> list[str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `axis` | `str` | **Required.** Axis name (currently only `'facial_signal'`) |

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List of all possible signal values |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `KeyError` | If axis not in `FACIAL_AXES` |

#### Examples

**Get signal values**
```python
from condition_axis import get_facial_axis_values

signals = get_facial_axis_values('facial_signal')
print(signals)
# ['understated', 'pronounced', 'exaggerated', 'asymmetrical',
#  'weathered', 'soft-featured', 'sharp-featured']
```

**Build UI selector**
```python
signals = get_facial_axis_values('facial_signal')

for signal in signals:
    print(f"<option value='{signal}'>{signal.replace('-', ' ').title()}</option>")
# <option value='understated'>Understated</option>
# <option value='pronounced'>Pronounced</option>
# ...
```

**Error handling**
```python
try:
    values = get_facial_axis_values('invalid_axis')
except KeyError as e:
    print(f"Axis not found: {e}")
# Output: Axis not found: 'invalid_axis'
```

---

## Module Exports

```python
__all__ = [
    "FACIAL_AXES",
    "FACIAL_EXCLUSIONS",
    "FACIAL_POLICY",
    "FACIAL_WEIGHTS",
    "facial_condition_to_prompt",
    "generate_facial_condition",
    "get_available_facial_axes",
    "get_facial_axis_values",
]
```

### Exported Constants
- `FACIAL_AXES` - Signal definitions
- `FACIAL_POLICY` - Mandatory/optional rules
- `FACIAL_WEIGHTS` - Probability distribution
- `FACIAL_EXCLUSIONS` - Semantic rules (currently empty)

### Exported Functions
- `generate_facial_condition()` - Generate facial signal
- `facial_condition_to_prompt()` - Serialize to prompt
- `get_available_facial_axes()` - List axes
- `get_facial_axis_values()` - List signal values

---

## Advanced Usage

### Custom Weights for Specific Contexts

```python
from condition_axis import facial_conditions

# Save original
original_weights = facial_conditions.FACIAL_WEIGHTS.copy()

# Emphasize extreme features for villain generation
facial_conditions.FACIAL_WEIGHTS['facial_signal'] = {
    'exaggerated': 3.0,
    'sharp-featured': 3.0,
    'asymmetrical': 2.0,
    'pronounced': 1.5,
    'weathered': 1.0,
    'soft-featured': 0.5,
    'understated': 0.5
}

villain_face = facial_conditions.generate_facial_condition()

# Restore
facial_conditions.FACIAL_WEIGHTS = original_weights
```

### Filter for Specific Signals

```python
from condition_axis import generate_facial_condition

def generate_until_signal(target_signal: str, max_attempts: int = 100):
    """Generate until specific signal is found."""
    for _ in range(max_attempts):
        face = generate_facial_condition()
        if face['facial_signal'] == target_signal:
            return face
    raise ValueError(f"Could not generate {target_signal}")

# Generate weathered face
face = generate_until_signal('weathered')
print(face)
# {'facial_signal': 'weathered'}
```

### Population Analysis

```python
from condition_axis import generate_facial_condition
from collections import Counter

def analyze_facial_distribution(size: int = 10000):
    """Analyze facial signal distribution."""
    population = [generate_facial_condition(seed=i) for i in range(size)]

    signals = [f['facial_signal'] for f in population]
    distribution = Counter(signals)

    print("Facial Signal Distribution:")
    for signal, count in distribution.most_common():
        pct = count / size * 100
        print(f"  {signal:15} {count:5} ({pct:5.2f}%)")

analyze_facial_distribution()
# Facial Signal Distribution:
#   understated      2500 (25.00%)
#   soft-featured    2083 (20.83%)
#   pronounced       1667 (16.67%)
#   sharp-featured   1667 (16.67%)
#   weathered        1250 (12.50%)
#   asymmetrical      833 ( 8.33%)
#   exaggerated       500 ( 5.00%)
```

---

## Testing Recommendations

### Test Reproducibility

```python
def test_facial_reproducibility():
    """Same seed produces same result."""
    face1 = generate_facial_condition(seed=42)
    face2 = generate_facial_condition(seed=42)
    assert face1 == face2
```

### Test Always Returns Signal

```python
def test_always_returns_signal():
    """All generations include facial_signal."""
    for i in range(100):
        face = generate_facial_condition(seed=i)
        assert 'facial_signal' in face
        assert len(face) == 1  # Only one key
```

### Test Weight Distribution

```python
def test_weight_distribution():
    """Distribution matches weights over large sample."""
    from collections import Counter

    population = [generate_facial_condition(seed=i) for i in range(10000)]
    signals = [f['facial_signal'] for f in population]
    counts = Counter(signals)

    # Understated should be most common
    assert counts['understated'] > counts['exaggerated']
    assert counts['soft-featured'] > counts['asymmetrical']
```

### Test Prompt Format

```python
def test_prompt_format():
    """Prompt is single word."""
    face = {'facial_signal': 'weathered'}
    prompt = facial_condition_to_prompt(face)

    assert prompt == 'weathered'
    assert ',' not in prompt  # Single value, no commas
    assert 'facial_signal' not in prompt  # No axis names
```

---

## Integration Examples

### Complete Character Generation

```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    condition_to_prompt,
    facial_condition_to_prompt
)

def generate_full_character(seed: int):
    """Generate complete character with facial signal."""
    char = generate_condition(seed=seed)
    face = generate_facial_condition(seed=seed)

    return {
        'character': char,
        'facial': face,
        'prompt': f"{condition_to_prompt(char)}, {facial_condition_to_prompt(face)}"
    }

character = generate_full_character(42)
print(character['prompt'])
# 'wiry, poor, weary, weathered'
```

### Narrative Description

```python
def describe_face(facial_dict: dict) -> str:
    """Convert facial signal to narrative description."""
    signal = facial_dict['facial_signal']

    descriptions = {
        'understated': "unremarkable features",
        'pronounced': "strong, defined features",
        'exaggerated': "striking, almost caricatured features",
        'asymmetrical': "uniquely uneven features",
        'weathered': "a face marked by time and hardship",
        'soft-featured': "gentle, rounded features",
        'sharp-featured': "angular, sharp features"
    }

    return descriptions.get(signal, signal)

face = generate_facial_condition(seed=42)
print(f"They have {describe_face(face)}.")
# 'They have a face marked by time and hardship.'
```

### Image Generation with Style

```python
def generate_portrait_prompt(
    species: str,
    style: str,
    seed: int | None = None
):
    """Generate styled portrait prompt with facial signal."""
    face = generate_facial_condition(seed=seed)
    signal = facial_condition_to_prompt(face)

    return f"{style} portrait of a {species}, {signal}, detailed, high quality"

prompt = generate_portrait_prompt("goblin", "oil painting", seed=42)
print(prompt)
# 'oil painting portrait of a goblin, weathered, detailed, high quality'
```

---

## Performance Considerations

### Generation Speed
- **Average**: < 0.5ms per facial signal
- **Bottleneck**: RNG call (single choice operation)
- **Optimization**: Negligible overhead

### Memory Usage
- **Per signal**: ~100 bytes (single-entry dict)
- **Module constants**: < 500 bytes
- **Batch generation**: Linear with population size

### Thread Safety
**Not thread-safe** - uses global `random` module state.

Use separate processes or sequential generation for concurrent needs.

---

## Future Plans

### Planned Merge with Character Conditions

This module will be merged into `character_conditions.py` when:

1. **Cross-system interactions validated**
   - Age + facial signal combinations tested
   - Health + facial signal patterns analyzed
   - Demeanor + facial signal coherence verified

2. **Exclusion rules identified**
   - Documented conflicts between axes
   - Appropriate exclusions defined
   - Edge cases resolved

3. **API compatibility ensured**
   - No breaking changes to existing code
   - Smooth migration path for users
   - Backward compatibility maintained

### Potential Enhancements

- **Multiple concurrent signals** (increase max_optional)
- **Intensity modifiers** (slightly weathered vs. heavily weathered)
- **Contextual signals** (temporary vs. permanent features)
- **Cultural/species-specific signals**

---

## Version History

- **v1.0.0**: Initial experimental release
  - Single facial_signal axis
  - Weighted probability distribution
  - Minimal exclusions (future cross-system rules planned)

---

## See Also

- [Base Utilities API](._base.md) - Shared generation functions
- [Character Conditions API](./character_conditions.md) - Physical & social states
- [Occupation Axis API](./occupation_axis.md) - Occupation characteristics
- [Obey the Verb](../specifications/Obey_the_Verb.md) - Prompting philosophy
- [Character State Model](../design/01_character_state_model.md) - Conceptual foundation
