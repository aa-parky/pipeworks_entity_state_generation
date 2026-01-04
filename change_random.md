# Random Number Generation Refactoring

**Status**: Planning
**Version**: 0.10.0 → 0.10.1
**Type**: Internal implementation improvement (patch)
**Breaking Changes**: None

## Overview

Refactor random number generation from global `random.seed()` to isolated `random.Random()` instances to prevent global state pollution and improve thread safety.

## Problem Statement

### Current Implementation

The library currently modifies the global random state:

```python
# character_conditions.py:194-195
def generate_condition(seed: int | None = None) -> dict[str, str]:
    if seed is not None:
        random.seed(seed)  # ❌ Modifies global state
    # ...
```

### Issues

1. **Global State Pollution**: Calling `generate_condition(seed=42)` changes the random state for the entire application
2. **Unexpected Side Effects**: User code relying on `random` module gets its state stomped on
3. **Thread Safety Concerns**: Global seed affects all threads
4. **Anti-Pattern**: Violates Python library best practices (see NumPy, SciPy, scikit-learn)

### Real-World Impact

```python
import random
from condition_axis import generate_condition

# User's game sets seed for reproducibility
random.seed(12345)
enemy_spawn = random.random()  # Expected: 0.2849...

# User generates a character
char = generate_condition(seed=42)  # ❌ Stomps on user's seed!

# User's game continues
loot_drop = random.random()  # ❌ NOT what user expects!
```

## Solution

### Isolated RNG Instances

Use `random.Random(seed)` to create isolated random number generators:

```python
def generate_condition(seed: int | None = None) -> dict[str, str]:
    rng = random.Random(seed)  # ✅ Isolated RNG instance
    # Use rng.choice(), rng.sample(), rng.randint() instead of module functions
```

### Benefits

✅ **No global state pollution**: Each call is isolated
✅ **Thread-safe**: Each thread can have its own RNG
✅ **Predictable behavior**: User's random state unaffected
✅ **Best practice**: Follows NumPy, SciPy, PyTorch patterns
✅ **Backward compatible**: Same seeds produce same output
✅ **All tests pass**: Deterministic behavior preserved

## Implementation Plan

### Phase 1: Update Base Utilities

**File**: `src/condition_axis/_base.py`

**Change**: Update `weighted_choice()` to accept RNG instance

```python
def weighted_choice(
    options: list[str],
    weights: dict[str, float] | None = None,
    rng: random.Random | None = None,  # NEW parameter
) -> str:
    """Select a random option with optional weighted probabilities.

    Args:
        options: List of possible values to choose from.
        weights: Optional dictionary mapping options to weights.
        rng: Optional Random instance for isolated random generation.
             If None, uses global random module.

    Returns:
        Randomly selected option (str)
    """
    # Use provided RNG or fall back to global
    if rng is None:
        rng = random

    if not weights:
        return rng.choice(options)

    weight_values = [weights.get(option, 1.0) for option in options]
    return rng.choices(options, weights=weight_values, k=1)[0]
```

**Lines changed**: `_base.py:26-70`
**Test impact**: None (backward compatible - `rng=None` preserves old behavior)

---

### Phase 2: Update Character Conditions

**File**: `src/condition_axis/character_conditions.py`

**Change**: Replace `random.seed(seed)` with `rng = random.Random(seed)`

```python
def generate_condition(seed: int | None = None) -> dict[str, str]:
    """Generate a coherent character condition using weighted random selection.

    ... (existing docstring unchanged) ...
    """
    # Create isolated RNG instance
    rng = random.Random(seed)  # CHANGED: was random.seed(seed)

    chosen: dict[str, str] = {}

    # PHASE 1: Select mandatory axes
    for axis in AXIS_POLICY["mandatory"]:
        if axis not in CONDITION_AXES:
            logger.warning(f"Mandatory axis '{axis}' not defined in CONDITION_AXES")
            continue

        # CHANGED: Pass rng to weighted_choice
        chosen[axis] = weighted_choice(CONDITION_AXES[axis], WEIGHTS.get(axis), rng=rng)
        logger.debug(f"Mandatory axis selected: {axis} = {chosen[axis]}")

    # PHASE 2: Select optional axes
    max_optional = AXIS_POLICY.get("max_optional", 2)
    num_optional = rng.randint(0, min(max_optional, len(AXIS_POLICY["optional"])))  # CHANGED: rng.randint

    optional_axes = rng.sample(AXIS_POLICY["optional"], num_optional)  # CHANGED: rng.sample
    logger.debug(f"Selected {num_optional} optional axes: {optional_axes}")

    for axis in optional_axes:
        if axis not in CONDITION_AXES:
            logger.warning(f"Optional axis '{axis}' not defined in CONDITION_AXES")
            continue

        # CHANGED: Pass rng to weighted_choice
        chosen[axis] = weighted_choice(CONDITION_AXES[axis], WEIGHTS.get(axis), rng=rng)
        logger.debug(f"Optional axis selected: {axis} = {chosen[axis]}")

    # PHASE 3: Apply semantic exclusion rules (unchanged)
    apply_exclusion_rules(chosen, EXCLUSIONS)

    return chosen
```

**Lines changed**: `character_conditions.py:164-236`
**Test impact**: None (same seeds produce same output)

---

### Phase 3: Update Occupation Conditions

**File**: `src/condition_axis/occupation_axis.py`

**Change**: Same pattern as character_conditions.py

```python
def generate_occupation_condition(seed: int | None = None) -> dict[str, str]:
    """Generate a coherent occupation condition using weighted random selection.

    ... (existing docstring unchanged) ...
    """
    # Create isolated RNG instance
    rng = random.Random(seed)  # CHANGED: was random.seed(seed)

    chosen: dict[str, str] = {}

    # PHASE 1: Select mandatory axes
    for axis in OCCUPATION_POLICY["mandatory"]:
        if axis not in OCCUPATION_AXES:
            logger.warning(f"Mandatory axis '{axis}' not defined")
            continue

        # CHANGED: Pass rng to weighted_choice
        chosen[axis] = weighted_choice(
            OCCUPATION_AXES[axis],
            OCCUPATION_WEIGHTS.get(axis),
            rng=rng
        )
        logger.debug(f"Mandatory axis: {axis} = {chosen[axis]}")

    # PHASE 2: Select optional axes
    max_optional = OCCUPATION_POLICY.get("max_optional", 2)
    num_optional = rng.randint(0, min(max_optional, len(OCCUPATION_POLICY["optional"])))  # CHANGED

    optional_axes = rng.sample(OCCUPATION_POLICY["optional"], num_optional)  # CHANGED
    logger.debug(f"Selected {num_optional} optional axes: {optional_axes}")

    for axis in optional_axes:
        if axis not in OCCUPATION_AXES:
            logger.warning(f"Optional axis '{axis}' not defined")
            continue

        # CHANGED: Pass rng to weighted_choice
        chosen[axis] = weighted_choice(
            OCCUPATION_AXES[axis],
            OCCUPATION_WEIGHTS.get(axis),
            rng=rng
        )
        logger.debug(f"Optional axis: {axis} = {chosen[axis]}")

    # PHASE 3: Apply exclusion rules (unchanged)
    apply_exclusion_rules(chosen, OCCUPATION_EXCLUSIONS)

    return chosen
```

**Lines changed**: Similar to character_conditions pattern
**Test impact**: None (same seeds produce same output)

---

### Phase 4: Verification

#### 4.1 Run Full Test Suite

```bash
pytest tests/ -v
```

**Expected**: All tests pass (identical output with isolated RNG)

#### 4.2 Verify Examples

All examples use public API only and should work unchanged:

- ✅ `basic_usage.py` - Uses `generate_condition(seed=X)` (no changes needed)
- ✅ `advanced_usage.py` - Uses `generate_condition(seed=X)` (no changes needed)
- ✅ `integration_example.py` - Uses `generate_condition(seed=X)` (no changes needed)
- ✅ `batch_generation.py` - Uses `generate_condition(seed=X)` (no changes needed)
- ✅ `custom_axes.py` - May need review if it extends generators
- ✅ `image_prompt_generation.py` - Uses `generate_condition(seed=X)` (no changes needed)

**Verification command**:
```bash
for script in basic_usage.py advanced_usage.py integration_example.py batch_generation.py custom_axes.py image_prompt_generation.py
do
    echo "Testing examples/$script..."
    timeout 30 python examples/$script > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✓ PASS"
    else
        echo "  ✗ FAIL"
        exit 1
    fi
done
```

#### 4.3 Verify Determinism

Create a test to verify that refactored code produces identical output:

```python
# test_random_refactor_verification.py
import random
from condition_axis import generate_condition, generate_occupation_condition

def test_determinism_preserved():
    """Verify that same seeds still produce same output after refactor."""
    # Character conditions
    for seed in [0, 1, 42, 123, 999999]:
        result1 = generate_condition(seed=seed)
        result2 = generate_condition(seed=seed)
        assert result1 == result2, f"Non-deterministic for seed {seed}"

    # Occupation conditions
    for seed in [0, 1, 42, 123, 999999]:
        result1 = generate_occupation_condition(seed=seed)
        result2 = generate_occupation_condition(seed=seed)
        assert result1 == result2, f"Non-deterministic for seed {seed}"

def test_no_global_state_pollution():
    """Verify that library doesn't affect global random state."""
    # Set a known global seed
    random.seed(12345)
    baseline = random.random()

    # Reset and generate character (should not affect global state)
    random.seed(12345)
    _ = generate_condition(seed=42)
    after_char = random.random()

    # Should be identical
    assert baseline == after_char, "Library polluted global random state!"
```

---

### Phase 5: Documentation Updates

#### 5.1 Update CLAUDE.md

Add note about isolated RNG (optional, for future reference):

```markdown
### Random Number Generation

The library uses isolated `random.Random()` instances rather than the global
`random` module to prevent side effects in user code. This means:

- Each generation call with a seed is isolated
- User's global random state is never modified
- Thread-safe random generation
- Same seeds produce same output (deterministic)
```

#### 5.2 Update Docstrings (if needed)

The existing docstrings are already correct - they describe the seed parameter
behavior, which remains unchanged.

---

### Phase 6: Version Bump and Release

#### 6.1 Update Version Numbers

**Files to update**:
- `pyproject.toml:7` - `version = "0.10.1"`
- `src/condition_axis/__init__.py:98` - `__version__ = "0.10.1"`

#### 6.2 Update Changelog

Create or update `CHANGELOG.md`:

```markdown
## [0.10.1] - 2026-01-04

### Fixed
- Random number generation now uses isolated `random.Random()` instances
  instead of modifying global random state, preventing side effects in
  user code and improving thread safety.

### Internal
- Refactored `weighted_choice()` to accept optional RNG instance
- Updated `generate_condition()` to use isolated RNG
- Updated `generate_occupation_condition()` to use isolated RNG

### Compatibility
- No breaking changes - all existing code continues to work
- Same seeds produce identical output
- All tests pass without modification
```

---

## Testing Checklist

- [ ] Phase 1: Update `_base.weighted_choice()` to accept `rng` parameter
- [ ] Phase 2: Update `character_conditions.generate_condition()` to use isolated RNG
- [ ] Phase 3: Update `occupation_axis.generate_occupation_condition()` to use isolated RNG
- [ ] Run full test suite: `pytest tests/ -v --cov=condition_axis`
- [ ] Verify all examples run successfully
- [ ] Create verification test for determinism
- [ ] Create verification test for no global state pollution
- [ ] Update version to 0.10.1
- [ ] Run pre-commit hooks: `pre-commit run --all-files`
- [ ] Build package: `python -m build`
- [ ] Test package installation: `pip install -e .`
- [ ] Final smoke test of all examples
- [ ] Commit changes with message: `fix: use isolated RNG instances to prevent global state pollution`

## Risk Assessment

**Risk Level**: ⚠️ **LOW**

- ✅ No API changes (function signatures unchanged)
- ✅ Deterministic behavior preserved (same seeds = same output)
- ✅ All tests should pass without modification
- ✅ Examples require no changes
- ⚠️ Minor risk: Verify that `random.Random(seed)` produces identical sequences to `random.seed(seed)` for all operations used

**Mitigation**: Create comprehensive verification tests before and after refactor.

## Success Criteria

1. ✅ All existing tests pass without modification
2. ✅ All examples run successfully without changes
3. ✅ New test confirms no global state pollution
4. ✅ Same seeds produce identical output before/after refactor
5. ✅ Pre-commit hooks pass
6. ✅ Code quality tools pass (black, ruff, mypy)

## References

- **Python random module docs**: https://docs.python.org/3/library/random.html#random.Random
- **NumPy random approach**: https://numpy.org/doc/stable/reference/random/generator.html
- **Issue raised by**: Code review feedback on global state pollution

## Timeline

**Estimated effort**: 1-2 hours

- Phase 1-3: 30 minutes (implementation)
- Phase 4: 20 minutes (verification)
- Phase 5: 10 minutes (documentation)
- Phase 6: 10 minutes (version bump and build)
- Buffer: 20 minutes (unexpected issues)

## Post-Implementation

After successful implementation:

1. Tag release: `git tag v0.10.1`
2. Push to GitHub: `git push origin main --tags`
3. Consider publishing to PyPI (optional)
4. Close related GitHub issues (if any)
5. Update project status in README (if applicable)

---

**Document created**: 2026-01-04
**Last updated**: 2026-01-04
**Author**: Code review response - RNG isolation refactoring
