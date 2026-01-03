"""Custom Axes Example for Pipeworks Conditional Axis.

This example demonstrates how to extend the library by creating
custom condition axis systems. You'll learn:
- The pattern for defining new axis systems
- How to use shared utilities from _base.py
- Creating axes, weights, exclusions, and policies
- Writing generation and serialization functions
- Integrating custom axes with existing systems

This example creates two custom axis systems:
1. Fantasy Magic System (for fantasy RPG contexts)
2. Sci-Fi Technology System (for science fiction contexts)

Run this example:
    python examples/custom_axes.py
"""

import random
from typing import Any

# Import shared utilities from the base module
from condition_axis._base import apply_exclusion_rules, values_to_prompt, weighted_choice


# ============================================================================
# CUSTOM SYSTEM 1: Fantasy Magic Axes
# ============================================================================

# Define possible values for each magic-related axis
MAGIC_AXES: dict[str, list[str]] = {
    "affinity": ["arcane", "divine", "primal", "shadow", "elemental"],
    "proficiency": ["latent", "novice", "adept", "master", "transcendent"],
    "manifestation": ["subtle", "visible", "radiant", "volatile", "catastrophic"],
    "cost": ["effortless", "draining", "painful", "corrupting"],
}

# Define policy: which axes are mandatory vs optional
MAGIC_POLICY: dict[str, Any] = {
    "mandatory": ["affinity", "proficiency"],
    "optional": ["manifestation", "cost"],
    "max_optional": 1,
}

# Define weights for realistic distribution
MAGIC_WEIGHTS: dict[str, dict[str, float]] = {
    "proficiency": {
        "latent": 3.0,  # Most people have latent magic
        "novice": 2.0,
        "adept": 1.5,
        "master": 0.8,
        "transcendent": 0.2,  # Very rare
    },
    "manifestation": {
        "subtle": 2.5,
        "visible": 2.0,
        "radiant": 1.0,
        "volatile": 0.8,
        "catastrophic": 0.3,
    },
}

# Define exclusion rules for semantic coherence
MAGIC_EXCLUSIONS: dict[tuple[str, str], dict[str, list[str]]] = {
    # Latent magic can't have dramatic manifestations
    ("proficiency", "latent"): {
        "manifestation": ["radiant", "volatile", "catastrophic"],
        "cost": ["painful", "corrupting"],
    },
    # Transcendent magic can't be effortless
    ("proficiency", "transcendent"): {
        "cost": ["effortless"],
    },
    # Subtle manifestations can't have high costs
    ("manifestation", "subtle"): {
        "cost": ["painful", "corrupting"],
    },
}


def generate_magic_condition(seed: int | None = None) -> dict[str, str]:
    """Generate magic-related conditions using the axis pattern.

    Args:
        seed: Optional random seed for reproducible generation.

    Returns:
        Dictionary mapping axis names to selected values.

    Example:
        >>> magic = generate_magic_condition(seed=42)
        >>> 'affinity' in magic
        True
        >>> 'proficiency' in magic
        True
    """
    if seed is not None:
        random.seed(seed)

    result: dict[str, str] = {}

    # Select mandatory axes
    for axis in MAGIC_POLICY["mandatory"]:
        options = MAGIC_AXES[axis]
        weights = MAGIC_WEIGHTS.get(axis, None)
        result[axis] = weighted_choice(options, weights)

    # Select optional axes
    optional_axes = MAGIC_POLICY["optional"]
    max_optional = MAGIC_POLICY["max_optional"]

    num_optional = random.randint(0, min(max_optional, len(optional_axes)))
    selected_optional = random.sample(optional_axes, num_optional)

    for axis in selected_optional:
        options = MAGIC_AXES[axis]
        weights = MAGIC_WEIGHTS.get(axis, None)
        result[axis] = weighted_choice(options, weights)

    # Apply exclusion rules
    result = apply_exclusion_rules(result, MAGIC_EXCLUSIONS)

    return result


def magic_condition_to_prompt(magic: dict[str, str]) -> str:
    """Convert magic conditions to comma-separated prompt string.

    Args:
        magic: Magic condition dictionary.

    Returns:
        Comma-separated string of magic conditions.

    Example:
        >>> magic = {"affinity": "arcane", "proficiency": "adept"}
        >>> magic_condition_to_prompt(magic)
        'arcane, adept'
    """
    return values_to_prompt(magic)


# ============================================================================
# CUSTOM SYSTEM 2: Sci-Fi Technology Axes
# ============================================================================

TECH_AXES: dict[str, list[str]] = {
    "augmentation": ["unmodified", "basic", "enhanced", "cybernetic", "synthetic"],
    "tech_access": ["primitive", "standard", "advanced", "cutting-edge", "experimental"],
    "integration": ["natural", "functional", "seamless", "symbiotic"],
    "stability": ["reliable", "glitchy", "unstable", "failing"],
}

TECH_POLICY: dict[str, Any] = {
    "mandatory": ["augmentation", "tech_access"],
    "optional": ["integration", "stability"],
    "max_optional": 2,
}

TECH_WEIGHTS: dict[str, dict[str, float]] = {
    "augmentation": {
        "unmodified": 2.5,
        "basic": 3.0,
        "enhanced": 2.0,
        "cybernetic": 1.0,
        "synthetic": 0.3,
    },
    "tech_access": {
        "primitive": 1.0,
        "standard": 3.5,
        "advanced": 2.0,
        "cutting-edge": 0.8,
        "experimental": 0.2,
    },
}

TECH_EXCLUSIONS: dict[tuple[str, str], dict[str, list[str]]] = {
    # Unmodified can't have integration issues
    ("augmentation", "unmodified"): {
        "integration": ["functional", "seamless", "symbiotic"],
        "stability": ["glitchy", "unstable", "failing"],
    },
    # Synthetic augmentation requires seamless integration
    ("augmentation", "synthetic"): {
        "integration": ["natural"],
        "stability": ["failing"],
    },
    # Primitive tech can't be cutting-edge
    ("tech_access", "primitive"): {
        "integration": ["seamless", "symbiotic"],
    },
}


def generate_tech_condition(seed: int | None = None) -> dict[str, str]:
    """Generate technology-related conditions using the axis pattern.

    Args:
        seed: Optional random seed for reproducible generation.

    Returns:
        Dictionary mapping axis names to selected values.

    Example:
        >>> tech = generate_tech_condition(seed=42)
        >>> 'augmentation' in tech
        True
        >>> 'tech_access' in tech
        True
    """
    if seed is not None:
        random.seed(seed)

    result: dict[str, str] = {}

    # Select mandatory axes
    for axis in TECH_POLICY["mandatory"]:
        options = TECH_AXES[axis]
        weights = TECH_WEIGHTS.get(axis, None)
        result[axis] = weighted_choice(options, weights)

    # Select optional axes
    optional_axes = TECH_POLICY["optional"]
    max_optional = TECH_POLICY["max_optional"]

    num_optional = random.randint(0, min(max_optional, len(optional_axes)))
    selected_optional = random.sample(optional_axes, num_optional)

    for axis in selected_optional:
        options = TECH_AXES[axis]
        weights = TECH_WEIGHTS.get(axis, None)
        result[axis] = weighted_choice(options, weights)

    # Apply exclusion rules
    result = apply_exclusion_rules(result, TECH_EXCLUSIONS)

    return result


def tech_condition_to_prompt(tech: dict[str, str]) -> str:
    """Convert tech conditions to comma-separated prompt string.

    Args:
        tech: Technology condition dictionary.

    Returns:
        Comma-separated string of technology conditions.

    Example:
        >>> tech = {"augmentation": "cybernetic", "tech_access": "advanced"}
        >>> tech_condition_to_prompt(tech)
        'cybernetic, advanced'
    """
    return values_to_prompt(tech)


# ============================================================================
# EXAMPLES
# ============================================================================


def example_1_using_custom_magic_system() -> None:
    """Demonstrate using the custom fantasy magic system."""
    print("=" * 70)
    print("EXAMPLE 1: Custom Fantasy Magic System")
    print("=" * 70)

    print("\nGenerating 5 magical characters:\n")

    for seed in range(5):
        magic = generate_magic_condition(seed=seed)
        prompt = magic_condition_to_prompt(magic)
        print(f"  Character #{seed}: {prompt}")
        print(f"    Raw data: {magic}")


def example_2_using_custom_tech_system() -> None:
    """Demonstrate using the custom sci-fi technology system."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Custom Sci-Fi Technology System")
    print("=" * 70)

    print("\nGenerating 5 tech-augmented characters:\n")

    for seed in range(10, 15):
        tech = generate_tech_condition(seed=seed)
        prompt = tech_condition_to_prompt(tech)
        print(f"  Character #{seed}: {prompt}")
        print(f"    Raw data: {tech}")


def example_3_combining_with_core_systems() -> None:
    """Demonstrate combining custom axes with core library systems."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Combining Custom with Core Systems")
    print("=" * 70)

    from condition_axis import (
        generate_condition,
        generate_facial_condition,
        condition_to_prompt,
        facial_condition_to_prompt,
    )

    print("\nFantasy Character (Core + Magic):\n")

    seed = 42
    character = generate_condition(seed=seed)
    facial = generate_facial_condition(seed=seed)
    magic = generate_magic_condition(seed=seed)

    char_prompt = condition_to_prompt(character)
    face_prompt = facial_condition_to_prompt(facial)
    magic_prompt = magic_condition_to_prompt(magic)

    print(f"  Character: {char_prompt}")
    print(f"  Facial: {face_prompt}")
    print(f"  Magic: {magic_prompt}")
    print(f"\n  Combined: {char_prompt}, {face_prompt}, {magic_prompt}")

    print("\n" + "-" * 70)
    print("\nSci-Fi Character (Core + Tech):\n")

    seed = 99
    character = generate_condition(seed=seed)
    facial = generate_facial_condition(seed=seed)
    tech = generate_tech_condition(seed=seed)

    char_prompt = condition_to_prompt(character)
    face_prompt = facial_condition_to_prompt(facial)
    tech_prompt = tech_condition_to_prompt(tech)

    print(f"  Character: {char_prompt}")
    print(f"  Facial: {face_prompt}")
    print(f"  Tech: {tech_prompt}")
    print(f"\n  Combined: {char_prompt}, {face_prompt}, {tech_prompt}")


def example_4_testing_exclusion_rules() -> None:
    """Demonstrate exclusion rules preventing illogical combinations."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Testing Custom Exclusion Rules")
    print("=" * 70)

    print("\nMagic System Exclusions:")
    print("  Searching for 'latent' proficiency (should have limited manifestation)...\n")

    for seed in range(50):
        magic = generate_magic_condition(seed=seed)
        if magic.get("proficiency") == "latent":
            print(f"  Seed {seed}: {magic}")
            if "manifestation" in magic:
                print(
                    f"    ✓ Manifestation '{magic['manifestation']}' "
                    "is compatible with latent"
                )
            break

    print("\n" + "-" * 70)
    print("\nTech System Exclusions:")
    print("  Searching for 'unmodified' augmentation (should have no integration/stability)...\n")

    for seed in range(50):
        tech = generate_tech_condition(seed=seed)
        if tech.get("augmentation") == "unmodified":
            print(f"  Seed {seed}: {tech}")
            has_integration = "integration" in tech
            has_stability = "stability" in tech
            print(f"    ✓ Has integration axis: {has_integration}")
            print(f"    ✓ Has stability axis: {has_stability}")
            break


def example_5_custom_axis_pattern_summary() -> None:
    """Provide a summary of the pattern for creating custom axes."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Custom Axis Pattern Summary")
    print("=" * 70)

    print("""
╔══════════════════════════════════════════════════════════════════╗
║                 CUSTOM AXIS CREATION PATTERN                     ║
╚══════════════════════════════════════════════════════════════════╝

1. Define AXES Dictionary
   - Maps axis names to lists of possible values
   - Example: {"affinity": ["arcane", "divine", "primal"]}

2. Define POLICY Dictionary
   - Specify mandatory and optional axes
   - Set max_optional to control detail level
   - Example: {"mandatory": ["affinity"], "optional": ["cost"], "max_optional": 1}

3. Define WEIGHTS Dictionary (optional)
   - Assign probability weights to values
   - Creates realistic population distributions
   - Example: {"proficiency": {"novice": 2.0, "master": 0.5}}

4. Define EXCLUSIONS Dictionary (optional)
   - Prevent illogical combinations
   - Format: {(axis, value): {blocked_axis: [blocked_values]}}
   - Example: {("proficiency", "latent"): {"manifestation": ["catastrophic"]}}

5. Write generate_<name>_condition() Function
   - Use weighted_choice() for value selection
   - Use apply_exclusion_rules() for coherence
   - Accept optional seed parameter

6. Write <name>_condition_to_prompt() Function
   - Use values_to_prompt() for serialization
   - Returns comma-separated string

7. Use Shared Utilities from _base.py
   - weighted_choice(options, weights)
   - apply_exclusion_rules(result, exclusions)
   - values_to_prompt(condition_dict)

╔══════════════════════════════════════════════════════════════════╗
║                    READY TO CREATE YOUR OWN!                     ║
╚══════════════════════════════════════════════════════════════════╝

Possible domains to explore:
  - Horror: fear_level, sanity, corruption
  - Modern: tech_savvy, social_media, education
  - Post-apocalypse: survival_skill, mutation, scarcity
  - Maritime: sea_experience, weather_affinity, navigation
  - Academic: knowledge_domain, research_standing, teaching_style
    """)


def main() -> None:
    """Run all custom axes examples.

    This main function executes all examples demonstrating how to
    create and use custom axis systems following the library pattern.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 20 + "CUSTOM AXES EXAMPLES" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_using_custom_magic_system()
    example_2_using_custom_tech_system()
    example_3_combining_with_core_systems()
    example_4_testing_exclusion_rules()
    example_5_custom_axis_pattern_summary()

    print("\n" + "=" * 70)
    print("All custom axes examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - Follow the AXES → POLICY → WEIGHTS → EXCLUSIONS pattern")
    print("  - Use shared utilities from _base.py (weighted_choice, etc.)")
    print("  - Custom axes integrate seamlessly with core systems")
    print("  - Exclusion rules maintain semantic coherence")
    print("  - Pattern works for any domain (fantasy, sci-fi, horror, etc.)")
    print("\nNext Steps:")
    print("  - Try image_prompt_generation.py for visual AI integration")
    print("  - See batch_generation.py for generating many custom entities")
    print("  - Review _base.py to understand shared utilities")
    print()


if __name__ == "__main__":
    main()
