#!/usr/bin/env python3
"""Smoke test for facial conditions merge.

Quick verification that basic functionality works after merge.
This script tests the unified API (post-merge) without backward compatibility.

Run this test:
    python smoke_test.py

Expected output:
    ✓ All smoke tests passed!

Exit codes:
    0 - All tests passed
    1 - One or more tests failed
"""

import sys
from typing import Any


def test_imports() -> None:
    """Test that required imports work."""
    print("Testing imports...")

    try:
        from condition_axis import (
            generate_condition,
            condition_to_prompt,
            CONDITION_AXES,
            AXIS_POLICY,
            WEIGHTS,
            EXCLUSIONS,
            get_available_axes,
            get_axis_values,
        )
        print("  ✓ All imports successful")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        raise


def test_deprecated_api_removed() -> None:
    """Test that deprecated API functions are removed."""
    print("\nTesting deprecated API removal...")

    import condition_axis

    # These should NOT exist after merge
    deprecated_functions = [
        "generate_facial_condition",
        "facial_condition_to_prompt",
        "get_available_facial_axes",
        "get_facial_axis_values",
    ]

    deprecated_data = [
        "FACIAL_AXES",
        "FACIAL_POLICY",
        "FACIAL_WEIGHTS",
        "FACIAL_EXCLUSIONS",
    ]

    found_deprecated = []

    for func_name in deprecated_functions:
        if hasattr(condition_axis, func_name):
            found_deprecated.append(f"function: {func_name}")

    for data_name in deprecated_data:
        if hasattr(condition_axis, data_name):
            found_deprecated.append(f"data structure: {data_name}")

    if found_deprecated:
        print(f"  ✗ Found deprecated API that should be removed:")
        for item in found_deprecated:
            print(f"    - {item}")
        raise AssertionError("Deprecated API still exists")

    print("  ✓ All deprecated API removed")


def test_basic_generation() -> None:
    """Test basic character generation."""
    print("\nTesting basic character generation...")

    from condition_axis import generate_condition

    char = generate_condition(seed=42)

    assert isinstance(char, dict), "Result should be a dict"
    assert "physique" in char, "Should have mandatory 'physique' axis"
    assert "wealth" in char, "Should have mandatory 'wealth' axis"
    assert len(char) >= 2, "Should have at least 2 axes (mandatory)"

    print(f"  ✓ Basic generation works: {char}")


def test_facial_signal_in_axes() -> None:
    """Test that facial_signal is in CONDITION_AXES."""
    print("\nTesting facial_signal in CONDITION_AXES...")

    from condition_axis import CONDITION_AXES

    assert "facial_signal" in CONDITION_AXES, "facial_signal should be in CONDITION_AXES"

    facial_values = CONDITION_AXES["facial_signal"]
    expected_values = [
        "understated",
        "pronounced",
        "exaggerated",
        "asymmetrical",
        "weathered",
        "soft-featured",
        "sharp-featured",
    ]

    assert set(facial_values) == set(
        expected_values
    ), f"Facial signal values incorrect. Got: {facial_values}"

    print(f"  ✓ facial_signal axis present with {len(facial_values)} values")


def test_facial_signal_in_policy() -> None:
    """Test that facial_signal is in optional axes."""
    print("\nTesting facial_signal in AXIS_POLICY...")

    from condition_axis import AXIS_POLICY

    assert "facial_signal" in AXIS_POLICY["optional"], (
        "facial_signal should be in optional axes"
    )

    optional_axes = AXIS_POLICY["optional"]
    expected_optional = ["health", "demeanor", "age", "facial_signal"]

    assert set(optional_axes) == set(
        expected_optional
    ), f"Optional axes incorrect. Got: {optional_axes}"

    print(f"  ✓ facial_signal in optional axes: {optional_axes}")


def test_facial_signal_has_weights() -> None:
    """Test that facial_signal has weights defined."""
    print("\nTesting facial_signal weights...")

    from condition_axis import WEIGHTS, CONDITION_AXES

    assert "facial_signal" in WEIGHTS, "facial_signal should have weights"

    facial_weights = WEIGHTS["facial_signal"]
    facial_values = set(CONDITION_AXES["facial_signal"])
    weighted_values = set(facial_weights.keys())

    assert (
        facial_values == weighted_values
    ), f"Weight coverage incomplete. Missing: {facial_values - weighted_values}"

    print(f"  ✓ All {len(facial_weights)} facial signal values have weights")


def test_facial_signal_can_be_generated() -> None:
    """Test that facial signals can appear in generated conditions."""
    print("\nTesting facial signal generation...")

    from condition_axis import generate_condition

    facial_signal_found = False
    attempts = 0
    max_attempts = 200

    for seed in range(max_attempts):
        char = generate_condition(seed=seed)
        if "facial_signal" in char:
            facial_signal_found = True
            facial_value = char["facial_signal"]
            print(f"  ✓ Facial signal found at seed {seed}: '{facial_value}'")
            break
        attempts += 1

    if not facial_signal_found:
        raise AssertionError(
            f"No facial signal found in {max_attempts} generations. "
            "Facial signals should appear occasionally as optional axis."
        )


def test_all_facial_signals_can_appear() -> None:
    """Test that all facial signal values can appear over many generations."""
    print("\nTesting all facial signal values can appear...")

    from condition_axis import generate_condition, CONDITION_AXES

    facial_signals_found: set[str] = set()
    max_attempts = 5000

    for seed in range(max_attempts):
        char = generate_condition(seed=seed)
        if "facial_signal" in char:
            facial_signals_found.add(char["facial_signal"])

    expected_signals = set(CONDITION_AXES["facial_signal"])
    missing_signals = expected_signals - facial_signals_found

    if missing_signals:
        print(f"  ⚠ Warning: Missing facial signals after {max_attempts} attempts:")
        for signal in missing_signals:
            print(f"    - {signal}")
        print(f"  Found {len(facial_signals_found)}/{len(expected_signals)} signals")
    else:
        print(
            f"  ✓ All {len(expected_signals)} facial signal values can appear "
            f"(tested with {max_attempts} generations)"
        )


def test_serialization() -> None:
    """Test prompt serialization."""
    print("\nTesting serialization...")

    from condition_axis import generate_condition, condition_to_prompt

    char = generate_condition(seed=42)
    prompt = condition_to_prompt(char)

    assert isinstance(prompt, str), "Prompt should be a string"
    assert len(prompt) > 0, "Prompt should not be empty"
    assert ", " in prompt or len(char) == 1, "Prompt should be comma-separated"

    print(f"  ✓ Serialization works: '{prompt}'")


def test_exclusion_young_weathered() -> None:
    """Test that young age excludes weathered facial signal."""
    print("\nTesting exclusion: young + weathered...")

    from condition_axis import generate_condition

    violations = []
    test_iterations = 500

    for seed in range(test_iterations):
        char = generate_condition(seed=seed)

        # Test young + weathered exclusion
        if char.get("age") == "young" and char.get("facial_signal") == "weathered":
            violations.append(seed)

    if violations:
        print(f"  ✗ Exclusion violated at seeds: {violations}")
        raise AssertionError(f"young + weathered exclusion failed ({len(violations)} violations)")

    print(f"  ✓ Exclusion working (tested {test_iterations} generations)")


def test_exclusion_ancient_understated() -> None:
    """Test that ancient age excludes understated facial signal."""
    print("\nTesting exclusion: ancient + understated...")

    from condition_axis import generate_condition

    violations = []
    test_iterations = 500

    for seed in range(test_iterations):
        char = generate_condition(seed=seed)

        if char.get("age") == "ancient" and char.get("facial_signal") == "understated":
            violations.append(seed)

    if violations:
        print(f"  ✗ Exclusion violated at seeds: {violations}")
        raise AssertionError(
            f"ancient + understated exclusion failed ({len(violations)} violations)"
        )

    print(f"  ✓ Exclusion working (tested {test_iterations} generations)")


def test_exclusion_hale_weathered() -> None:
    """Test that hale health excludes weathered facial signal."""
    print("\nTesting exclusion: hale + weathered...")

    from condition_axis import generate_condition

    violations = []
    test_iterations = 500

    for seed in range(test_iterations):
        char = generate_condition(seed=seed)

        if char.get("health") == "hale" and char.get("facial_signal") == "weathered":
            violations.append(seed)

    if violations:
        print(f"  ✗ Exclusion violated at seeds: {violations}")
        raise AssertionError(f"hale + weathered exclusion failed ({len(violations)} violations)")

    print(f"  ✓ Exclusion working (tested {test_iterations} generations)")


def test_exclusion_decadent_weathered() -> None:
    """Test that decadent wealth excludes weathered facial signal."""
    print("\nTesting exclusion: decadent + weathered...")

    from condition_axis import generate_condition

    violations = []
    test_iterations = 500

    for seed in range(test_iterations):
        char = generate_condition(seed=seed)

        if char.get("wealth") == "decadent" and char.get("facial_signal") == "weathered":
            violations.append(seed)

    if violations:
        print(f"  ✗ Exclusion violated at seeds: {violations}")
        raise AssertionError(
            f"decadent + weathered exclusion failed ({len(violations)} violations)"
        )

    print(f"  ✓ Exclusion working (tested {test_iterations} generations)")


def test_exclusion_sickly_soft_featured() -> None:
    """Test that sickly health excludes soft-featured facial signal."""
    print("\nTesting exclusion: sickly + soft-featured...")

    from condition_axis import generate_condition

    violations = []
    test_iterations = 500

    for seed in range(test_iterations):
        char = generate_condition(seed=seed)

        if char.get("health") == "sickly" and char.get("facial_signal") == "soft-featured":
            violations.append(seed)

    if violations:
        print(f"  ✗ Exclusion violated at seeds: {violations}")
        raise AssertionError(
            f"sickly + soft-featured exclusion failed ({len(violations)} violations)"
        )

    print(f"  ✓ Exclusion working (tested {test_iterations} generations)")


def test_helper_functions() -> None:
    """Test helper functions."""
    print("\nTesting helper functions...")

    from condition_axis import get_available_axes, get_axis_values

    # Test get_available_axes
    axes = get_available_axes()
    assert isinstance(axes, list), "get_available_axes should return a list"
    assert "facial_signal" in axes, "facial_signal should be in available axes"
    assert "physique" in axes, "physique should be in available axes"
    assert "wealth" in axes, "wealth should be in available axes"

    # Test get_axis_values
    facial_values = get_axis_values("facial_signal")
    assert isinstance(facial_values, list), "get_axis_values should return a list"
    assert len(facial_values) == 7, "facial_signal should have 7 values"
    assert "weathered" in facial_values, "weathered should be in facial_signal values"

    print(f"  ✓ Helper functions work: {len(axes)} axes available")


def test_deterministic_generation() -> None:
    """Test that generation is deterministic with seeds."""
    print("\nTesting deterministic generation...")

    from condition_axis import generate_condition

    # Generate twice with same seed
    char1 = generate_condition(seed=12345)
    char2 = generate_condition(seed=12345)

    assert char1 == char2, "Same seed should produce identical results"

    # Generate with different seeds
    char3 = generate_condition(seed=54321)
    # May or may not be different, but should be consistent
    char4 = generate_condition(seed=54321)

    assert char3 == char4, "Same seed should produce identical results"

    print("  ✓ Deterministic generation verified")


def run_all_tests() -> int:
    """Run all smoke tests.

    Returns:
        0 if all tests passed, 1 if any failed.
    """
    tests = [
        test_imports,
        test_deprecated_api_removed,
        test_basic_generation,
        test_facial_signal_in_axes,
        test_facial_signal_in_policy,
        test_facial_signal_has_weights,
        test_facial_signal_can_be_generated,
        test_all_facial_signals_can_appear,
        test_serialization,
        test_exclusion_young_weathered,
        test_exclusion_ancient_understated,
        test_exclusion_hale_weathered,
        test_exclusion_decadent_weathered,
        test_exclusion_sickly_soft_featured,
        test_helper_functions,
        test_deterministic_generation,
    ]

    print("=" * 70)
    print("SMOKE TEST: Facial Conditions Merge")
    print("=" * 70)

    failed_tests = []

    for test_func in tests:
        try:
            test_func()
        except Exception as e:
            print(f"\n  ✗ TEST FAILED: {test_func.__name__}")
            print(f"    Error: {e}")
            failed_tests.append((test_func.__name__, e))

    print("\n" + "=" * 70)

    if failed_tests:
        print(f"✗ {len(failed_tests)} test(s) FAILED:")
        for test_name, error in failed_tests:
            print(f"  - {test_name}: {error}")
        print("=" * 70)
        return 1
    else:
        print("✅ All smoke tests PASSED!")
        print("=" * 70)
        return 0


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
