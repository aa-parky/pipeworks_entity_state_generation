"""Image Prompt Generation Example for Pipeworks Conditional Axis.

This example demonstrates integration with AI image generation tools:
- Converting conditions to optimized image prompts
- Adding style modifiers and quality tags
- Constructing negative prompts
- Prompt engineering best practices
- Integration patterns for Stable Diffusion, DALL-E, Midjourney
- Batch prompt generation for consistent character sets

Run this example:
    python examples/image_prompt_generation.py
"""

from typing import Any

from condition_axis import (
    generate_condition,
    generate_occupation_condition,
    condition_to_prompt,
    occupation_condition_to_prompt,
)


def build_full_prompt(
    character: dict[str, str],
    facial: dict[str, str],
    occupation: dict[str, str],
    style: str = "",
    quality_tags: list[str] | None = None,
    additional_details: str = "",
) -> str:
    """Build a complete image generation prompt from conditions.

    Args:
        character: Character condition dictionary.
        facial: Facial condition dictionary.
        occupation: Occupation condition dictionary.
        style: Optional style modifier (e.g., "oil painting", "3d render").
        quality_tags: Optional quality/technical tags.
        additional_details: Optional additional descriptive text.

    Returns:
        Complete prompt string optimized for image generation.

    Example:
        >>> char = {"physique": "wiry", "wealth": "poor"}
        >>> facial = {"overall_impression": "weathered"}
        >>> occ = {"legitimacy": "tolerated"}
        >>> build_full_prompt(char, facial, occ, style="portrait")
        'portrait, wiry, poor, weathered, tolerated, ...'
    """
    # Convert conditions to prompts
    char_prompt = condition_to_prompt(character)
    face_prompt = condition_to_prompt(facial)
    occ_prompt = occupation_condition_to_prompt(occupation)

    # Combine base components
    parts = [char_prompt, face_prompt, occ_prompt]

    # Add additional details if provided
    if additional_details:
        parts.append(additional_details)

    # Add style modifier
    if style:
        parts.insert(0, style)

    # Add quality tags
    if quality_tags:
        parts.extend(quality_tags)

    # Join with comma separation
    return ", ".join(filter(None, parts))


def build_negative_prompt(avoid_traits: list[str] | None = None) -> str:
    """Build a negative prompt for image generation.

    Negative prompts tell the model what NOT to generate.
    Common for Stable Diffusion and similar tools.

    Args:
        avoid_traits: Specific traits to avoid in generation.

    Returns:
        Comma-separated negative prompt string.

    Example:
        >>> build_negative_prompt(["cartoonish", "anime"])
        'cartoonish, anime, low quality, ...'
    """
    # Common quality issues to avoid
    base_negatives = [
        "low quality",
        "blurry",
        "distorted",
        "deformed",
        "duplicate",
        "watermark",
    ]

    if avoid_traits:
        base_negatives.extend(avoid_traits)

    return ", ".join(base_negatives)


def example_1_basic_image_prompt() -> None:
    """Demonstrate converting conditions to a basic image prompt."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Image Prompt Generation")
    print("=" * 70)

    seed = 42
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    print("\nGenerated Conditions:")
    print(f"  Character: {character}")
    print(f"  Facial: {facial}")
    print(f"  Occupation: {occupation}")

    # Basic prompt
    basic_prompt = build_full_prompt(character, facial, occupation)

    print("\nBasic Image Prompt:")
    print(f"  '{basic_prompt}'")

    print("\nThis prompt can be used directly in:")
    print("  - Stable Diffusion")
    print("  - DALL-E 3")
    print("  - Midjourney")
    print("  - Any text-to-image model")


def example_2_styled_prompts() -> None:
    """Demonstrate adding style modifiers to prompts."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Styled Image Prompts")
    print("=" * 70)

    seed = 99
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    styles = [
        "portrait photograph",
        "oil painting",
        "pencil sketch",
        "3d render, octane",
        "watercolor illustration",
        "digital art, concept art",
    ]

    print("\nSame character in different styles:\n")

    for style in styles:
        prompt = build_full_prompt(character, facial, occupation, style=style)
        print(f"  {style.upper()}:")
        print(f"    {prompt}\n")


def example_3_quality_enhanced_prompts() -> None:
    """Demonstrate adding quality tags for better results."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Quality-Enhanced Prompts")
    print("=" * 70)

    seed = 777
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    # Different quality tag sets for different needs
    quality_presets = {
        "Photorealistic": [
            "highly detailed",
            "8k resolution",
            "photorealistic",
            "professional photography",
        ],
        "Artistic": [
            "masterpiece",
            "trending on artstation",
            "award winning",
            "high detail",
        ],
        "Fantasy": [
            "fantasy art",
            "dramatic lighting",
            "epic composition",
            "detailed",
        ],
    }

    print("\nSame character with different quality presets:\n")

    for preset_name, quality_tags in quality_presets.items():
        prompt = build_full_prompt(
            character, facial, occupation, style="portrait", quality_tags=quality_tags
        )
        print(f"  {preset_name.upper()} PRESET:")
        print(f"    {prompt}\n")


def example_4_with_negative_prompts() -> None:
    """Demonstrate using negative prompts for better control."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Positive and Negative Prompts")
    print("=" * 70)

    seed = 123
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    # Build positive prompt
    positive_prompt = build_full_prompt(
        character,
        facial,
        occupation,
        style="realistic portrait photograph",
        quality_tags=["highly detailed", "professional lighting"],
    )

    # Build negative prompt
    negative_prompt = build_negative_prompt(
        avoid_traits=["cartoon", "anime", "illustration", "painting"]
    )

    print("\nPOSITIVE PROMPT (what to generate):")
    print(f"  {positive_prompt}")

    print("\nNEGATIVE PROMPT (what to avoid):")
    print(f"  {negative_prompt}")

    print("\nUsage in Stable Diffusion Web UI:")
    print("  - Paste positive prompt in the main prompt box")
    print("  - Paste negative prompt in the negative prompt box")
    print("  - Adjust CFG scale (7-12 recommended)")
    print("  - Use sampling steps: 20-50")


def example_5_batch_prompt_generation() -> None:
    """Demonstrate generating a batch of prompts for a character set."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Batch Prompt Generation")
    print("=" * 70)

    print("\nGenerating prompts for a party of 4 adventurers:\n")

    base_style = "fantasy character portrait"
    quality_tags = ["detailed", "dramatic lighting", "trending on artstation"]

    for i in range(4):
        seed = 1000 + i
        character = generate_condition(seed=seed)
        facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
        occupation = generate_occupation_condition(seed=seed)

        prompt = build_full_prompt(
            character, facial, occupation, style=base_style, quality_tags=quality_tags
        )

        print(f"ADVENTURER {i + 1} (seed={seed}):")
        print(f"  {prompt}\n")

    print("These prompts maintain consistent style while varying character traits.")


def example_6_context_specific_additions() -> None:
    """Demonstrate adding context-specific details to prompts."""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Context-Specific Additions")
    print("=" * 70)

    seed = 456
    character = generate_condition(seed=seed)
    facial = {"facial_signal": character.get("facial_signal", "")} if "facial_signal" in character else {}
    occupation = generate_occupation_condition(seed=seed)

    contexts = {
        "Tavern Scene": "standing in a medieval tavern, warm firelight, wooden interior",
        "Market Square": "in a busy marketplace, merchant stall background, daytime",
        "Dark Alley": "in a shadowy alley, foggy atmosphere, nighttime, ominous",
        "Throne Room": "in an ornate throne room, marble columns, regal setting",
    }

    print("\nSame character in different contexts:\n")

    for context_name, context_details in contexts.items():
        prompt = build_full_prompt(
            character,
            facial,
            occupation,
            style="cinematic portrait",
            additional_details=context_details,
        )

        print(f"  {context_name.upper()}:")
        print(f"    {prompt}\n")


def example_7_prompt_engineering_tips() -> None:
    """Provide prompt engineering tips and best practices."""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Prompt Engineering Best Practices")
    print("=" * 70)

    print(
        """
╔══════════════════════════════════════════════════════════════════╗
║              IMAGE GENERATION PROMPT BEST PRACTICES              ║
╚══════════════════════════════════════════════════════════════════╝

1. Structure Your Prompt
   Order matters! Use this structure:
   [Style] → [Subject traits] → [Context] → [Quality tags]

   Example:
   "portrait photograph, wiry, weathered, standing in tavern, highly detailed"

2. Be Specific but Concise
   ✓ Good: "wiry physique, weathered face"
   ✗ Bad: "a person who looks like they have a thin build"

3. Use Comma Separation
   Commas help models parse different concepts:
   "portrait, medieval, detailed, dramatic lighting"

4. Quality Tags (Stable Diffusion)
   - "highly detailed" - more detail
   - "8k resolution" - high resolution
   - "masterpiece" - quality bias
   - "trending on artstation" - artistic style bias

5. Style Modifiers
   - "portrait photograph" - photorealistic style
   - "oil painting" - traditional art
   - "digital art" - modern digital style
   - "3d render, octane" - 3D CGI style

6. Negative Prompts (Stable Diffusion)
   Essential for avoiding:
   - "low quality, blurry, distorted"
   - "cartoon, anime" (if you want realism)
   - "watermark, signature"

7. Consistency Across Batch
   For character sets:
   - Use same style modifier
   - Use same quality tags
   - Vary only character conditions
   - Consider using same seed with variations

8. Model-Specific Considerations

   STABLE DIFFUSION:
   - Supports negative prompts
   - Prompt weighting: (keyword:1.2) for emphasis
   - CFG Scale: 7-12 for balanced results
   - Steps: 20-50 typically sufficient

   DALL-E 3:
   - More natural language friendly
   - No negative prompts
   - Longer descriptions work well
   - Interprets context better

   MIDJOURNEY:
   - Uses --parameters for style control
   - More artistic bias by default
   - --style raw for less interpretation
   - --ar for aspect ratio

9. Condition → Visual Mapping
   Character conditions map naturally:
   - "physique: wiry" → "wiry build"
   - "wealth: poor" → "worn clothing"
   - "health: scarred" → "battle scars"
   - "facial: weathered" → "weathered face"

10. Iterative Refinement
    Start simple, then refine:
    1. Base prompt with conditions
    2. Add style modifier
    3. Add quality tags
    4. Add context if needed
    5. Use negative prompts to fix issues

╔══════════════════════════════════════════════════════════════════╗
║               READY TO GENERATE AMAZING CHARACTERS!              ║
╚══════════════════════════════════════════════════════════════════╝
    """
    )


def main() -> None:
    """Run all image prompt generation examples.

    This main function executes all examples demonstrating how to
    convert condition axis data into optimized prompts for AI image
    generation tools.
    """
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "PIPEWORKS CONDITIONAL AXIS" + " " * 27 + "║")
    print("║" + " " * 13 + "IMAGE PROMPT GENERATION EXAMPLES" + " " * 21 + "║")
    print("╚" + "═" * 68 + "╝")

    example_1_basic_image_prompt()
    example_2_styled_prompts()
    example_3_quality_enhanced_prompts()
    example_4_with_negative_prompts()
    example_5_batch_prompt_generation()
    example_6_context_specific_additions()
    example_7_prompt_engineering_tips()

    print("\n" + "=" * 70)
    print("All image prompt generation examples completed successfully!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  - Conditions convert naturally to visual descriptors")
    print("  - Style modifiers control artistic interpretation")
    print("  - Quality tags enhance output quality")
    print("  - Negative prompts help avoid unwanted features")
    print("  - Batch generation maintains visual consistency")
    print("  - Different models need different prompt strategies")
    print("\nNext Steps:")
    print("  - Try your prompts in Stable Diffusion, DALL-E, or Midjourney")
    print("  - Experiment with different style modifiers")
    print("  - Create character sheets with batch_generation.py")
    print("  - See custom_axes.py to add domain-specific traits")
    print()


if __name__ == "__main__":
    main()
