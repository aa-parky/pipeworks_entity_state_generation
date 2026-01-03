# `occupation_axis` - Occupation Characteristics Generation

**Module**: `condition_axis.occupation_axis`

**Purpose**: Generate occupation descriptors across multiple semantic dimensions.

This module generates the contextual characteristics and social positioning of occupations, rather than simple occupation names. It characterizes how occupations relate to society through legitimacy, visibility, moral weight, dependency, and risk exposure.

---

## Overview

The occupation axis system generates characteristics across five dimensions:

1. **Legitimacy** - Legal and social acceptance
2. **Visibility** - Public conspicuousness
3. **Moral Load** - Psychological/ethical burden
4. **Dependency** - Societal necessity
5. **Risk Exposure** - Physical/psychological toll

Unlike simple occupation lookups ("blacksmith", "merchant"), this system describes **how an occupation feels to practice and how society views it**.

---

## Quick Start

```python
from condition_axis import generate_occupation_condition, occupation_condition_to_prompt

# Generate occupation characteristics
occupation = generate_occupation_condition(seed=42)
print(occupation)
# {'legitimacy': 'tolerated', 'visibility': 'discreet', 'moral_load': 'burdened'}

# Convert to prompt format
prompt = occupation_condition_to_prompt(occupation)
print(prompt)
# 'tolerated, discreet, burdened'

# Use in complete character description
full_prompt = (
    f"illustration of a goblin whose work is {prompt}, "
    f"dressed appropriately for their occupation"
)
```

---

## Design Philosophy

### Characteristics, Not Names

Occupation axes describe **how work relates to society**, not what the work is called.

**Bad** (job title):
```
"blacksmith"
```

**Good** (occupation characteristics):
```
"sanctioned, routine, neutral, necessary, straining"
```

The characteristics allow you to:
- Apply to any job title (blacksmith, software engineer, mushroom taxonomist)
- Work across cultural/species boundaries
- Focus on lived experience rather than labels
- Enable emergent occupation archetypes

### The Five Axes Explained

#### Legitimacy
How does society view this work legally and officially?

- `sanctioned` - Approved, licensed, regulated
- `tolerated` - Accepted but informal
- `questioned` - Legal but dubious
- `illicit` - Illegal or forbidden

#### Visibility
How conspicuous is this work in daily life?

- `hidden` - Deliberately concealed
- `discreet` - Low-profile, not advertised
- `routine` - Normal, unremarkable
- `conspicuous` - Highly visible, attention-drawing

#### Moral Load
What psychological/ethical burden do practitioners carry?

- `neutral` - No significant moral weight
- `burdened` - Some ethical weight
- `conflicted` - Ongoing moral struggle
- `corrosive` - Soul-destroying

#### Dependency
How essential is this work to society?

- `optional` - Luxury service
- `useful` - Beneficial but not critical
- `necessary` - Important for normal functioning
- `unavoidable` - Society cannot function without it

#### Risk Exposure
What physical/psychological toll does this work exact?

- `benign` - Safe, minimal long-term impact
- `straining` - Demanding but manageable
- `hazardous` - Significant risk of injury
- `eroding` - Gradual degradation of health/sanity

---

## Architecture

The system operates in three phases:

### Phase 1: Mandatory Axes Selection
Always includes **legitimacy** and **visibility** to establish baseline occupation profile.

### Phase 2: Optional Axes Selection
Randomly includes 0-2 axes from **moral_load**, **dependency**, **risk_exposure** to add contextual detail.

### Phase 3: Semantic Exclusions
Removes illogical combinations (e.g., illicit + conspicuous, sanctioned + hidden).

---

## Axis Definitions

### `OCCUPATION_AXES`

Dictionary defining all possible values for each axis.

**Type**: `dict[str, list[str]]`

**Structure**:
```python
OCCUPATION_AXES = {
    "legitimacy": ["sanctioned", "tolerated", "questioned", "illicit"],
    "visibility": ["hidden", "discreet", "routine", "conspicuous"],
    "moral_load": ["neutral", "burdened", "conflicted", "corrosive"],
    "dependency": ["optional", "useful", "necessary", "unavoidable"],
    "risk_exposure": ["benign", "straining", "hazardous", "eroding"]
}
```

#### Detailed Axis Reference

##### `legitimacy` - Legal/Social Acceptance

How society views the occupation legally and officially.

| Value | Description | Examples | Frequency |
|-------|-------------|----------|-----------|
| `sanctioned` | Officially approved, licensed, regulated | Licensed doctor, certified accountant, guild member | Very Common (4.0) |
| `tolerated` | Accepted but not formally regulated | Street performer, informal mechanic, unlicensed trader | Common (3.0) |
| `questioned` | Legal but socially/ethically dubious | Debt collector, bail bondsman, tabloid journalist | Less Common (1.5) |
| `illicit` | Illegal or forbidden | Smuggler, fence, unlicensed healer | Rare (0.5) |

**Design Notes**:
- Most work is legal (sanctioned/tolerated = 77.8%)
- Questioned work exists in grey areas
- Illicit work is rare but present in any society

##### `visibility` - Public Conspicuousness

How visible and public-facing the occupation is.

| Value | Description | Examples | Frequency |
|-------|-------------|----------|-----------|
| `hidden` | Deliberately concealed from public view | Spy, underground engineer, secret keeper | Uncommon (1.0) |
| `discreet` | Low-profile, not advertised | Cleaner, archivist, night-shift worker | Common (3.0) |
| `routine` | Normal, unremarkable presence | Shop clerk, postal worker, gardener | Very Common (4.0) |
| `conspicuous` | Highly visible, attention-drawing | Town crier, performer, public official | Uncommon (1.0) |

**Design Notes**:
- Most work is routine or discreet (77.8%)
- Hidden work requires secrecy
- Conspicuous work draws attention (performance, leadership)

##### `moral_load` - Psychological/Ethical Burden

The psychological or ethical weight carried by practitioners.

| Value | Description | Examples | Frequency |
|-------|-------------|----------|-----------|
| `neutral` | No significant moral weight | Data entry, gardening, basic crafts | Very Common (5.0) |
| `burdened` | Some ethical weight or moral questioning | Healthcare, law enforcement, funeral services | Less Common (2.0) |
| `conflicted` | Ongoing moral struggle or doubt | Executioner, wartime medic, repo agent | Uncommon (1.0) |
| `corrosive` | Soul-destroying, psychologically damaging | Torture interrogator, industrial slaughterhouse | Rare (0.5) |

**Design Notes**:
- Most work is morally neutral (58.8%)
- Burdened work carries responsibility
- Corrosive work damages practitioners over time

##### `dependency` - Societal Necessity

How essential the occupation is to society's functioning.

| Value | Description | Examples | Frequency |
|-------|-------------|----------|-----------|
| `optional` | Nice to have, luxury service | Jeweler, portrait artist, luxury goods | Less Common (2.0) |
| `useful` | Beneficial but not critical | Teacher, librarian, craftsperson | Common (3.0) |
| `necessary` | Important for normal functioning | Farmer, water bearer, healer | Common (3.0) |
| `unavoidable` | Society cannot function without it | Waste management, food production, infrastructure | Uncommon (1.0) |

**Design Notes**:
- Balanced between useful/necessary (66.7%)
- Unavoidable work is critical infrastructure
- Optional work serves luxury/entertainment needs

##### `risk_exposure` - Physical/Psychological Toll

The physical or psychological toll exacted over time.

| Value | Description | Examples | Frequency |
|-------|-------------|----------|-----------|
| `benign` | Safe, minimal long-term impact | Desk work, light crafts, teaching | Very Common (4.0) |
| `straining` | Demanding but manageable | Construction, mining, nursing | Common (3.0) |
| `hazardous` | Significant risk of injury/harm | Soldier, firefighter, deep-sea fisher | Less Common (1.5) |
| `eroding` | Gradual degradation of health/sanity | Toxic waste handler, trauma surgeon, executioner | Rare (0.5) |

**Design Notes**:
- Most work is safe (benign = 44.4%)
- Straining work is physically demanding
- Eroding work causes long-term damage

---

## Configuration Constants

### `OCCUPATION_POLICY`

Controls which axes are mandatory vs. optional.

**Type**: `dict[str, Any]`

**Structure**:
```python
OCCUPATION_POLICY = {
    "mandatory": ["legitimacy", "visibility"],
    "optional": ["moral_load", "dependency", "risk_exposure"],
    "max_optional": 2
}
```

**Fields**:

| Field | Type | Description |
|-------|------|-------------|
| `mandatory` | `list[str]` | Always included (baseline profile) |
| `optional` | `list[str]` | Conditionally included (contextual detail) |
| `max_optional` | `int` | Maximum optional axes (prevents complexity) |

**Design Rationale**:

**Why legitimacy and visibility are mandatory:**
- These define how occupation relates to society
- Always relevant regardless of context
- Provide minimum viable occupation description
- Foundation for other characteristics

**Why moral_load/dependency/risk_exposure are optional:**
- Add nuance without overwhelming
- Not always narratively relevant
- Keep focus on core social positioning
- Prevent prompt dilution

**Why max_optional = 2:**
- Balance detail vs. clarity
- Prevent "Christmas tree" effect
- Maintain focus for image/narrative generation
- Force prioritization of important characteristics

---

### `OCCUPATION_WEIGHTS`

Probability distributions for realistic variety.

**Type**: `dict[str, dict[str, float]]`

**Complete Structure**:
```python
OCCUPATION_WEIGHTS = {
    "legitimacy": {
        "sanctioned": 4.0,   # 44.4%
        "tolerated": 3.0,    # 33.3%
        "questioned": 1.5,   # 16.7%
        "illicit": 0.5       # 5.6%
    },
    "visibility": {
        "routine": 4.0,      # 44.4%
        "discreet": 3.0,     # 33.3%
        "hidden": 1.0,       # 11.1%
        "conspicuous": 1.0   # 11.1%
    },
    "moral_load": {
        "neutral": 5.0,      # 58.8%
        "burdened": 2.0,     # 23.5%
        "conflicted": 1.0,   # 11.8%
        "corrosive": 0.5     # 5.9%
    },
    "dependency": {
        "necessary": 3.0,    # 33.3%
        "useful": 3.0,       # 33.3%
        "optional": 2.0,     # 22.2%
        "unavoidable": 1.0   # 11.1%
    },
    "risk_exposure": {
        "benign": 4.0,       # 44.4%
        "straining": 3.0,    # 33.3%
        "hazardous": 1.5,    # 16.7%
        "eroding": 0.5       # 5.6%
    }
}
```

**Design Philosophy**:
- Legitimacy: Most work is legal
- Visibility: Most work is unremarkable
- Moral load: Most work is ethically neutral
- Dependency: Balanced useful/necessary
- Risk exposure: Most work is safe

---

### `OCCUPATION_EXCLUSIONS`

Semantic coherence rules preventing illogical combinations.

**Type**: `dict[tuple[str, str], dict[str, list[str]]]`

**Complete Rules**:
```python
OCCUPATION_EXCLUSIONS = {
    # Rule 1: Illicit work avoids conspicuous visibility
    ("legitimacy", "illicit"): {
        "visibility": ["conspicuous"]
    },

    # Rule 2: Conspicuous work excludes illicit legitimacy (bidirectional)
    ("visibility", "conspicuous"): {
        "legitimacy": ["illicit"]
    },

    # Rule 3: Sanctioned work isn't hidden
    ("legitimacy", "sanctioned"): {
        "visibility": ["hidden"]
    },

    # Rule 4: Hidden work excludes sanctioned legitimacy + unavoidable dependency
    ("visibility", "hidden"): {
        "legitimacy": ["sanctioned"],
        "dependency": ["unavoidable"]
    },

    # Rule 5: Eroding risk carries moral weight
    ("risk_exposure", "eroding"): {
        "moral_load": ["neutral"]
    },

    # Rule 6: Optional work shouldn't be eroding
    ("dependency", "optional"): {
        "risk_exposure": ["eroding"]
    }
}
```

#### Exclusion Rules Explained

##### Rule 1 & 2: Illicit work avoids visibility (bidirectional)
```python
("legitimacy", "illicit"): {"visibility": ["conspicuous"]}
("visibility", "conspicuous"): {"legitimacy": ["illicit"]}
```

**Rationale**: Criminals don't advertise illegal activities. Public-facing work must be legal.

**Effect**: Cannot have `illicit + conspicuous`

**Examples**:
- ✅ Illicit + hidden (smuggler)
- ✅ Sanctioned + conspicuous (town crier)
- ❌ Illicit + conspicuous (doesn't make sense)

##### Rule 3 & 4: Sanctioned work isn't hidden (bidirectional)
```python
("legitimacy", "sanctioned"): {"visibility": ["hidden"]}
("visibility", "hidden"): {"legitimacy": ["sanctioned"]}
```

**Rationale**: Why conceal legal, approved work? Licensed professions operate openly.

**Effect**: Cannot have `sanctioned + hidden`

**Examples**:
- ✅ Sanctioned + routine (licensed doctor)
- ✅ Tolerated + hidden (underground healer)
- ❌ Sanctioned + hidden (contradictory)

##### Rule 4b: Hidden work can't be unavoidable
```python
("visibility", "hidden"): {"dependency": ["unavoidable"]}
```

**Rationale**: Critical infrastructure must be accessible and visible.

**Effect**: Cannot have `hidden + unavoidable`

**Examples**:
- ✅ Hidden + optional (secret luxury service)
- ✅ Routine + unavoidable (public water system)
- ❌ Hidden + unavoidable (how would society access it?)

##### Rule 5: Eroding risk carries moral weight
```python
("risk_exposure", "eroding"): {"moral_load": ["neutral"]}
```

**Rationale**: Work that destroys health/sanity isn't morally neutral for practitioners.

**Effect**: Cannot have `eroding + neutral`

**Examples**:
- ✅ Eroding + corrosive (torture interrogator)
- ✅ Benign + neutral (data entry)
- ❌ Eroding + neutral (degradation has moral cost)

##### Rule 6: Optional work shouldn't be eroding
```python
("dependency", "optional"): {"risk_exposure": ["eroding"]}
```

**Rationale**: Why do soul-crushing work that's not necessary? (Conservative rule)

**Effect**: Cannot have `optional + eroding`

**Examples**:
- ✅ Optional + benign (luxury jeweler)
- ✅ Necessary + eroding (trauma surgeon)
- ❌ Optional + eroding (illogical choice)

**Note**: This rule is conservative. Some people do risky optional work (extreme sports), but in occupation context it's uncommon.

---

## Functions

### `generate_occupation_condition()`

Generate coherent occupation characteristics using the full rule system.

#### Signature

```python
def generate_occupation_condition(seed: int | None = None) -> dict[str, str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `seed` | `int \| None` | **Optional.** Random seed for reproducible generation. If `None`, uses system entropy. |

#### Returns

| Type | Description |
|------|-------------|
| `dict[str, str]` | Dictionary mapping axis names to selected values. Always includes `legitimacy` and `visibility`, plus 0-2 optional axes. |

#### Generation Process

1. **Seed RNG** (if seed provided)
2. **Select mandatory axes** (legitimacy, visibility)
3. **Select 0-2 optional axes** (randomly from moral_load, dependency, risk_exposure)
4. **Apply weighted selection** for each chosen axis
5. **Apply exclusion rules** to remove conflicts
6. **Return structured dict**

#### Examples

**Reproducible generation**
```python
from condition_axis import generate_occupation_condition

# Same seed = same result
occ1 = generate_occupation_condition(seed=42)
occ2 = generate_occupation_condition(seed=42)
assert occ1 == occ2  # True

print(occ1)
# {'legitimacy': 'tolerated', 'visibility': 'discreet', 'moral_load': 'burdened'}
```

**Non-reproducible generation**
```python
# Different each time
occ = generate_occupation_condition()
print(occ)
# {'legitimacy': 'sanctioned', 'visibility': 'routine', 'dependency': 'useful'}
```

**Batch generation for occupations**
```python
occupations = [generate_occupation_condition(seed=i) for i in range(10)]

for i, occ in enumerate(occupations):
    prompt = occupation_condition_to_prompt(occ)
    print(f"Occupation {i+1}: {prompt}")
# Occupation 1: tolerated, discreet, burdened
# Occupation 2: sanctioned, routine, necessary
# Occupation 3: questioned, discreet
# ...
```

**Observing exclusions**
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Generate many occupations
for i in range(1000):
    occ = generate_occupation_condition(seed=i)

    # Check for excluded combinations
    if occ.get('legitimacy') == 'illicit' and occ.get('visibility') == 'conspicuous':
        print("Found excluded combination!")
        break
else:
    print("No excluded combinations found (as expected)")
# Output: "No excluded combinations found (as expected)"
```

#### Return Value Structure

The returned dictionary always includes:
- **legitimacy** (mandatory)
- **visibility** (mandatory)

And may include 0-2 of:
- **moral_load** (optional)
- **dependency** (optional)
- **risk_exposure** (optional)

**Minimum return**: `{"legitimacy": "...", "visibility": "..."}`
**Maximum return**: `{"legitimacy": "...", "visibility": "...", "moral_load": "...", "dependency": "..."}`
(or any 2 optional axes)

---

### `occupation_condition_to_prompt()`

Convert structured occupation data to comma-separated prompt fragment.

#### Signature

```python
def occupation_condition_to_prompt(condition_dict: dict[str, str]) -> str
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `condition_dict` | `dict[str, str]` | **Required.** Dictionary from `generate_occupation_condition()` |

#### Returns

| Type | Description |
|------|-------------|
| `str` | Comma-separated string of occupation values. Empty dict returns empty string. |

#### Examples

**Basic usage**
```python
from condition_axis import generate_occupation_condition, occupation_condition_to_prompt

occ = generate_occupation_condition(seed=42)
prompt = occupation_condition_to_prompt(occ)
print(prompt)
# 'tolerated, discreet, burdened'
```

**Image generation**
```python
occ = generate_occupation_condition(seed=123)
occ_prompt = occupation_condition_to_prompt(occ)

full_prompt = f"illustration of a goblin, whose work is {occ_prompt}, in their workplace"
print(full_prompt)
# 'illustration of a goblin, whose work is sanctioned, routine, necessary, in their workplace'
```

**Combining systems**
```python
from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
    occupation_condition_to_prompt
)

char = generate_condition(seed=42)
occ = generate_occupation_condition(seed=42)

combined = f"{condition_to_prompt(char)}, occupation: {occupation_condition_to_prompt(occ)}"
print(combined)
# 'wiry, poor, weary, occupation: tolerated, discreet, burdened'
```

---

### `get_available_occupation_axes()`

Get list of all defined occupation axes.

#### Signature

```python
def get_available_occupation_axes() -> list[str]
```

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List of axis names: `['legitimacy', 'visibility', 'moral_load', 'dependency', 'risk_exposure']` |

#### Examples

```python
from condition_axis import get_available_occupation_axes

axes = get_available_occupation_axes()
print(axes)
# ['legitimacy', 'visibility', 'moral_load', 'dependency', 'risk_exposure']
```

---

### `get_occupation_axis_values()`

Get all possible values for a specific occupation axis.

#### Signature

```python
def get_occupation_axis_values(axis: str) -> list[str]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `axis` | `str` | **Required.** Axis name (e.g., `'legitimacy'`, `'visibility'`) |

#### Returns

| Type | Description |
|------|-------------|
| `list[str]` | List of possible values for that axis |

#### Raises

| Exception | Condition |
|-----------|-----------|
| `KeyError` | If axis not in `OCCUPATION_AXES` |

#### Examples

**Get values for axes**
```python
from condition_axis import get_occupation_axis_values

legitimacy_values = get_occupation_axis_values('legitimacy')
print(legitimacy_values)
# ['sanctioned', 'tolerated', 'questioned', 'illicit']

moral_load_values = get_occupation_axis_values('moral_load')
print(moral_load_values)
# ['neutral', 'burdened', 'conflicted', 'corrosive']
```

**Build UI**
```python
from condition_axis import get_available_occupation_axes, get_occupation_axis_values

for axis in get_available_occupation_axes():
    print(f"{axis.replace('_', ' ').title()}:")
    for value in get_occupation_axis_values(axis):
        print(f"  - {value}")
    print()
```

---

## Module Exports

```python
__all__ = [
    "OCCUPATION_AXES",
    "OCCUPATION_EXCLUSIONS",
    "OCCUPATION_POLICY",
    "OCCUPATION_WEIGHTS",
    "generate_occupation_condition",
    "get_available_occupation_axes",
    "get_occupation_axis_values",
    "occupation_condition_to_prompt",
]
```

---

## Advanced Usage

### Occupation Archetypes

Generate specific occupation archetypes by filtering:

```python
from condition_axis import generate_occupation_condition, occupation_condition_to_prompt

def generate_archetype(archetype_criteria: dict, max_attempts: int = 100):
    """Generate occupation matching specific archetype."""
    for _ in range(max_attempts):
        occ = generate_occupation_condition()
        if all(occ.get(k) == v for k, v in archetype_criteria.items()):
            return occ
    raise ValueError(f"Could not generate archetype {archetype_criteria}")

# Generate "Underground Worker" archetype
underground = generate_archetype({
    'legitimacy': 'tolerated',
    'visibility': 'hidden'
})
print(occupation_condition_to_prompt(underground))

# Generate "Public Official" archetype
official = generate_archetype({
    'legitimacy': 'sanctioned',
    'visibility': 'conspicuous'
})
print(occupation_condition_to_prompt(official))
```

### Narrative Occupation Descriptions

```python
def describe_occupation(occ_dict: dict) -> str:
    """Convert occupation to narrative description."""
    legitimacy = occ_dict.get('legitimacy', '')
    visibility = occ_dict.get('visibility', '')

    descriptions = {
        ('sanctioned', 'routine'): "a respectable tradesperson",
        ('tolerated', 'discreet'): "an informal service provider",
        ('questioned', 'routine'): "a morally grey professional",
        ('illicit', 'hidden'): "a secretive criminal operator",
        ('sanctioned', 'conspicuous'): "a prominent public official"
    }

    return descriptions.get((legitimacy, visibility), "a worker")

occ = generate_occupation_condition(seed=42)
print(f"They work as {describe_occupation(occ)}.")
# 'They work as an informal service provider.'
```

### Population Analysis

```python
from condition_axis import generate_occupation_condition
from collections import Counter

def analyze_occupation_population(size: int = 10000):
    """Analyze occupation distribution."""
    population = [generate_occupation_condition(seed=i) for i in range(size)]

    # Legitimacy distribution
    legitimacy = Counter(o['legitimacy'] for o in population)
    print("Legitimacy Distribution:")
    for value, count in legitimacy.most_common():
        pct = count / size * 100
        print(f"  {value:12} {count:5} ({pct:5.2f}%)")

    # Optional axis frequency
    has_moral = sum(1 for o in population if 'moral_load' in o)
    has_dependency = sum(1 for o in population if 'dependency' in o)
    has_risk = sum(1 for o in population if 'risk_exposure' in o)

    print(f"\nOptional axis frequency:")
    print(f"  moral_load:     {has_moral/size*100:.1f}%")
    print(f"  dependency:     {has_dependency/size*100:.1f}%")
    print(f"  risk_exposure:  {has_risk/size*100:.1f}%")

analyze_occupation_population()
```

---

## Testing Recommendations

### Test Reproducibility

```python
def test_occupation_reproducibility():
    """Same seed produces same result."""
    occ1 = generate_occupation_condition(seed=42)
    occ2 = generate_occupation_condition(seed=42)
    assert occ1 == occ2
```

### Test Mandatory Axes

```python
def test_mandatory_axes_present():
    """All occupations include mandatory axes."""
    for i in range(100):
        occ = generate_occupation_condition(seed=i)
        assert 'legitimacy' in occ
        assert 'visibility' in occ
```

### Test Exclusions

```python
def test_exclusion_rules():
    """Exclusion rules prevent illogical combinations."""
    for i in range(1000):
        occ = generate_occupation_condition(seed=i)

        # Test illicit excludes conspicuous
        if occ.get('legitimacy') == 'illicit':
            assert occ.get('visibility') != 'conspicuous'

        # Test sanctioned excludes hidden
        if occ.get('legitimacy') == 'sanctioned':
            assert occ.get('visibility') != 'hidden'

        # Test eroding excludes neutral moral load
        if occ.get('risk_exposure') == 'eroding':
            assert occ.get('moral_load') != 'neutral'
```

---

## Integration Examples

### Complete Character with Occupation

```python
from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
    occupation_condition_to_prompt
)

def generate_working_character(seed: int):
    """Generate character with occupation."""
    char = generate_condition(seed=seed)
    occ = generate_occupation_condition(seed=seed)

    char_desc = condition_to_prompt(char)
    occ_desc = occupation_condition_to_prompt(occ)

    return {
        'character': char,
        'occupation': occ,
        'prompt': f"{char_desc}, working in {occ_desc} conditions"
    }

character = generate_working_character(42)
print(character['prompt'])
# 'wiry, poor, weary, working in tolerated, discreet, burdened conditions'
```

---

## Version History

- **v1.0.0**: Initial stable release
  - Five-axis occupation generation
  - Weighted probability distributions
  - Bidirectional exclusion rules
  - Mandatory/optional axis policy

---

## See Also

- [Base Utilities API](_base.md) - Shared generation functions
- [Character Conditions API](./character_conditions.md) - Physical & social states
- [Facial Conditions API](./facial_conditions.md) - Facial perception modifiers
- [Occupation Axis Spec](../specifications/occupation_axis.md) - Full specification
- [Obey the Verb](../specifications/Obey_the_Verb.md) - Prompting philosophy
