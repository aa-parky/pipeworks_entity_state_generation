"""Integration Example for Pipeworks Conditional Axis.

This example demonstrates how to integrate all three axis systems:
- Character conditions (physical and social state)
- Facial conditions (perception modifiers)
- Occupation conditions (labor pressures and positioning)

Together, these systems create rich, coherent entity descriptions
suitable for both visual generation and narrative contexts.

Run this example:
    python examples/integration_example.py
"""

from typing import Any

from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
    occupation_condition_to_prompt,
)

# ============================================================================
# NOTE: Unified API for Facial Conditions (v1.1.0+)
# ============================================================================
# As of v1.1.0, facial conditions are integrated into character_conditions.
# The separate generate_facial_condition() function is now deprecated but
# maintained for backward compatibility. For new code, facial signals are
# automatically included in generate_condition() as an optional axis.
#
# Old approach (still works, used in this example):
#   character = generate_condition(seed=42)
#   facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
#   combined = f"{condition_to_prompt(character)}, {condition_to_prompt(facial)}"
#
# New approach (recommended):
#   character = generate_condition(seed=42)  # May include facial_signal
#   prompt = condition_to_prompt(character)  # Automatically includes facial_signal
#
# This example uses the old API to demonstrate backward compatibility.
# See examples/migration_guide.py for migration patterns.
# ============================================================================


def example_1_complete_entity_generation() -> None:
    """Demonstrate generating a complete entity with all three systems.

    Using the same seed across all three systems ensures consistency
    in the random number generator state, though each system operates
    independently.
    """
    print("=" * 70)
    print("EXAMPLE 1: Complete Entity Generation")
    print("=" * 70)

    seed = 42

    # Generate all three condition types with the same seed
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    print(f"\nEntity (seed={seed}):")
    print(f"\nCharacter Conditions: {character}")
    print(f"Facial Conditions: {facial}")
    print(f"Occupation Conditions: {occupation}")

    # Convert to prompts
    char_prompt = condition_to_prompt(character)
    face_prompt = condition_to_prompt(facial)
    occ_prompt = occupation_condition_to_prompt(occupation)

    print(f"\nSerialized Prompts:")
    print(f"  Character: {char_prompt}")
    print(f"  Facial: {face_prompt}")
    print(f"  Occupation: {occ_prompt}")

    # Combined prompt for image generation or narrative
    full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
    print(f"\nCombined Prompt:")
    print(f"  '{full_prompt}'")


def example_2_multiple_complete_entities() -> None:
    """Demonstrate generating a population of complete entities.

    Each entity gets a unique seed to ensure distinct characteristics
    across all three systems.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Multiple Complete Entities")
    print("=" * 70)

    entities = []
    for seed in range(5):
        char = generate_condition(seed=seed)
        entity = {
            "seed": seed,
            "character": char,
            "facial": {"facial_signal": char.get("facial_signal", "")} if "facial_signal" in char else {},
            "occupation": generate_occupation_condition(seed=seed),
        }
        entities.append(entity)

    print("\nGenerated Population (5 entities):\n")

    for entity in entities:
        seed = entity["seed"]
        char_prompt = condition_to_prompt(entity["character"])
        face_prompt = condition_to_prompt(entity["facial"])
        occ_prompt = occupation_condition_to_prompt(entity["occupation"])

        full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"

        print(f"Entity #{seed}: {full_prompt}")


def example_3_narrative_vs_visual_formatting() -> None:
    """Demonstrate different formatting for narrative vs visual contexts.

    The same underlying data can be formatted differently depending
    on whether it's used for:
    - AI image generation (comma-separated keywords)
    - Narrative description (natural language)
    - Data storage (structured dict)
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Narrative vs Visual Formatting")
    print("=" * 70)

    seed = 777

    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    # 1. Structured data (for storage/transmission)
    print("\n1. STRUCTURED DATA (JSON-ready):")
    structured = {
        "character": character,
        "facial": facial,
        "occupation": occupation,
    }
    print(f"   {structured}")

    # 2. Visual prompt (for image generation)
    print("\n2. VISUAL PROMPT (for Stable Diffusion, DALL-E, etc.):")
    char_prompt = condition_to_prompt(character)
    face_prompt = condition_to_prompt(facial)
    occ_prompt = occupation_condition_to_prompt(occupation)
    visual_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
    print(f"   '{visual_prompt}'")

    # 3. Narrative description (for text-based content)
    print("\n3. NARRATIVE DESCRIPTION (for MUDs, interactive fiction):")
    narrative = format_as_narrative(character, facial, occupation)
    print(f"   {narrative}")


def format_as_narrative(
    character: dict[str, str],
    facial: dict[str, str],
    occupation: dict[str, str],
) -> str:
    """Convert conditions to natural language narrative description.

    Args:
        character: Character condition dictionary (may include facial_signal as of v1.1.0).
        facial: Facial condition dictionary (deprecated, kept for backward compatibility).
        occupation: Occupation condition dictionary.

    Returns:
        Natural language description suitable for narrative contexts.

    Example:
        >>> char = {"physique": "wiry", "wealth": "poor", "facial_signal": "weathered"}
        >>> facial = {}  # Optional, for backward compat
        >>> occ = {"legitimacy": "tolerated", "visibility": "discreet"}
        >>> format_as_narrative(char, facial, occ)
        "A wiry, poor individual with a weathered face..."

    Note:
        As of v1.1.0, facial_signal can be in the character dict (unified API).
        This function checks both locations for backward compatibility.
    """
    # Extract key values
    physique = character.get("physique", "")
    wealth = character.get("wealth", "")
    health = character.get("health", "")

    # NEW: Check for facial_signal in character dict first (unified API),
    # then fall back to facial dict (old API for backward compatibility)
    facial_signal = character.get("facial_signal") or facial.get("facial_signal", "")

    legitimacy = occupation.get("legitimacy", "")
    visibility = occupation.get("visibility", "")

    # Build narrative
    parts = []

    # Physical description
    if physique and wealth:
        parts.append(f"A {physique}, {wealth} individual")
    elif physique:
        parts.append(f"A {physique} individual")

    # Facial features (updated to use facial_signal instead of overall_impression)
    if facial_signal:
        parts.append(f"with a {facial_signal} face")

    # Health and demeanor
    if health:
        parts.append(f"bearing signs of being {health}")

    # Occupation characteristics
    occ_parts = []
    if legitimacy:
        occ_parts.append(f"{legitimacy} work")
    if visibility:
        occ_parts.append(f"{visibility} presence")

    if occ_parts:
        parts.append(f"whose {' and '.join(occ_parts)} suggests careful positioning")

    return ". ".join(parts) + "."


def example_4_identifying_coherence_patterns() -> None:
    """Demonstrate how to identify coherent vs incoherent combinations.

    While each system operates independently, some cross-system
    combinations create more or less coherent narratives.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Identifying Coherence Patterns")
    print("=" * 70)

    print("\nSearching for interesting combinations (seeds 0-50)...")

    interesting_cases = []

    for seed in range(50):
        character = generate_condition(seed=seed)
        facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
        occupation = generate_occupation_condition(seed=seed)

        # Look for specific patterns
        is_wealthy_illicit = (
            character.get("wealth") in ["wealthy", "decadent"]
            and occupation.get("legitimacy") == "illicit"
        )

        is_young_weathered = (
            character.get("age") == "young" and facial.get("facial_signal") == "weathered"
        )

        is_conspicuous_hidden = (
            occupation.get("visibility") == "hidden" and character.get("demeanor") == "proud"
        )

        if is_wealthy_illicit or is_young_weathered or is_conspicuous_hidden:
            interesting_cases.append(
                {
                    "seed": seed,
                    "character": character,
                    "facial": facial,
                    "occupation": occupation,
                    "pattern": (
                        "wealthy_illicit"
                        if is_wealthy_illicit
                        else "young_weathered" if is_young_weathered else "contradictory"
                    ),
                }
            )

    print(f"\nFound {len(interesting_cases)} interesting patterns:\n")

    for case in interesting_cases[:3]:  # Show first 3
        seed = case["seed"]
        pattern = case["pattern"]
        char_prompt = condition_to_prompt(case["character"])
        face_prompt = condition_to_prompt(case["facial"])
        occ_prompt = occupation_condition_to_prompt(case["occupation"])

        print(f"Seed {seed} ({pattern}):")
        print(f"  {char_prompt}, {face_prompt}, {occ_prompt}")
        print()


def example_5_entity_archetype_generation() -> None:
    """Demonstrate generating entities that fit specific archetypes.

    By generating many entities and filtering for desired traits,
    you can find entities that match specific narrative archetypes.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Entity Archetype Generation")
    print("=" * 70)

    archetypes = {
        "The Desperate Outlaw": {
            "character": lambda c: c.get("wealth") == "poor"
            and c.get("health") in ["weary", "scarred"],
            "occupation": lambda o: o.get("legitimacy") == "illicit"
            and o.get("risk_exposure") in ["hazardous", "eroding"],
        },
        "The Respected Merchant": {
            "character": lambda c: c.get("wealth") in ["wealthy", "well-kept"]
            and c.get("demeanor") in ["alert", "proud"],
            "occupation": lambda o: o.get("legitimacy") == "sanctioned"
            and o.get("visibility") == "routine",
        },
        "The Hidden Scholar": {
            "character": lambda c: c.get("wealth") in ["poor", "modest"]
            and c.get("physique") in ["skinny", "wiry", "hunched"],
            "occupation": lambda o: o.get("visibility") == "hidden"
            and o.get("moral_load") in ["neutral", "burdened"],
        },
    }

    print("\nSearching for archetype matches (seeds 0-1000000)...\n")

    for archetype_name, criteria in archetypes.items():
        print(f"=== {archetype_name} ===")

        found = False
        for seed in range(1000000):
            character = generate_condition(seed=seed)
            facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
            occupation = generate_occupation_condition(seed=seed)

            char_match = criteria["character"](character)
            occ_match = criteria["occupation"](occupation)

            if char_match and occ_match:
                char_prompt = condition_to_prompt(character)
                face_prompt = condition_to_prompt(facial)
                occ_prompt = occupation_condition_to_prompt(occupation)

                print(f"  Seed {seed}: {char_prompt}, {face_prompt}, {occ_prompt}")
                found = True
                break

        if not found:
            print(f"  No match found in seeds 0-1000000")
        print()


def main() -> None:
    """Run all integration examples.

    This main function executes all examples demonstrating how to
    combine character, facial, and occupation condition systems
    for complete entity generation.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 17 + "INTEGRATION EXAMPLES" + " " * 31 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_complete_entity_generation()
    example_2_multiple_complete_entities()
    example_3_narrative_vs_visual_formatting()
    example_4_identifying_coherence_patterns()
    example_5_entity_archetype_generation()

    print("\n" + "=" * 70)
    print("All integration examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - All three systems can be combined with the same seed")
    print("  - Each system operates independently but creates coherent wholes")
    print("  - Same data can be formatted for visual or narrative contexts")
    print("  - Cross-system patterns emerge from independent generation")
    print("  - Archetype filtering enables targeted entity discovery")
    print("\nNext Steps:")
    print("  - Try batch_generation.py for efficient bulk generation")
    print("  - Try custom_axes.py for extending the system")
    print("  - See image_prompt_generation.py for visual AI integration")
    print()


if __name__ == "__main__":
    main()
