# Baseline API Surface Documentation

**Date**: 2026-01-03
**Branch**: feature/merge-facial-into-character
**Purpose**: Record current API for backward compatibility verification

## Test Baseline

- **Total Tests**: 162
- **Pass Rate**: 100% (162/162 passed)
- **Coverage**: 89.66%
- **Test Time**: 0.90s

### Module Coverage
- `__init__.py`: 100.00%
- `_base.py`: 100.00%
- `character_conditions.py`: 89.47%
- `facial_conditions.py`: 81.58%
- `occupation_axis.py`: 89.47%

---

## facial_conditions Module API

### Exported Constants

```python
FACIAL_AXES: dict[str, list[str]]
# Structure:
{
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

FACIAL_POLICY: dict[str, Any]
# Structure:
{
    "mandatory": ["facial_signal"],
    "optional": [],
    "max_optional": 0
}

FACIAL_WEIGHTS: dict[str, dict[str, float]]
# Structure:
{
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

FACIAL_EXCLUSIONS: dict[tuple[str, str], dict[str, list[str]]]
# Structure: {} (empty - no internal exclusions)
```

### Exported Functions

```python
def generate_facial_condition(seed: int | None = None) -> dict[str, str]:
    """Generate a facial signal condition using weighted random selection.

    Args:
        seed: Optional random seed for reproducible generation.

    Returns:
        Dictionary always containing exactly one key: "facial_signal"
        Example: {"facial_signal": "weathered"}
    """

def facial_condition_to_prompt(condition_dict: dict[str, str]) -> str:
    """Convert facial condition to prompt fragment.

    Args:
        condition_dict: Dictionary from generate_facial_condition()

    Returns:
        Single word (facial signal value). Empty string if dict is empty.
        Example: "weathered"
    """

def get_available_facial_axes() -> list[str]:
    """Get list of all defined facial axes.

    Returns:
        List containing ['facial_signal']
    """

def get_facial_axis_values(axis: str) -> list[str]:
    """Get all possible values for a facial axis.

    Args:
        axis: Axis name (currently only 'facial_signal')

    Returns:
        List of possible values for that axis

    Raises:
        KeyError: If axis not in FACIAL_AXES
    """
```

### Module Exports (__all__)

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

---

## character_conditions Module API (Current)

### Exported Constants

```python
CONDITION_AXES: dict[str, list[str]]
# Current axes: physique, wealth, health, demeanor, age
# (facial_signal will be added in merge)

AXIS_POLICY: dict[str, Any]
# Current:
{
    "mandatory": ["physique", "wealth"],
    "optional": ["health", "demeanor", "age"],
    "max_optional": 2
}
# (facial_signal will be added to optional in merge)

WEIGHTS: dict[str, dict[str, float]]
# Current: physique, wealth
# (facial_signal weights will be added in merge)

EXCLUSIONS: dict[tuple[str, str], dict[str, list[str]]]
# Current: 4 exclusion rules
# (5 cross-system rules will be added in merge)
```

### Exported Functions

```python
def generate_condition(seed: int | None = None) -> dict[str, str]:
    """Generate character condition."""

def condition_to_prompt(condition_dict: dict[str, str]) -> str:
    """Convert condition to prompt fragment."""

def get_available_axes() -> list[str]:
    """Get list of all defined condition axes."""

def get_axis_values(axis: str) -> list[str]:
    """Get all possible values for a specific axis."""
```

---

## Integration Points

### Current Separate Usage

```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    condition_to_prompt,
    facial_condition_to_prompt,
)

# Generate separately
character = generate_condition(seed=42)
facial = generate_facial_condition(seed=42)

# Serialize separately
char_prompt = condition_to_prompt(character)
face_prompt = facial_condition_to_prompt(facial)

# Combine manually
full_prompt = f"{char_prompt}, {face_prompt}"
```

### Post-Merge Unified Usage (Target)

```python
from condition_axis import (
    generate_condition,
    condition_to_prompt,
)

# Generate unified (may include facial_signal)
character = generate_condition(seed=42)

# Serialize unified
prompt = condition_to_prompt(character)
# Automatically includes facial_signal if present
```

### Backward Compatibility (Post-Merge)

```python
# Old API will still work with deprecation warnings
from condition_axis import generate_facial_condition

facial = generate_facial_condition(seed=42)
# DeprecationWarning: generate_facial_condition() is deprecated...
```

---

## Backward Compatibility Requirements

To maintain backward compatibility, the merge MUST ensure:

1. ✅ All 8 facial_conditions functions remain importable
2. ✅ Functions have identical signatures
3. ✅ Functions return identical output structures
4. ✅ DeprecationWarning raised on use
5. ✅ All 162 existing tests continue to pass
6. ✅ Coverage maintained or increased (≥89.66%)

---

## Verification Checklist

After merge, verify:

- [ ] `from condition_axis import generate_facial_condition` works
- [ ] `from condition_axis import FACIAL_AXES` works
- [ ] Deprecated functions raise DeprecationWarning
- [ ] Deprecated functions return correct types
- [ ] All 162 baseline tests still pass
- [ ] Coverage ≥89.66%
- [ ] New tests for merged functionality pass
- [ ] Examples using old API still work

---

## Notes

- **Total API surface**: 8 exports from facial_conditions (4 constants, 4 functions)
- **Merge strategy**: Keep all exports as backward-compatible wrappers
- **Deprecation timeline**: v1.1.0 (deprecated) → v2.0.0 (removed)
- **Cross-system exclusions**: 5 new rules to be added

---

**Document Version**: 1.0
**Last Updated**: 2026-01-03
**Status**: ✅ Complete
