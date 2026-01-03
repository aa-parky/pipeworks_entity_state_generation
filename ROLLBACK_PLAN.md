# Rollback Plan: Facial Conditions Merge

**Created**: 2026-01-03
**Branch**: feature/merge-facial-into-character
**Status**: Pre-merge documentation

## Overview

This document provides a comprehensive rollback procedure if the facial conditions merge causes critical issues after deployment. Since this merge involved **FULL REMOVAL** of the deprecated `facial_conditions` API (no backward compatibility), rollback is the only recovery option for users depending on the old API.

## Risk Assessment

**Breaking Change Level**: HIGH
**Backward Compatibility**: NONE (all deprecated code removed)
**User Impact**: Any code using `generate_facial_condition()` or related functions will break immediately

## When to Rollback

Execute rollback if:

1. **Critical bugs** discovered in production that block core functionality
2. **User reports** indicate widespread breakage of existing integrations
3. **Test failures** appear after merge that weren't caught in CI
4. **Performance regressions** that significantly impact generation speed
5. **Data quality issues** with the new cross-system exclusion rules

## Rollback Procedure

### Step 1: Assess the Situation

```bash
# Review recent commits to identify the merge point
git log --oneline --graph --all -20

# Check current branch
git branch --show-current

# Verify the state of the working directory
git status
```

### Step 2: Create Hotfix Branch

```bash
# Switch to main branch
git checkout main

# Pull latest changes
git pull origin main

# Create hotfix branch
git checkout -b hotfix/revert-facial-merge
```

### Step 3: Identify Commits to Revert

The facial conditions merge consists of these commits (in order):

```bash
# Key commits from the merge (newest to oldest):
# 5cc4809 - docs: mark Section 7 complete in merge_todo.md (97% complete)
# da90158 - style: apply ruff auto-fix for __all__ sorting
# 25ff4fc - style: apply black formatting to test_examples.py
# 5ee4c12 - fix: update all examples and tests to use unified API only
# 3ad23e1 - refactor: remove all deprecated facial conditions API (Section 7)
# cb4d919 - style: apply black formatting to all files
# da395be - style: fix E402 linting error - move all imports to top of file
# 634c264 - docs: mark Section 5 complete in merge_todo.md (90% complete)
# 0a3a102 - docs: complete Section 5 - Documentation Updates
# 6a48c79 - docs: mark Section 4 complete in merge_todo.md (69% complete)
# d2560e4 - feat: update examples for unified facial signal API (Section 4)
# 271bb4e - docs: mark Sections 2 & 3 tasks complete in merge_todo.md
# b9fdd19 - style: fix linting issues (black formatting + ruff E402)
# cc0d67c - docs: update merge_todo.md with progress (60% complete)
# ace1ae2 - test: update tests for facial signal integration
# 0eed1e0 - feat: integrate facial signals into character conditions system
# 6587a7b - docs: establish baseline API documentation
# 0405711 - docs: add comprehensive merge TODO
```

### Step 4: Revert the Merge

**Option A: Revert All Merge Commits** (Safest)

```bash
# Revert commits in reverse order (newest first)
git revert 5cc4809  # docs: mark Section 7 complete
git revert da90158  # style: apply ruff auto-fix
git revert 25ff4fc  # style: apply black formatting
git revert 5ee4c12  # fix: update all examples and tests
git revert 3ad23e1  # refactor: remove all deprecated API (CRITICAL)
git revert cb4d919  # style: apply black formatting
git revert da395be  # style: fix E402 linting error
git revert 634c264  # docs: mark Section 5 complete
git revert 0a3a102  # docs: complete Section 5
git revert 6a48c79  # docs: mark Section 4 complete
git revert d2560e4  # feat: update examples for unified API
git revert 271bb4e  # docs: mark Sections 2 & 3 complete
git revert b9fdd19  # style: fix linting issues
git revert cc0d67c  # docs: update merge_todo.md
git revert ace1ae2  # test: update tests for facial integration
git revert 0eed1e0  # feat: integrate facial signals (CRITICAL)
git revert 6587a7b  # docs: establish baseline API
git revert 0405711  # docs: add comprehensive merge TODO
```

**Option B: Reset to Pre-Merge State** (Nuclear option)

```bash
# Find the commit BEFORE the merge started (0405711 is first merge commit)
git log --oneline

# Reset to the commit before 0405711
git reset --hard <commit-sha-before-merge>

# Note: This will lose all merge work. Only use if revert fails.
```

### Step 5: Verify Rollback

```bash
# Run full test suite to ensure stability
pytest --cov=condition_axis --cov-report=term-missing -v

# Verify old API is restored (should find facial_conditions.py)
ls -la src/condition_axis/facial_conditions.py

# Verify tests pass
pytest tests/test_facial_conditions_axis.py -v

# Check examples work
python examples/integration_example.py

# Verify code quality
black src/ tests/ --line-length=100 --check
ruff check src/ tests/ --line-length=100
mypy src/ --python-version=3.12 --ignore-missing-imports
```

### Step 6: Test Old API Functionality

```bash
# Create quick verification script
cat > verify_old_api.py << 'EOF'
"""Verify old facial conditions API is restored."""

from condition_axis import (
    generate_facial_condition,
    facial_condition_to_prompt,
    FACIAL_AXES,
    FACIAL_WEIGHTS,
)

# Test generation
facial = generate_facial_condition(seed=42)
print(f"Generated facial condition: {facial}")

# Test serialization
prompt = facial_condition_to_prompt(facial)
print(f"Prompt: {prompt}")

# Test data structures
print(f"FACIAL_AXES keys: {list(FACIAL_AXES.keys())}")
print(f"FACIAL_WEIGHTS keys: {list(FACIAL_WEIGHTS.keys())}")

print("\n✓ Old API restored and functional!")
EOF

python verify_old_api.py
```

### Step 7: Push Hotfix

```bash
# Push the hotfix branch
git push origin hotfix/revert-facial-merge

# Create pull request with description:
# "Rollback: Revert facial conditions merge due to [REASON]"
#
# Impact: This restores the old facial_conditions module and
# separate API functions. Users can continue using the deprecated API.
```

### Step 8: Deploy Hotfix

```bash
# After PR approval, merge to main
git checkout main
git merge hotfix/revert-facial-merge
git push origin main

# Tag the hotfix release
git tag -a v1.0.1-hotfix -m "Hotfix: Rollback facial merge"
git push origin v1.0.1-hotfix
```

## Partial Rollback Options

If only specific features are problematic, consider partial fixes:

### Option 1: Restore Backward Compatibility Wrappers

Instead of full rollback, restore only the wrapper functions:

```python
# Add to src/condition_axis/__init__.py

import warnings

def generate_facial_condition(seed: int | None = None) -> dict[str, str]:
    """Generate facial condition (DEPRECATED - Backward compat wrapper)."""
    warnings.warn(
        "generate_facial_condition() is deprecated. Use generate_condition().",
        DeprecationWarning,
        stacklevel=2
    )

    import random
    if seed is not None:
        random.seed(seed)

    from .character_conditions import CONDITION_AXES, WEIGHTS
    from ._base import weighted_choice

    facial_signal = weighted_choice(
        CONDITION_AXES["facial_signal"],
        WEIGHTS.get("facial_signal")
    )

    return {"facial_signal": facial_signal}

# Add other wrapper functions...
```

This provides emergency backward compatibility without reverting the merge.

### Option 2: Fix Specific Exclusion Rules

If exclusion rules are too aggressive:

```python
# Edit src/condition_axis/character_conditions.py
# Remove or modify problematic exclusion rules

# For example, if "young + weathered" exclusion is too strict:
EXCLUSIONS: dict[tuple[str, str], dict[str, list[str]]] = {
    # ... other exclusions ...

    # REMOVED: Too strict for some use cases
    # ("age", "young"): {
    #     "facial_signal": ["weathered"],
    # },
}
```

## Post-Rollback Actions

After successful rollback:

1. **Communicate with users**:
   - Announce the rollback on GitHub/docs
   - Explain what happened and why
   - Provide timeline for fix

2. **Root cause analysis**:
   - Identify what went wrong
   - Document lessons learned
   - Update testing procedures

3. **Plan re-merge**:
   - Fix identified issues
   - Add more comprehensive tests
   - Consider phased rollout with feature flags
   - Add backward compatibility wrappers

4. **Update documentation**:
   - Mark the old API as "stable" again
   - Remove deprecation warnings
   - Update migration guide with lessons learned

## Prevention for Future Merges

To avoid needing rollback in future:

1. **Feature flags**: Use environment variables to toggle new behavior
2. **Backward compatibility period**: Maintain old API for 1-2 releases
3. **Beta testing**: Release as alpha/beta first for early feedback
4. **Gradual rollout**: Deploy to subset of users first
5. **Better testing**: More integration tests, user acceptance testing

## Emergency Contacts

If rollback is needed:

- **Repository owner**: @aapark
- **Primary maintainer**: [Add contact info]
- **Backup maintainer**: [Add contact info]

## Rollback Decision Tree

```
Is the issue critical?
├─ YES → Does it affect all users?
│   ├─ YES → Full rollback (Option A or B)
│   └─ NO → Can we hotfix specific issue?
│       ├─ YES → Partial rollback or targeted fix
│       └─ NO → Full rollback
│
└─ NO → Can we fix forward?
    ├─ YES → Create hotfix PR with fix
    └─ NO → Consider rollback
```

## Success Criteria for Rollback

Rollback is successful when:

- [ ] All tests pass (100% pass rate)
- [ ] Old API functions are restored and working
- [ ] `facial_conditions.py` module exists
- [ ] `test_facial_conditions_axis.py` tests pass
- [ ] Examples work with old API
- [ ] Code quality checks pass (black, ruff, mypy)
- [ ] No references to unified API in old code
- [ ] Documentation reflects current state

## Files Changed by Merge (Reference)

Files that would be affected by rollback:

**Core modules**:
- `src/condition_axis/__init__.py` - API exports and wrappers
- `src/condition_axis/character_conditions.py` - Added facial_signal axis
- `src/condition_axis/facial_conditions.py` - DELETED (would be restored)

**Tests**:
- `tests/test_character_conditions_axis.py` - Added facial tests
- `tests/test_facial_conditions_axis.py` - DELETED (would be restored)
- `tests/test_examples.py` - Updated for unified API

**Examples**:
- `examples/basic_usage.py` - Updated imports
- `examples/advanced_usage.py` - Updated imports
- `examples/integration_example.py` - Updated to extract facial from character
- `examples/batch_generation.py` - Updated facial generation
- `examples/custom_axes.py` - Updated imports
- `examples/image_prompt_generation.py` - Updated to extract facial
- `examples/migration_guide.py` - DELETED (migration no longer needed)

**Documentation**:
- `README.md` - Updated Quick Start and examples
- `CLAUDE.md` - Updated architecture section
- `docs/api/character_conditions.md` - Added facial_signal docs
- `docs/api/facial_conditions.md` - Added deprecation notice
- `merge_todo.md` - Progress tracking

---

**Last Updated**: 2026-01-03
**Reviewed By**: [To be filled]
**Next Review**: After merge to main
