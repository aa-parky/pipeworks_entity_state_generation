Pipeworks Conditional Axis Documentation
=========================================

.. image:: https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/test.yml/badge.svg
   :target: https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/test.yml
   :alt: Tests

.. image:: https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/lint.yml/badge.svg
   :target: https://github.com/aa-parky/pipeworks_entity_state_generation/actions/workflows/lint.yml
   :alt: Lint & Type Check

.. image:: https://codecov.io/gh/aa-parky/pipeworks_entity_state_generation/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/aa-parky/pipeworks_entity_state_generation
   :alt: codecov

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: License: GPL v3

A structured, rule-based Python framework for generating coherent character and entity state descriptions across multiple semantic dimensions. Designed for procedural content generation in both visual contexts (AI image prompts) and narrative systems (game development, MUDs, interactive fiction).

**Core Philosophy**: Conditions exist on axes (e.g., ``Stable ↔ Precarious``) rather than binary flags. The system asks *"Where along this axis does interpretation tilt?"* rather than *"Do you have the condition?"* This modulates resolution margins, biases outcomes, and colors narrative interpretation without prescribing specific outcomes.

Installation
------------

.. code-block:: bash

   # Install from PyPI (when published)
   pip install pipeworks-conditional-axis

   # Install from source for development
   git clone https://github.com/aa-parky/pipeworks_entity_state_generation.git
   cd pipeworks_entity_state_generation
   pip install -e ".[dev]"

**Requirements**: Python 3.12+

Quick Start
-----------

.. code-block:: python

   from condition_axis import (
       generate_condition,
       generate_facial_condition,
       generate_occupation_condition,
       condition_to_prompt,
       facial_condition_to_prompt,
       occupation_condition_to_prompt,
   )

   # Generate character physical and social state
   character_state = generate_condition(seed=42)
   print(character_state)
   # {'physique': 'wiry', 'wealth': 'poor', 'health': 'weary'}

   # Generate facial perception modifiers
   facial_state = generate_facial_condition(seed=42)
   print(facial_state)
   # {'overall_impression': 'weathered'}

   # Generate occupation characteristics
   occupation_state = generate_occupation_condition(seed=42)
   print(occupation_state)
   # {'legitimacy': 'tolerated', 'visibility': 'discreet', 'moral_load': 'burdened'}

   # Convert to comma-separated prompts
   char_prompt = condition_to_prompt(character_state)
   face_prompt = facial_condition_to_prompt(facial_state)
   occ_prompt = occupation_condition_to_prompt(occupation_state)

   full_prompt = f"{char_prompt}, {face_prompt}, {occ_prompt}"
   print(full_prompt)
   # "wiry, poor, weary, weathered, tolerated, discreet, burdened"

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   README

.. toctree::
   :maxdepth: 2
   :caption: Usage Examples

   examples

.. toctree::
   :maxdepth: 2
   :caption: Architecture Diagrams

   diagrams/README

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/_base
   api/character_conditions
   api/facial_conditions
   api/occupation_axis

.. toctree::
   :maxdepth: 2
   :caption: Design & Philosophy

   design/00_goblin_laws
   design/01_character_state_model
   design/02_pipeworks_system_architecture
   design/03_pipeworks_components
   design/04_characters_first_narrow_door

.. toctree::
   :maxdepth: 2
   :caption: Technical Specifications

   specifications/condition_axis
   specifications/occupation_axis
   specifications/Obey_the_Verb

.. toctree::
   :maxdepth: 2
   :caption: Setup & Development

   guides/Pre-Commit Hooks Setup Guide
   guides/GitHub Actions CI Setup Guide
   guides/ReadTheDocs Setup Guide

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources

   Project Documentation Index <README>


Key Features
------------

- **Weighted Probability Distributions**: Axes use realistic population weights rather than uniform randomness
- **Semantic Exclusion Rules**: The system prevents illogical combinations through exclusion rules
- **Mandatory and Optional Axes**: Prevents prompt dilution while maintaining narrative clarity
- **Reproducible Generation**: All generation functions accept an optional seed parameter for deterministic output
- **Zero Runtime Dependencies**: Pure Python implementation with no external requirements
- **Comprehensive Testing**: 90%+ test coverage with full CI/CD pipeline

What Are Conditional Axes?
---------------------------

Conditional axes describe the **current lived state** of an entity. They are:

- **Mutually exclusive within an axis**: A character can't be both "wealthy" and "poor"
- **Population-weighted**: Poor characters are more common than wealthy ones
- **Explainable and auditable**: Every value comes from a traceable rule
- **Resolved once during generation**: Deterministic given the same seed

Available Axis Systems
----------------------

The library currently provides three independent axis systems:

**1. Character Conditions** (``character_conditions``)
   Physical and social states that establish baseline character presentation:

   - **Physique**: skinny, wiry, stocky, hunched, frail, broad
   - **Wealth**: poor, modest, well-kept, wealthy, decadent
   - **Health**: sickly, scarred, weary, hale, limping
   - **Demeanor**: timid, suspicious, resentful, alert, proud
   - **Age**: young, middle-aged, old, ancient

**2. Facial Conditions** (``facial_conditions``)
   Perception modifiers that bias how faces are interpreted:

   - **Overall Impression**: youthful, weathered, stern, gentle, marked, unremarkable

**3. Occupation Conditions** (``occupation_axis``)
   Labor pressures and social positioning (not job titles):

   - **Legitimacy**: sanctioned, tolerated, questioned, illicit
   - **Visibility**: hidden, discreet, routine, conspicuous
   - **Moral Load**: neutral, burdened, conflicted, corrosive
   - **Dependency**: optional, useful, necessary, unavoidable
   - **Risk Exposure**: benign, straining, hazardous, eroding

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
