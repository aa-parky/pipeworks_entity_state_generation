# Migration Guide: v1.0.0 → v1.1.0

This guide explains how to migrate your code from v1.0.0 to v1.1.0, which introduced the **unified character conditions API** by merging facial signals into the main character generation system.

---

## What Changed in v1.1.0?

### Summary

**v1.0.0**: Facial conditions were a separate module with dedicated functions
**v1.1.0**: Facial signals are now integrated into `character_conditions` as an optional axis

### Key Changes

1. **`generate_facial_condition()` removed** from public API
2. **`facial_condition_to_prompt()` removed** from public API
3. **`facial_signal` is now an optional axis** within `generate_condition()`
4. **Cross-system exclusion rules** implemented between facial signals and other character axes
5. **No breaking changes** to existing `generate_condition()` or `generate_occupation_condition()` APIs

---

## Migration Patterns

### Pattern 1: Basic Facial Generation

**Old Code (v1.0.0)**:
```python
from condition_axis import generate_facial_condition, facial_condition_to_prompt

facial = generate_facial_condition(seed=42)
# {'facial_signal': 'weathered'}

prompt = facial_condition_to_prompt(facial)
# 'weathered'
```

**New Code (v1.1.0+)**:
```python
from condition_axis import generate_condition, condition_to_prompt

# Generate character (may include facial_signal)
character = generate_condition(seed=42)
# {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary', 'facial_signal': 'weathered'}

# Extract facial signal if present
facial_signal = character.get('facial_signal', None)
# 'weathered' or None

# Or convert entire character to prompt (includes facial_signal if present)
prompt = condition_to_prompt(character)
# 'wiry, poor, weary, weathered'
```

---

### Pattern 2: Combining Character and Facial Conditions

**Old Code (v1.0.0)**:
```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    condition_to_prompt,
    facial_condition_to_prompt,
)

character = generate_condition(seed=42)
facial = generate_facial_condition(seed=42)

char_prompt = condition_to_prompt(character)
face_prompt = facial_condition_to_prompt(facial)

combined = f"{char_prompt}, {face_prompt}"
# 'wiry, poor, weary, weathered'
```

**New Code (v1.1.0+)**:
```python
from condition_axis import generate_condition, condition_to_prompt

# Facial signals are automatically included
character = generate_condition(seed=42)

# Single conversion includes everything
prompt = condition_to_prompt(character)
# 'wiry, poor, weary, weathered'
```

**Result**: Simpler code, same output

---

### Pattern 3: Conditional Facial Signal Handling

**Old Code (v1.0.0)**:
```python
# Generate character
character = generate_condition(seed=42)

# Optionally add facial signal
include_facial = True
if include_facial:
    facial = generate_facial_condition(seed=42)
    full_prompt = f"{condition_to_prompt(character)}, {facial_condition_to_prompt(facial)}"
else:
    full_prompt = condition_to_prompt(character)
```

**New Code (v1.1.0+)**:
```python
# Generate character (facial_signal is already optional)
character = generate_condition(seed=42)

# Facial signal may or may not be present
full_prompt = condition_to_prompt(character)

# Check if facial signal was included
has_facial = 'facial_signal' in character
```

**Result**: The system automatically handles optionality

---

### Pattern 4: Separate Facial and Character Storage

**Old Code (v1.0.0)**:
```python
# Store separately
entity = {
    'character': generate_condition(seed=42),
    'facial': generate_facial_condition(seed=42),
    'occupation': generate_occupation_condition(seed=42)
}

# Reconstruct prompt
prompt = (
    f"{condition_to_prompt(entity['character'])}, "
    f"{facial_condition_to_prompt(entity['facial'])}, "
    f"{occupation_condition_to_prompt(entity['occupation'])}"
)
```

**New Code (v1.1.0+)**:
```python
# Facial signal is part of character
entity = {
    'character': generate_condition(seed=42),
    'occupation': generate_occupation_condition(seed=42)
}

# Simpler reconstruction
prompt = (
    f"{condition_to_prompt(entity['character'])}, "
    f"{occupation_condition_to_prompt(entity['occupation'])}"
)
```

**Result**: Cleaner data model

---

### Pattern 5: Filtering/Customizing Facial Signals

**Old Code (v1.0.0)**:
```python
# Generate until specific facial signal found
while True:
    facial = generate_facial_condition()
    if facial['facial_signal'] == 'weathered':
        break
```

**New Code (v1.1.0+)**:
```python
# Generate until character has desired facial signal
while True:
    character = generate_condition()
    if character.get('facial_signal') == 'weathered':
        break

# Or check if facial_signal is present at all
while True:
    character = generate_condition()
    if 'facial_signal' in character:
        break
```

**Result**: Same pattern, different accessor

---

## Understanding the New System

### Facial Signal as Optional Axis

In v1.1.0, `facial_signal` is one of **four optional axes**:
- `health`
- `demeanor`
- `age`
- `facial_signal` *(new)*

**Policy**: Each generation randomly includes **0-2** optional axes (controlled by `max_optional=2`)

**This means**:
- `facial_signal` may or may not appear in any given generation
- It competes with other optional axes for inclusion
- When it appears, it follows the same exclusion rules as other axes

### Cross-System Exclusion Rules

v1.1.0 introduces exclusion rules between facial signals and other character axes:

| Trigger | Excluded Facial Signal | Rationale |
|---------|------------------------|-----------|
| `age=young` | `weathered` | Youth contradicts wear |
| `age=ancient` | `understated` | Age is rarely subtle |
| `wealth=decadent` | `weathered` | Wealth preserves appearance |
| `health=hale` | `weathered` | Health shows in appearance |
| `health=sickly` | `soft-featured` | Sickness affects appearance |

**Example**:
```python
# This combination will never occur
character = generate_condition(seed=X)
# character will NEVER be: {'age': 'young', 'facial_signal': 'weathered'}
```

---

## API Compatibility Chart

| v1.0.0 Function | v1.1.0 Status | Replacement |
|----------------|---------------|-------------|
| `generate_condition()` | ✅ **Unchanged** | Same function, now may include `facial_signal` |
| `condition_to_prompt()` | ✅ **Unchanged** | Same function, handles `facial_signal` automatically |
| `generate_facial_condition()` | ❌ **Removed** | Use `generate_condition()` |
| `facial_condition_to_prompt()` | ❌ **Removed** | Use `condition_to_prompt()` |
| `get_available_facial_axes()` | ❌ **Removed** | Use `get_available_axes()` |
| `get_facial_axis_values()` | ❌ **Removed** | Use `get_axis_values('facial_signal')` |
| `FACIAL_AXES` | ❌ **Removed** | Now part of `CONDITION_AXES` |
| `FACIAL_POLICY` | ❌ **Removed** | Now part of `AXIS_POLICY` |
| `FACIAL_WEIGHTS` | ❌ **Removed** | Now part of `WEIGHTS` |
| `FACIAL_EXCLUSIONS` | ❌ **Removed** | Now part of `EXCLUSIONS` |

---

## Recommended Migration Steps

### Step 1: Update Imports
```python
# Remove
from condition_axis import generate_facial_condition, facial_condition_to_prompt

# Keep (these still work)
from condition_axis import generate_condition, condition_to_prompt
```

### Step 2: Replace Facial Generation Calls
```python
# Replace this
facial = generate_facial_condition(seed=42)

# With this (check for facial_signal in result)
character = generate_condition(seed=42)
if 'facial_signal' in character:
    facial_signal = character['facial_signal']
```

### Step 3: Consolidate Prompt Generation
```python
# Replace this
combined = f"{condition_to_prompt(char)}, {facial_condition_to_prompt(facial)}"

# With this
combined = condition_to_prompt(character)
```

### Step 4: Update Data Models
If you're storing entities in JSON or databases:
```python
# Old schema
{
    "character": {"physique": "wiry", "wealth": "poor"},
    "facial": {"facial_signal": "weathered"}
}

# New schema
{
    "character": {"physique": "wiry", "wealth": "poor", "facial_signal": "weathered"}
}
```

### Step 5: Test Exclusion Rule Interactions
```python
# Test that exclusions work as expected
for i in range(1000):
    char = generate_condition(seed=i)

    # These combinations should never occur
    if char.get('age') == 'young':
        assert char.get('facial_signal') != 'weathered'

    if char.get('wealth') == 'decadent':
        assert char.get('facial_signal') != 'weathered'
```

---

## Benefits of Upgrading

1. **Simpler API**: One function instead of two
2. **Semantic Coherence**: Exclusion rules prevent illogical combinations
3. **Cleaner Data Models**: Facial signals stored with character data
4. **Fewer Imports**: Less boilerplate code
5. **Better Integration**: Facial signals interact with other character axes

---

## Need Help?

- **API Documentation**: See [Character Conditions API](../api/character_conditions.md)
- **Examples**: Check `examples/integration_example.py` for updated patterns
- **Questions**: Open an issue on GitHub

---

## Version History

- **v1.0.0**: Separate `facial_conditions` module
- **v1.1.0**: Merged facial signals into `character_conditions` with unified API
