# pipeworks-conditional-axis

> The intent is not to define what is true about a character, system, or situation, but to bias how outcomes are interpreted and resolved.

`pipeworks-conditional-axis` is a structured, rule-based Python framework for generating coherent state descriptions across multiple semantic dimensions (axes). It is designed for procedural content generation in both visual (AI image prompts) and narrative (game development, MUDs, interactive fiction) contexts.

This package moves beyond simple state flags or debuffs, treating conditions as **axes that modulate resolution**. Instead of defining what *is true*, it provides a system to bias how outcomes are interpreted, what they cost, and what traces they leave behind.

## Core Philosophy

The system is built on a few key principles:

*   **Conditions as Axes, Not Labels**: A condition exists on an axis (e.g., `Stable ↔ Precarious`), not as a binary on/off switch. The system asks, *“Where along this axis does interpretation tilt?”* rather than *“Do you have the condition?”*
*   **Modulation Over Definition**: Conditions influence the *margins* of success or failure, bias the tone and consequences of actions, and color narrative interpretation. They do not prescribe specific outcomes or forbid attempts, preserving agency and emergence.
*   **Observed, Not Owned**: Conditions are not something a character *has*; they are something the system *observes* about a situation, its context, and its accumulated history. This avoids medicalization or moral judgment, aligning instead with a ledger-based approach where actions leave traces.

## Key Features

*   **Weighted Probability Distributions**: Generate realistic populations and scenarios using weighted probabilities (e.g., "poor" is more common than "wealthy").
*   **Semantic Exclusion Rules**: Prevent illogical combinations with a robust, declarative rule system (e.g., a character with the "decadent" wealth condition cannot also be "frail").
*   **Mandatory & Optional Policies**: Control the complexity and narrative detail of generated conditions by defining which axes are mandatory and which are optional.
*   **Reproducible Generation**: Use random seeds to generate the exact same conditions every time, ensuring deterministic and testable output.
*   **Extensible Architecture**: Easily add new condition types and axes to suit any domain.
*   **Zero Dependencies**: Pure Python with no external runtime dependencies.

## Core Systems

The package includes three primary condition generation systems:

### 1. Character Conditions

Generates physical and social character states. This system establishes a character’s baseline physical and social presence.

| Axis | Description | Example Values |
|---|---|---|
| **Physique** | Body structure and build | `skinny`, `wiry`, `stocky`, `hunched`, `frail`, `broad` |
| **Wealth** | Economic and social status | `poor`, `modest`, `well-kept`, `wealthy`, `decadent` |
| **Health** | Physical health and condition | `sickly`, `scarred`, `weary`, `hale`, `limping` |
| **Demeanor** | Behavioral presentation | `timid`, `suspicious`, `resentful`, `alert`, `proud` |
| **Age** | Life stage | `young`, `middle-aged`, `old`, `ancient` |

### 2. Occupation Conditions

Generates the contextual characteristics and social positioning of an occupation. Instead of defining *what* a job is, this system describes *what living with it feels like*.

| Axis | Description | Example Values |
|---|---|---|
| **Legitimacy** | How society views the occupation | `sanctioned`, `tolerated`, `questioned`, `illicit` |
| **Visibility** | How conspicuous the work is | `hidden`, `discreet`, `routine`, `conspicuous` |
| **Moral Load** | The ethical weight on practitioners | `neutral`, `burdened`, `conflicted`, `corrosive` |
| **Dependency** | How essential the work is to society | `optional`, `useful`, `necessary`, `unavoidable` |
| **Risk Exposure** | The physical and psychological toll | `benign`, `straining`, `hazardous`, `eroding` |

### 3. Facial Conditions

Generates facial signal descriptors that modulate how a character’s face is perceived. These are interpretive signals, not anatomical specifications.

| Axis | Description | Example Values |
|---|---|---|
| **Facial Signal** | Perceptual modifier for facial features | `understated`, `pronounced`, `exaggerated`, `asymmetrical`, `weathered`, `soft-featured`, `sharp-featured` |

## Installation

The package has zero runtime dependencies and can be installed directly from PyPI:

```bash
pip install pipeworks-conditional-axis
```

For development, clone the repository and install with the `[dev]` extras:

```bash
git clone https://github.com/aa-parky/pipeworks_conditional_axis.git
cd pipeworks_conditional_axis
pip install -e ".[dev]"
```

## Usage

Each system provides a `generate_<type>_condition()` function and a `<type>_condition_to_prompt()` serializer.

```python
from condition_axis import (
    generate_condition,
    generate_facial_condition,
    generate_occupation_condition,
    condition_to_prompt,
    facial_condition_to_prompt,
    occupation_condition_to_prompt,
)

# 1. Generate conditions for each system using a seed for reproducibility
char_condition = generate_condition(seed=42)
face_condition = generate_facial_condition(seed=42)
occ_condition = generate_occupation_condition(seed=42)

# 2. Convert the structured data to prompt-friendly strings
char_prompt = condition_to_prompt(char_condition)
face_prompt = facial_condition_to_prompt(face_condition)
occ_prompt = occupation_condition_to_prompt(occ_condition)

# 3. Combine the prompts for a full description
full_prompt = f"{char_prompt}, {face_prompt}, whose work is {occ_prompt}"

print(f"Character Condition: {char_prompt}")
# >>> Character Condition: hunched, poor, scarred

print(f"Facial Condition: {face_prompt}")
# >>> Facial Condition: weathered

print(f"Occupation Condition: {occ_prompt}")
# >>> Occupation Condition: tolerated, hidden, neutral

print(f"\nCombined: {full_prompt}")
# >>> Combined: hunched, poor, scarred, weathered, whose work is tolerated, hidden, neutral
```

### Example: Occupation Archetypes

The power of the system comes from combining axes to create rich archetypes. The occupation axes can describe a "Corpse Collector" and an "Unofficial Problem Resolver" with the same five dimensions, just different pressures.

**Corpse Collector**
```python
{
  "legitimacy": "tolerated",
  "visibility": "routine",
  "moral_load": "burdened",
  "dependency": "necessary",
  "risk_exposure": "eroding",
}
```
*Narrative Handles: "Licensed for after-hours recovery," "Doesn’t eat near work."*

**Unofficial Problem Resolver**
```python
{
  "legitimacy": "questioned",
  "visibility": "discreet",
  "moral_load": "conflicted",
  "dependency": "unavoidable",
  "risk_exposure": "hazardous",
}
```
*Narrative Handles: "Works without appointment," "Paid after results," "Never advertised."*

## Contributing

Contributions are welcome! This project uses a standard development workflow with `pytest` for testing, `black` for formatting, `ruff` for linting, and `mypy` for type checking. Please see `pyproject.toml` for full development dependencies and tool configurations.

## License

This project is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for details.
