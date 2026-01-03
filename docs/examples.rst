Usage Examples
==============

The ``examples/`` directory contains comprehensive, runnable examples demonstrating all library features.
Each example is fully tested and includes detailed docstrings explaining the concepts.

Running Examples
----------------

All examples can be run directly from the command line:

.. code-block:: bash

   python examples/basic_usage.py
   python examples/advanced_usage.py
   python examples/integration_example.py
   python examples/batch_generation.py
   python examples/custom_axes.py
   python examples/image_prompt_generation.py

Each example includes:

- Comprehensive type hints and Google-style docstrings
- Working, executable code with ``main()`` functions
- Educational comments explaining concepts
- Multiple demonstrations per file (5-7 examples each)

Core Examples
-------------

Basic Usage
~~~~~~~~~~~

Simple generation, serialization, and reproducibility.

**File**: ``examples/basic_usage.py``

.. literalinclude:: ../examples/basic_usage.py
   :language: python
   :lines: 1-76
   :caption: Basic Usage Example

**Key Concepts**:

- Random generation without seeds
- Reproducible generation with seeds
- Serialization to prompt strings
- Understanding axis structure
- Generating multiple distinct entities

Advanced Usage
~~~~~~~~~~~~~~

Weighted distributions, exclusion rules, and statistical analysis.

**File**: ``examples/advanced_usage.py``

This example demonstrates:

- Understanding weighted probability distributions
- How exclusion rules prevent illogical combinations
- Mandatory vs optional axes
- Analyzing generation patterns with statistics
- Inspecting raw data structures (CONDITION_AXES, WEIGHTS, EXCLUSIONS, AXIS_POLICY)

.. literalinclude:: ../examples/advanced_usage.py
   :language: python
   :lines: 33-68
   :caption: Understanding Weighted Distributions

Integration Example
~~~~~~~~~~~~~~~~~~~

Combining character and occupation axis systems for complete entity generation.

**File**: ``examples/integration_example.py``

.. literalinclude:: ../examples/integration_example.py
   :language: python
   :lines: 24-76
   :caption: Complete Entity Generation

**Key Concepts**:

- Combining character conditions (including facial signals) and occupation systems
- Multiple complete entities
- Narrative vs visual formatting
- Identifying coherence patterns
- Entity archetype generation

**Note**: As of v1.1.0, facial signals are integrated into character conditions as an optional axis.

Advanced Examples
-----------------

Batch Generation
~~~~~~~~~~~~~~~~

Bulk generation with JSON/CSV export and memory-efficient streaming.

**File**: ``examples/batch_generation.py``

.. literalinclude:: ../examples/batch_generation.py
   :language: python
   :lines: 43-77
   :caption: Batch Generation Functions

**Features**:

- Simple batch generation (up to 10k entities)
- Export to JSON format
- Export to CSV format
- Filtering and selection from batches
- Memory-efficient streaming for large batches (100k+)
- Parallel generation patterns

Custom Axes
~~~~~~~~~~~

Creating custom axis systems for different domains.

**File**: ``examples/custom_axes.py``

This example includes two complete custom systems:

1. **Fantasy Magic System**: affinity, proficiency, manifestation, cost
2. **Sci-Fi Technology System**: augmentation, tech_access, integration, stability

.. literalinclude:: ../examples/custom_axes.py
   :language: python
   :lines: 19-113
   :caption: Fantasy Magic Axis System

**Pattern for Creating Custom Axes**:

1. Define ``AXES`` dictionary (axis names → possible values)
2. Define ``POLICY`` dictionary (mandatory/optional axes)
3. Define ``WEIGHTS`` dictionary (optional, for realistic distributions)
4. Define ``EXCLUSIONS`` dictionary (optional, for semantic coherence)
5. Write ``generate_<name>_condition()`` function
6. Write ``<name>_condition_to_prompt()`` function
7. Use shared utilities from ``_base.py``

Image Prompt Generation
~~~~~~~~~~~~~~~~~~~~~~~

Integration with AI image generation tools (Stable Diffusion, DALL-E, Midjourney).

**File**: ``examples/image_prompt_generation.py``

.. literalinclude:: ../examples/image_prompt_generation.py
   :language: python
   :lines: 23-81
   :caption: Building Full Image Prompts

**Features**:

- Basic image prompt generation
- Styled prompts (portrait, oil painting, 3D render, etc.)
- Quality-enhanced prompts (photorealistic, artistic, fantasy)
- Positive and negative prompts (Stable Diffusion)
- Batch prompt generation for character sets
- Context-specific additions (tavern, market, alley, throne room)
- Comprehensive prompt engineering best practices

Example Tests
-------------

All examples are comprehensively tested in ``tests/test_examples.py``:

- 39 tests covering all example functionality
- Import tests for all modules
- Function-specific tests (generation, serialization, utilities)
- Reproducibility tests with parametrization
- Integration tests verifying patterns
- Edge case and error handling tests

All tests pass with 100% success rate.

Next Steps
----------

After exploring the examples:

1. Review the :doc:`API Reference <api/_base>` for detailed function documentation
2. Read the :doc:`Design Philosophy <design/00_goblin_laws>` to understand the architectural principles
3. Check the :doc:`Conceptual System Design <design/specifications/condition_axis>` for implementation details
4. See ``examples/custom_axes.py`` for guidance on extending the library

For more information, see:

- :doc:`README <README>` - Project overview and installation
- :doc:`API Reference <api/_base>` - Complete API documentation
- GitHub Repository: https://github.com/aa-parky/pipeworks_entity_state_generation
