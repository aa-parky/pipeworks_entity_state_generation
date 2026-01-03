"""Basic Usage Example for Pipeworks Conditional Axis.

This example demonstrates the simplest use cases for the library:
- Generating character conditions
- Generating facial conditions
- Generating occupation conditions
- Converting conditions to prompt-ready strings
- Understanding reproducibility with seeds

Run this example:
    python examples/basic_usage.py
"""

from condition_axis import (
    generate_condition,
    generate_facial_condition,
    generate_occupation_condition,
    condition_to_prompt,
    facial_condition_to_prompt,
    occupation_condition_to_prompt,
)


def example_1_simple_generation() -> None:
    """Demonstrate simple condition generation without seeds.

    Generates conditions for character, facial, and occupation systems
    without specifying seeds, resulting in random output each time.
    """
    print("=" * 70)
    print("EXAMPLE 1: Simple Generation (Random)")
    print("=" * 70)

    # Generate character conditions (random)
    character = generate_condition()
    print(f"\nCharacter Conditions: {character}")

    # Generate facial conditions (random)
    facial = generate_facial_condition()
    print(f"Facial Conditions: {facial}")

    # Generate occupation conditions (random)
    occupation = generate_occupation_condition()
    print(f"Occupation Conditions: {occupation}")


def example_2_reproducible_generation() -> None:
    """Demonstrate reproducible generation using seeds.

    Using the same seed value produces identical output every time,
    which is useful for:
    - Testing
    - Debugging
    - Saving and recreating specific entities
    - Ensuring consistency across systems
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Reproducible Generation (With Seeds)")
    print("=" * 70)

    seed_value = 42

    # Generate with seed
    char1 = generate_condition(seed=seed_value)
    char2 = generate_condition(seed=seed_value)

    print(f"\nFirst generation (seed={seed_value}): {char1}")
    print(f"Second generation (seed={seed_value}): {char2}")
    print(f"Are they identical? {char1 == char2}")

    # Different seeds produce different results
    char3 = generate_condition(seed=123)
    print(f"\nDifferent seed (seed=123): {char3}")
    print(f"Are they different? {char1 != char3}")


def example_3_serialization_to_prompts() -> None:
    """Demonstrate converting conditions to prompt-ready strings.

    The library provides serialization functions that convert
    structured condition dictionaries into comma-separated strings
    suitable for:
    - AI image generation prompts
    - Narrative text
    - Character descriptions
    - Data export
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Serialization to Prompts")
    print("=" * 70)

    seed = 99

    # Generate conditions
    character = generate_condition(seed=seed)
    facial = generate_facial_condition(seed=seed)
    occupation = generate_occupation_condition(seed=seed)

    print("\nStructured Data:")
    print(f"  Character: {character}")
    print(f"  Facial: {facial}")
    print(f"  Occupation: {occupation}")

    # Convert to prompt strings
    char_prompt = condition_to_prompt(character)
    face_prompt = facial_condition_to_prompt(facial)
    occ_prompt = occupation_condition_to_prompt(occupation)

    print("\nSerialized Prompts:")
    print(f"  Character: '{char_prompt}'")
    print(f"  Facial: '{face_prompt}'")
    print(f"  Occupation: '{occ_prompt}'")

    # Combine for complete description
    full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
    print(f"\nCombined: '{full_prompt}'")


def example_4_understanding_axes() -> None:
    """Demonstrate understanding the axis structure.

    Each condition system organizes state along multiple axes.
    This example shows what axes are available and how they
    can be combined.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Understanding Axes")
    print("=" * 70)

    seed = 777

    # Character conditions have 5 axes
    character = generate_condition(seed=seed)
    print("\nCharacter Axes:")
    for axis, value in character.items():
        print(f"  {axis}: {value}")

    # Facial conditions have 1 axis
    facial = generate_facial_condition(seed=seed)
    print("\nFacial Axes:")
    for axis, value in facial.items():
        print(f"  {axis}: {value}")

    # Occupation conditions have 5 axes
    occupation = generate_occupation_condition(seed=seed)
    print("\nOccupation Axes:")
    for axis, value in occupation.items():
        print(f"  {axis}: {value}")


def example_5_multiple_entities() -> None:
    """Demonstrate generating multiple distinct entities.

    Each entity needs a unique seed to ensure different characteristics.
    This example shows how to generate a population of diverse entities.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Multiple Distinct Entities")
    print("=" * 70)

    # Generate three different characters
    characters = [
        (1, generate_condition(seed=1)),
        (2, generate_condition(seed=2)),
        (3, generate_condition(seed=3)),
    ]

    print("\nThree Distinct Characters:")
    for char_id, char_data in characters:
        prompt = condition_to_prompt(char_data)
        print(f"  Character #{char_id}: {prompt}")


def main() -> None:
    """Run all basic usage examples.

    This main function executes all examples in sequence,
    demonstrating the core functionality of the Pipeworks
    Conditional Axis library.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 20 + "BASIC USAGE EXAMPLES" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_simple_generation()
    example_2_reproducible_generation()
    example_3_serialization_to_prompts()
    example_4_understanding_axes()
    example_5_multiple_entities()

    print("\n" + "=" * 70)
    print("All examples completed successfully!")
    print("=" * 70)
    print("\nNext Steps:")
    print("  - Try advanced_usage.py for custom weights and exclusions")
    print("  - Try integration_example.py for combining all systems")
    print("  - See documentation: docs/")
    print()


if __name__ == "__main__":
    main()
