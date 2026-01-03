"""Tests for example scripts.

This test module verifies that all example scripts work correctly:
- Examples can be imported without errors
- Functions produce expected output types
- Seeded generation is reproducible
- Custom axis systems follow the correct pattern
- Integration examples combine systems correctly
"""

import sys
from pathlib import Path

import pytest

# Add examples directory to Python path for imports
examples_dir = Path(__file__).parent.parent / "examples"
sys.path.insert(0, str(examples_dir))


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def test_seed() -> int:
    """Provide a consistent seed for reproducibility tests.

    Returns:
        Test seed value.
    """
    return 42


# ============================================================================
# Basic Usage Tests
# ============================================================================


def test_basic_usage_imports() -> None:
    """Test that basic_usage module can be imported."""
    import basic_usage  # noqa: F401


def test_basic_usage_examples_run_without_errors() -> None:
    """Test that all basic_usage examples execute without errors."""
    from basic_usage import (
        example_1_simple_generation,
        example_2_reproducible_generation,
        example_3_serialization_to_prompts,
        example_4_understanding_axes,
        example_5_multiple_entities,
    )

    # These should not raise exceptions
    example_1_simple_generation()
    example_2_reproducible_generation()
    example_3_serialization_to_prompts()
    example_4_understanding_axes()
    example_5_multiple_entities()


# ============================================================================
# Advanced Usage Tests
# ============================================================================


def test_advanced_usage_imports() -> None:
    """Test that advanced_usage module can be imported."""
    import advanced_usage  # noqa: F401


def test_advanced_usage_examples_run_without_errors() -> None:
    """Test that all advanced_usage examples execute without errors."""
    from advanced_usage import (
        example_1_understanding_weights,
        example_2_exclusion_rules_in_action,
        example_3_mandatory_vs_optional_axes,
        example_4_analyzing_generation_patterns,
        example_5_inspecting_raw_data,
    )

    # These should not raise exceptions
    example_1_understanding_weights()
    example_2_exclusion_rules_in_action()
    example_3_mandatory_vs_optional_axes()
    example_4_analyzing_generation_patterns()
    example_5_inspecting_raw_data()


# ============================================================================
# Integration Example Tests
# ============================================================================


def test_integration_example_imports() -> None:
    """Test that integration_example module can be imported."""
    import integration_example  # noqa: F401


def test_format_as_narrative(test_seed: int) -> None:
    """Test the format_as_narrative function produces valid output.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from integration_example import format_as_narrative

    from condition_axis import (
        generate_condition,
        generate_facial_condition,
        generate_occupation_condition,
    )

    character = generate_condition(seed=test_seed)
    facial = generate_facial_condition(seed=test_seed)
    occupation = generate_occupation_condition(seed=test_seed)

    narrative = format_as_narrative(character, facial, occupation)

    # Verify output is a non-empty string
    assert isinstance(narrative, str)
    assert len(narrative) > 0
    assert narrative.endswith(".")


def test_integration_examples_run_without_errors() -> None:
    """Test that all integration_example examples execute without errors."""
    from integration_example import (
        example_1_complete_entity_generation,
        example_2_multiple_complete_entities,
        example_3_narrative_vs_visual_formatting,
        example_4_identifying_coherence_patterns,
        example_5_entity_archetype_generation,
    )

    # These should not raise exceptions
    example_1_complete_entity_generation()
    example_2_multiple_complete_entities()
    example_3_narrative_vs_visual_formatting()
    example_4_identifying_coherence_patterns()
    example_5_entity_archetype_generation()


# ============================================================================
# Batch Generation Tests
# ============================================================================


def test_batch_generation_imports() -> None:
    """Test that batch_generation module can be imported."""
    import batch_generation  # noqa: F401


def test_generate_entity_function(test_seed: int) -> None:
    """Test the generate_entity function.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from batch_generation import generate_entity

    entity = generate_entity(test_seed)

    # Verify structure
    assert isinstance(entity, dict)
    assert "seed" in entity
    assert "character" in entity
    assert "facial" in entity
    assert "occupation" in entity
    assert entity["seed"] == test_seed


def test_generate_batch_function(test_seed: int) -> None:
    """Test the generate_batch function.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from batch_generation import generate_batch

    count = 10
    batch = generate_batch(start_seed=test_seed, count=count)

    # Verify batch structure
    assert isinstance(batch, list)
    assert len(batch) == count

    # Verify first entity has correct seed
    assert batch[0]["seed"] == test_seed

    # Verify last entity has correct seed
    assert batch[-1]["seed"] == test_seed + count - 1


def test_generate_streaming_function(test_seed: int) -> None:
    """Test the generate_streaming generator function.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from batch_generation import generate_streaming

    count = 5
    entities = list(generate_streaming(start_seed=test_seed, count=count))

    # Verify correct number generated
    assert len(entities) == count

    # Verify seeds are sequential
    for i, entity in enumerate(entities):
        assert entity["seed"] == test_seed + i


def test_batch_generation_examples_run_without_errors() -> None:
    """Test that all batch_generation examples execute without errors."""
    from batch_generation import (
        example_1_simple_batch_generation,
        example_2_export_to_json,
        example_3_export_to_csv,
        example_4_filtering_and_selection,
        example_5_memory_efficient_streaming,
        example_6_parallel_generation_pattern,
    )

    # These should not raise exceptions
    example_1_simple_batch_generation()
    example_2_export_to_json()
    example_3_export_to_csv()
    example_4_filtering_and_selection()
    example_5_memory_efficient_streaming()
    example_6_parallel_generation_pattern()


# ============================================================================
# Custom Axes Tests
# ============================================================================


def test_custom_axes_imports() -> None:
    """Test that custom_axes module can be imported."""
    import custom_axes  # noqa: F401


def test_magic_system_generation(test_seed: int) -> None:
    """Test the custom magic system generator.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from custom_axes import generate_magic_condition, magic_condition_to_prompt

    # Generate with seed
    magic = generate_magic_condition(seed=test_seed)

    # Verify structure
    assert isinstance(magic, dict)
    assert "affinity" in magic  # Mandatory axis
    assert "proficiency" in magic  # Mandatory axis

    # Verify reproducibility
    magic2 = generate_magic_condition(seed=test_seed)
    assert magic == magic2

    # Test serialization
    prompt = magic_condition_to_prompt(magic)
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_tech_system_generation(test_seed: int) -> None:
    """Test the custom tech system generator.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from custom_axes import generate_tech_condition, tech_condition_to_prompt

    # Generate with seed
    tech = generate_tech_condition(seed=test_seed)

    # Verify structure
    assert isinstance(tech, dict)
    assert "augmentation" in tech  # Mandatory axis
    assert "tech_access" in tech  # Mandatory axis

    # Verify reproducibility
    tech2 = generate_tech_condition(seed=test_seed)
    assert tech == tech2

    # Test serialization
    prompt = tech_condition_to_prompt(tech)
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_custom_axes_examples_run_without_errors() -> None:
    """Test that all custom_axes examples execute without errors."""
    from custom_axes import (
        example_1_using_custom_magic_system,
        example_2_using_custom_tech_system,
        example_3_combining_with_core_systems,
        example_4_testing_exclusion_rules,
        example_5_custom_axis_pattern_summary,
    )

    # These should not raise exceptions
    example_1_using_custom_magic_system()
    example_2_using_custom_tech_system()
    example_3_combining_with_core_systems()
    example_4_testing_exclusion_rules()
    example_5_custom_axis_pattern_summary()


# ============================================================================
# Image Prompt Generation Tests
# ============================================================================


def test_image_prompt_generation_imports() -> None:
    """Test that image_prompt_generation module can be imported."""
    import image_prompt_generation  # noqa: F401


def test_build_full_prompt_function(test_seed: int) -> None:
    """Test the build_full_prompt function.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from image_prompt_generation import build_full_prompt

    from condition_axis import (
        generate_condition,
        generate_facial_condition,
        generate_occupation_condition,
    )

    character = generate_condition(seed=test_seed)
    facial = generate_facial_condition(seed=test_seed)
    occupation = generate_occupation_condition(seed=test_seed)

    # Test basic prompt
    basic_prompt = build_full_prompt(character, facial, occupation)
    assert isinstance(basic_prompt, str)
    assert len(basic_prompt) > 0

    # Test with style
    styled_prompt = build_full_prompt(
        character, facial, occupation, style="portrait photograph"
    )
    assert "portrait photograph" in styled_prompt

    # Test with quality tags
    quality_prompt = build_full_prompt(
        character,
        facial,
        occupation,
        quality_tags=["highly detailed", "8k resolution"],
    )
    assert "highly detailed" in quality_prompt
    assert "8k resolution" in quality_prompt

    # Test with additional details
    detailed_prompt = build_full_prompt(
        character,
        facial,
        occupation,
        additional_details="standing in a medieval tavern",
    )
    assert "standing in a medieval tavern" in detailed_prompt


def test_build_negative_prompt_function() -> None:
    """Test the build_negative_prompt function."""
    from image_prompt_generation import build_negative_prompt

    # Test basic negative prompt
    basic_negative = build_negative_prompt()
    assert isinstance(basic_negative, str)
    assert "low quality" in basic_negative
    assert "blurry" in basic_negative

    # Test with custom avoid traits
    custom_negative = build_negative_prompt(avoid_traits=["cartoon", "anime"])
    assert "cartoon" in custom_negative
    assert "anime" in custom_negative


def test_image_prompt_generation_examples_run_without_errors() -> None:
    """Test that all image_prompt_generation examples execute without errors."""
    from image_prompt_generation import (
        example_1_basic_image_prompt,
        example_2_styled_prompts,
        example_3_quality_enhanced_prompts,
        example_4_with_negative_prompts,
        example_5_batch_prompt_generation,
        example_6_context_specific_additions,
        example_7_prompt_engineering_tips,
    )

    # These should not raise exceptions
    example_1_basic_image_prompt()
    example_2_styled_prompts()
    example_3_quality_enhanced_prompts()
    example_4_with_negative_prompts()
    example_5_batch_prompt_generation()
    example_6_context_specific_additions()
    example_7_prompt_engineering_tips()


# ============================================================================
# Reproducibility Tests
# ============================================================================


@pytest.mark.parametrize("seed", [0, 42, 100, 999])
def test_custom_magic_reproducibility(seed: int) -> None:
    """Test that magic generation is reproducible with seeds.

    Args:
        seed: Random seed value for generation.
    """
    from custom_axes import generate_magic_condition

    magic1 = generate_magic_condition(seed=seed)
    magic2 = generate_magic_condition(seed=seed)

    assert magic1 == magic2, f"Magic generation not reproducible with seed {seed}"


@pytest.mark.parametrize("seed", [0, 42, 100, 999])
def test_custom_tech_reproducibility(seed: int) -> None:
    """Test that tech generation is reproducible with seeds.

    Args:
        seed: Random seed value for generation.
    """
    from custom_axes import generate_tech_condition

    tech1 = generate_tech_condition(seed=seed)
    tech2 = generate_tech_condition(seed=seed)

    assert tech1 == tech2, f"Tech generation not reproducible with seed {seed}"


@pytest.mark.parametrize("seed", [0, 42, 100, 999])
def test_batch_generation_reproducibility(seed: int) -> None:
    """Test that batch generation is reproducible with seeds.

    Args:
        seed: Random seed value for generation.
    """
    from batch_generation import generate_entity

    entity1 = generate_entity(seed)
    entity2 = generate_entity(seed)

    assert entity1 == entity2, f"Entity generation not reproducible with seed {seed}"


# ============================================================================
# Integration Tests
# ============================================================================


def test_all_examples_have_main_functions() -> None:
    """Test that all example modules have main() functions."""
    import advanced_usage
    import basic_usage
    import batch_generation
    import custom_axes
    import image_prompt_generation
    import integration_example

    modules = [
        basic_usage,
        advanced_usage,
        integration_example,
        batch_generation,
        custom_axes,
        image_prompt_generation,
    ]

    for module in modules:
        assert hasattr(module, "main"), f"{module.__name__} missing main() function"
        assert callable(module.main), f"{module.__name__}.main is not callable"


def test_custom_axes_follow_pattern() -> None:
    """Test that custom axis systems follow the required pattern."""
    import custom_axes

    # Magic system
    assert hasattr(custom_axes, "MAGIC_AXES")
    assert hasattr(custom_axes, "MAGIC_POLICY")
    assert hasattr(custom_axes, "MAGIC_WEIGHTS")
    assert hasattr(custom_axes, "MAGIC_EXCLUSIONS")
    assert hasattr(custom_axes, "generate_magic_condition")
    assert hasattr(custom_axes, "magic_condition_to_prompt")

    # Tech system
    assert hasattr(custom_axes, "TECH_AXES")
    assert hasattr(custom_axes, "TECH_POLICY")
    assert hasattr(custom_axes, "TECH_WEIGHTS")
    assert hasattr(custom_axes, "TECH_EXCLUSIONS")
    assert hasattr(custom_axes, "generate_tech_condition")
    assert hasattr(custom_axes, "tech_condition_to_prompt")


def test_custom_axes_use_base_utilities() -> None:
    """Test that custom axes properly use utilities from _base.py."""
    from custom_axes import generate_magic_condition, generate_tech_condition

    # Generate conditions (should not raise if utilities are used correctly)
    magic = generate_magic_condition(seed=42)
    tech = generate_tech_condition(seed=42)

    # Verify they return dict (standard format)
    assert isinstance(magic, dict)
    assert isinstance(tech, dict)


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


def test_batch_generation_with_zero_count() -> None:
    """Test batch generation with zero count."""
    from batch_generation import generate_batch

    batch = generate_batch(start_seed=0, count=0)
    assert isinstance(batch, list)
    assert len(batch) == 0


def test_streaming_generation_with_zero_count() -> None:
    """Test streaming generation with zero count."""
    from batch_generation import generate_streaming

    entities = list(generate_streaming(start_seed=0, count=0))
    assert len(entities) == 0


def test_build_full_prompt_with_empty_components(test_seed: int) -> None:
    """Test build_full_prompt with minimal inputs.

    Args:
        test_seed: Pytest fixture providing test seed.
    """
    from image_prompt_generation import build_full_prompt

    from condition_axis import (
        generate_condition,
        generate_facial_condition,
        generate_occupation_condition,
    )

    character = generate_condition(seed=test_seed)
    facial = generate_facial_condition(seed=test_seed)
    occupation = generate_occupation_condition(seed=test_seed)

    # Should work with no optional parameters
    prompt = build_full_prompt(character, facial, occupation)
    assert isinstance(prompt, str)
    assert len(prompt) > 0


def test_build_negative_prompt_with_none() -> None:
    """Test build_negative_prompt with None avoid_traits."""
    from image_prompt_generation import build_negative_prompt

    negative = build_negative_prompt(avoid_traits=None)
    assert isinstance(negative, str)
    assert len(negative) > 0
