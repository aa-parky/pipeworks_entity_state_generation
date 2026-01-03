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

NOTE: As of v1.1.0, facial conditions are integrated into character_conditions.
The separate facial_conditions module is deprecated but maintained for backward compatibility.

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

For backward compatibility, the old API is still available:
    >>> # Deprecated approach (still works)
    >>> from pipeworks.core.condition_axis import generate_facial_condition
    >>> facial = generate_facial_condition(seed=42)
"""

import warnings

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
# Backward Compatibility: Deprecated Facial Conditions API
# ============================================================================
# NOTE: As of v1.1.0, facial conditions are integrated into character_conditions.
# These wrapper functions maintain backward compatibility and will be removed in v2.0.0.


def generate_facial_condition(seed: int | None = None) -> dict[str, str]:
    """Generate facial condition (DEPRECATED).

    DEPRECATED: This function is deprecated as of v1.1.0.
    Facial signals are now integrated into generate_condition() as an optional axis.

    This wrapper is maintained for backward compatibility and will be removed
    in v2.0.0.

    Args:
        seed: Optional random seed for reproducible generation.

    Returns:
        Dictionary with 'facial_signal' key (for backward compatibility).

    Examples:
        >>> # Old approach (deprecated)
        >>> facial = generate_facial_condition(seed=42)
        >>> # {'facial_signal': 'weathered'}

        >>> # New approach (recommended)
        >>> char = generate_condition(seed=42)
        >>> # May include 'facial_signal' alongside other axes

    See Also:
        generate_condition() - Unified character generation (recommended)
    """
    warnings.warn(
        "generate_facial_condition() is deprecated as of v1.1.0. "
        "Facial signals are now integrated into generate_condition(). "
        "This function will be removed in v2.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Generate a facial_signal using the character_conditions system
    import random

    if seed is not None:
        random.seed(seed)

    from ._base import weighted_choice

    # Select only facial_signal to maintain backward compatibility
    facial_signal = weighted_choice(
        CONDITION_AXES["facial_signal"], WEIGHTS.get("facial_signal")
    )

    return {"facial_signal": facial_signal}


def facial_condition_to_prompt(condition_dict: dict[str, str]) -> str:
    """Convert facial condition to prompt (DEPRECATED).

    DEPRECATED: This function is deprecated as of v1.1.0.
    Use condition_to_prompt() instead, which handles all axes including facial_signal.

    Args:
        condition_dict: Dictionary with facial_signal key.

    Returns:
        Prompt string.

    See Also:
        condition_to_prompt() - Unified serialization (recommended)
    """
    warnings.warn(
        "facial_condition_to_prompt() is deprecated as of v1.1.0. "
        "Use condition_to_prompt() instead. "
        "This function will be removed in v2.0.0.",
        DeprecationWarning,
        stacklevel=2,
    )

    from ._base import values_to_prompt

    return values_to_prompt(condition_dict)


def get_available_facial_axes() -> list[str]:
    """Get facial axes (DEPRECATED).

    DEPRECATED: Use get_available_axes() instead.
    """
    warnings.warn(
        "get_available_facial_axes() is deprecated. "
        "Use get_available_axes() instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return ["facial_signal"]


def get_facial_axis_values(axis: str) -> list[str]:
    """Get facial axis values (DEPRECATED).

    DEPRECATED: Use get_axis_values() instead.
    """
    warnings.warn(
        "get_facial_axis_values() is deprecated. "
        "Use get_axis_values('facial_signal') instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return CONDITION_AXES[axis]


# Deprecated data structures (for backward compatibility)
FACIAL_AXES = {"facial_signal": CONDITION_AXES["facial_signal"]}
FACIAL_POLICY = {"mandatory": ["facial_signal"], "optional": [], "max_optional": 0}
FACIAL_WEIGHTS = {"facial_signal": WEIGHTS.get("facial_signal", {})}
FACIAL_EXCLUSIONS: dict = {}  # Empty - exclusions now in EXCLUSIONS

# ============================================================================
# Public API
# ============================================================================

__all__ = [
    # Character conditions (unified API)
    "AXIS_POLICY",
    "CONDITION_AXES",
    "EXCLUSIONS",
    # Deprecated: Facial conditions (backward compatibility only)
    # These will be removed in v2.0.0
    "FACIAL_AXES",  # DEPRECATED
    "FACIAL_EXCLUSIONS",  # DEPRECATED
    "FACIAL_POLICY",  # DEPRECATED
    "FACIAL_WEIGHTS",  # DEPRECATED
    # Occupation conditions
    "OCCUPATION_AXES",
    "OCCUPATION_EXCLUSIONS",
    "OCCUPATION_POLICY",
    "OCCUPATION_WEIGHTS",
    "WEIGHTS",
    "condition_to_prompt",
    "facial_condition_to_prompt",  # DEPRECATED
    "generate_condition",
    "generate_facial_condition",  # DEPRECATED
    "generate_occupation_condition",
    "get_available_axes",
    "get_available_facial_axes",  # DEPRECATED
    "get_available_occupation_axes",
    "get_axis_values",
    "get_facial_axis_values",  # DEPRECATED
    "get_occupation_axis_values",
    "occupation_condition_to_prompt",
]

__version__ = "1.0.0"
