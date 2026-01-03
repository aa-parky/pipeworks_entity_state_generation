"""Advanced Usage Example for Pipeworks Conditional Axis.

This example demonstrates advanced concepts:
- Understanding weighted probability distributions
- How exclusion rules prevent illogical combinations
- Analyzing generation patterns and statistics
- Accessing raw data structures (AXES, WEIGHTS, EXCLUSIONS)
- Understanding mandatory vs optional axes

Run this example:
    python examples/advanced_usage.py
"""

from collections import Counter
from typing import Any

from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
)

# Import internal data structures for inspection
from condition_axis.character_conditions import (
    CONDITION_AXES,
    WEIGHTS,
    EXCLUSIONS,
    AXIS_POLICY,
)


def example_1_understanding_weights() -> None:
    """Demonstrate how weighted distributions affect generation.

    The library uses realistic population weights rather than
    uniform randomness. This creates believable populations where
    most characters are poor or modest, and few are wealthy.
    """
    print("=" * 70)
    print("EXAMPLE 1: Understanding Weighted Distributions")
    print("=" * 70)

    # Show wealth axis weights
    print("\nWealth Axis Weights:")
    wealth_weights = WEIGHTS.get("wealth", {})
    for value, weight in sorted(wealth_weights.items(), key=lambda x: -x[1]):
        bar = "█" * int(weight * 10)
        print(f"  {value:12} ({weight:3.1f}): {bar}")

    # Generate 1000 characters to demonstrate distribution
    print("\nGenerating 1000 characters to demonstrate distribution...")
    wealth_counts: Counter[str] = Counter()

    for seed in range(1000):
        char = generate_condition(seed=seed)
        if "wealth" in char:
            wealth_counts[char["wealth"]] += 1

    print("\nGenerated Wealth Distribution (out of 1000):")
    total = sum(wealth_counts.values())
    for value, count in sorted(wealth_counts.items(), key=lambda x: -x[1]):
        percentage = (count / total) * 100
        bar = "█" * int(percentage)
        print(f"  {value:12} ({count:4}): {bar} {percentage:.1f}%")

    print("\nNotice how the distribution matches the weights!")


def example_2_exclusion_rules_in_action() -> None:
    """Demonstrate how exclusion rules prevent illogical combinations.

    Exclusion rules enforce semantic coherence:
    - Decadent wealth → no frail/sickly conditions
    - Ancient age → no timid demeanor
    - Broad physique → no sickly health

    These prevent nonsense while maintaining variety.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Exclusion Rules in Action")
    print("=" * 70)

    # Show some key exclusion rules
    print("\nKey Exclusion Rules:")
    print("  ('wealth', 'decadent') blocks:")
    if ("wealth", "decadent") in EXCLUSIONS:
        for axis, values in EXCLUSIONS[("wealth", "decadent")].items():
            print(f"    {axis}: {values}")

    print("\n  ('age', 'ancient') blocks:")
    if ("age", "ancient") in EXCLUSIONS:
        for axis, values in EXCLUSIONS[("age", "ancient")].items():
            print(f"    {axis}: {values}")

    # Try to find combinations that would violate exclusions
    print("\nSearching for decadent characters (seed 0-200)...")
    decadent_chars = []

    for seed in range(200):
        char = generate_condition(seed=seed)
        if char.get("wealth") == "decadent":
            decadent_chars.append((seed, char))
            if len(decadent_chars) >= 3:
                break

    print("\nDecadent Characters Found:")
    for seed, char in decadent_chars:
        print(f"  Seed {seed:3}: {condition_to_prompt(char)}")
        health = char.get("health", "N/A")
        physique = char.get("physique", "N/A")
        print(f"    → Health: {health}, Physique: {physique}")
        print(f"    → Notice: NO 'frail' or 'sickly' despite wealth allowing it")


def example_3_mandatory_vs_optional_axes() -> None:
    """Demonstrate the difference between mandatory and optional axes.

    Character conditions:
    - Mandatory: physique, wealth (always present)
    - Optional: health, demeanor, age (0-2 selected randomly)

    This prevents prompt dilution while maintaining variety.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Mandatory vs Optional Axes")
    print("=" * 70)

    # Show policy
    print("\nCharacter Condition Policy:")
    print(f"  Mandatory axes: {AXIS_POLICY['mandatory']}")
    print(f"  Optional axes: {AXIS_POLICY['optional']}")
    print(f"  Max optional: {AXIS_POLICY['max_optional']}")

    # Generate 20 characters to show variety
    print("\nGenerating 20 characters to show axis variety:")
    print("(M = Mandatory, O = Optional)\n")

    for seed in range(20):
        char = generate_condition(seed=seed)
        axes_present = set(char.keys())

        mandatory_count = len(axes_present & set(AXIS_POLICY["mandatory"]))
        optional_count = len(axes_present & set(AXIS_POLICY["optional"]))

        print(f"  Seed {seed:2}: {len(axes_present)} axes | ", end="")
        print(f"M={mandatory_count} O={optional_count} | ", end="")
        print(f"{', '.join(char.keys())}")


def example_4_analyzing_generation_patterns() -> None:
    """Demonstrate analysis of generation patterns.

    By generating many entities and analyzing the results,
    we can verify the system behaves as expected:
    - Weighted distributions are respected
    - Exclusions are enforced
    - Variety is maintained
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Analyzing Generation Patterns")
    print("=" * 70)

    # Generate 500 characters and analyze
    sample_size = 500
    print(f"\nGenerating {sample_size} characters for analysis...")

    physique_counts: Counter[str] = Counter()
    health_counts: Counter[str] = Counter()
    age_counts: Counter[str] = Counter()
    total_axes_count: Counter[int] = Counter()

    for seed in range(sample_size):
        char = generate_condition(seed=seed)

        if "physique" in char:
            physique_counts[char["physique"]] += 1
        total_axes_count[len(char)] += 1

        if "health" in char:
            health_counts[char["health"]] += 1
        if "age" in char:
            age_counts[char["age"]] += 1

    # Report statistics
    print("\nPhysique Distribution:")
    for value, count in physique_counts.most_common():
        print(f"  {value:10} : {count:4} ({count/sample_size*100:5.1f}%)")

    print("\nTotal Axes Count (Mandatory + Optional):")
    for count, freq in sorted(total_axes_count.items()):
        bar = "█" * int(freq / 10)
        print(f"  {count} axes: {freq:4} {bar}")

    print("\nOptional Axes Appearance Rate:")
    print(
        f"  Health: {len(health_counts):4} / {sample_size} ({len(health_counts)/sample_size*100:.1f}%)"
    )  # noqa: E501
    print(
        f"  Age: {len(age_counts):4} / {sample_size} ({len(age_counts)/sample_size*100:.1f}%)"
    )  # noqa: E501


def example_5_cross_system_exclusions() -> None:
    """Demonstrate cross-system exclusion rules with facial signals.

    As of v1.1.0, facial signals are integrated into character generation,
    with exclusion rules preventing illogical combinations across systems.

    This example tests the cross-system exclusion rule:
    - young age cannot be paired with weathered facial signal
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Cross-System Exclusions (Character + Facial)")
    print("=" * 70)

    print("\nTesting exclusion: young age cannot be weathered")
    print("Generating 1000 characters...\n")

    young_chars = []
    for seed in range(1000):
        char = generate_condition(seed=seed)
        if char.get("age") == "young":
            young_chars.append(char)

    print(f"Found {len(young_chars)} young characters")

    # Check if any have weathered facial signal (should be 0)
    weathered_count = sum(1 for c in young_chars if c.get("facial_signal") == "weathered")

    print(f"Weathered young characters: {weathered_count} (should be 0)")

    if weathered_count == 0:
        print("✓ Exclusion rule working correctly!")
    else:
        print("✗ Exclusion rule violation detected!")

    # Show what facial signals young characters DO have
    if young_chars:
        facial_signals = [c.get("facial_signal") for c in young_chars if "facial_signal" in c]
        if facial_signals:
            signal_counts = Counter(facial_signals)
            print(f"\nFacial signals found in young characters:")
            for signal, count in signal_counts.most_common():
                print(f"  {signal}: {count}")


def example_6_inspecting_raw_data() -> None:
    """Demonstrate accessing and inspecting raw data structures.

    Advanced users can access:
    - CONDITION_AXES: All possible values for each axis
    - WEIGHTS: Probability weights for each value
    - EXCLUSIONS: Rules preventing illogical combinations
    - AXIS_POLICY: Mandatory/optional axis configuration
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Inspecting Raw Data Structures")
    print("=" * 70)

    print("\nAvailable Axes and Values:")
    for axis, values in CONDITION_AXES.items():
        print(f"  {axis:10} : {', '.join(values)}")

    print("\nWeighted Axes:")
    for axis in WEIGHTS.keys():
        weight_count = len(WEIGHTS[axis])
        print(f"  {axis:10} : {weight_count} weighted values")

    print("\nExclusion Rules Count:")
    print(f"  Total trigger conditions: {len(EXCLUSIONS)}")

    print("\nExample Exclusion:")
    example_key = list(EXCLUSIONS.keys())[0]
    example_exclusions = EXCLUSIONS[example_key]
    print(f"  When {example_key}:")
    for axis, blocked_values in example_exclusions.items():
        print(f"    Block {axis}: {blocked_values}")


def main() -> None:
    """Run all advanced usage examples.

    This main function executes all advanced examples,
    demonstrating deeper understanding of the Pipeworks
    Conditional Axis library's internal mechanisms.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 18 + "ADVANCED USAGE EXAMPLES" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_understanding_weights()
    example_2_exclusion_rules_in_action()
    example_3_mandatory_vs_optional_axes()
    example_4_analyzing_generation_patterns()
    example_5_cross_system_exclusions()
    example_6_inspecting_raw_data()

    print("\n" + "=" * 70)
    print("All advanced examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - Weighted distributions create realistic populations")
    print("  - Exclusion rules enforce semantic coherence")
    print("  - Mandatory/optional axes balance detail and clarity")
    print("  - Raw data structures are accessible for inspection")
    print("\nNext Steps:")
    print("  - Try integration_example.py for combining all systems")
    print("  - Try custom_axes.py for extending the library")
    print()


if __name__ == "__main__":
    main()
