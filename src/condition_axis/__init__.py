"""Condition axis generation system for procedural character and world building.

This package implements a structured, rule-based framework for generating coherent
state descriptions across multiple semantic dimensions (axes). It is designed for
use in both visual generation (image prompts) and narrative contexts (MUD/IF games).

The condition axis system provides:
- **Weighted probability distributions** for realistic populations
- **Semantic exclusion rules** to prevent illogical combinations
- **Mandatory and optional axis policies** to control complexity
- **Reproducible generation** via random seeds
- **Extensible architecture** for adding new condition types

Available Modules:
    - character_conditions: Physical and social character states (includes facial signals)
    - occupation_axis: Occupation characteristics and societal positioning
    - _base: Shared utilities (internal)

Example usage:
    >>> from pipeworks.core.condition_axis import (
    ...     generate_condition,
    ...     generate_occupation_condition,
    ...     condition_to_prompt,
    ...     occupation_condition_to_prompt,
    ... )
    >>>
    >>> # Generate character conditions (may include facial_signal)
    >>> char = generate_condition(seed=42)
    >>> print(condition_to_prompt(char))
    'wiry, poor, weary, weathered'
    >>>
    >>> # Generate occupation conditions
    >>> occupation = generate_occupation_condition(seed=42)
    >>> print(occupation_condition_to_prompt(occupation))
    'tolerated, discreet, burdened'
    >>>
    >>> # Combine for complete character
    >>> char_prompt = condition_to_prompt(char)
    >>> occ_prompt = occupation_condition_to_prompt(occupation)
    >>> full_prompt = f"{char_prompt}, {occ_prompt}"
    >>> print(full_prompt)
    'wiry, poor, weary, weathered, tolerated, discreet, burdened'
"""

# ============================================================================
# Character Conditions (Physical & Social States)
# ============================================================================
from .character_conditions import (
    AXIS_POLICY,
    CONDITION_AXES,
    EXCLUSIONS,
    WEIGHTS,
    condition_to_prompt,
    generate_condition,
    get_available_axes,
    get_axis_values,
)

# ============================================================================
# Occupation Conditions (Occupation Characteristics)
# ============================================================================
from .occupation_axis import (
    OCCUPATION_AXES,
    OCCUPATION_EXCLUSIONS,
    OCCUPATION_POLICY,
    OCCUPATION_WEIGHTS,
    generate_occupation_condition,
    get_available_occupation_axes,
    get_occupation_axis_values,
    occupation_condition_to_prompt,
)

# ============================================================================
# Public API
# ============================================================================

__all__ = [
    # Character conditions (unified API)
    "AXIS_POLICY",
    "CONDITION_AXES",
    "EXCLUSIONS",
    # Occupation conditions
    "OCCUPATION_AXES",
    "OCCUPATION_EXCLUSIONS",
    "OCCUPATION_POLICY",
    "OCCUPATION_WEIGHTS",
    "WEIGHTS",
    "condition_to_prompt",
    "generate_condition",
    "generate_occupation_condition",
    "get_available_axes",
    "get_available_occupation_axes",
    "get_axis_values",
    "get_occupation_axis_values",
    "occupation_condition_to_prompt",
]

__version__ = "0.10.1"
