# Pipeworks Conditional Axis - Examples

**TL;DR**: Six runnable Python scripts demonstrating everything from basic generation to AI image integration. Start with `basic_usage.py`, then explore based on your needs.

```bash
python examples/basic_usage.py  # Start here
```

All examples are fully tested, include comprehensive docstrings, and follow Python best practices.

---

## Quick Start

### Running Examples

```bash
# From project root
python examples/basic_usage.py
python examples/advanced_usage.py
python examples/integration_example.py
python examples/batch_generation.py
python examples/custom_axes.py
python examples/image_prompt_generation.py
```

### What You'll Learn

This library generates coherent state descriptions using **two axis systems**:

1. **Character conditions** - Physical and social state (physique, wealth, health, demeanor, age) with optional facial signals
2. **Occupation conditions** - Labor pressures and social positioning (legitimacy, visibility, moral_load, dependency, risk_exposure)

Examples show how to generate, combine, and serialize these for visual generation (AI images) and narrative contexts (games, MUDs, interactive fiction).

---

## Learning Paths

### New Users: Start Here
1. **`basic_usage.py`** - Core concepts, seeds, serialization
2. **`integration_example.py`** - Combining character and occupation systems
3. **`image_prompt_generation.py`** - Practical AI image generation

### Advanced Users: Deep Dives
1. **`advanced_usage.py`** - Weighted distributions, exclusion rules, internals
2. **`batch_generation.py`** - Performance patterns, bulk generation
3. **`custom_axes.py`** - Extending the library for custom domains

### By Use Case

**AI Image Generation** (Stable Diffusion, DALL-E, Midjourney):
- Start: `basic_usage.py` (generation and serialization)
- Then: `image_prompt_generation.py` (prompt engineering, styles, quality tags)

**Game Development / MUDs / Interactive Fiction**:
- Start: `basic_usage.py` (generation basics)
- Then: `integration_example.py` (narrative formatting, archetypes)
- Scale: `batch_generation.py` (populations, export to JSON/CSV)

**Custom Domains** (Fantasy, Sci-Fi, Horror):
- Start: `advanced_usage.py` (understanding the pattern)
- Then: `custom_axes.py` (magic systems, tech systems)

**Bulk Content Generation**:
- Start: `batch_generation.py` (efficient generation, streaming, export)
- Filter: `integration_example.py` (archetype filtering)

---

## Example Files

### Core Examples

#### `basic_usage.py` - Foundation
**Difficulty**: Beginner
**Best For**: First-time users, getting started

Learn fundamental concepts:
- Simple generation (with and without seeds)
- Reproducible generation for testing and consistency
- Serialization to prompt strings
- Understanding axis structure
- Generating multiple distinct entities
- Unified facial signals in character generation

Start here if you're new to the library.

#### `advanced_usage.py` - Internals Deep Dive
**Difficulty**: Intermediate
**Best For**: Power users, understanding mechanics

Explore how the system works:
- Weighted probability distributions (realistic populations)
- Exclusion rules (preventing illogical combinations)
- Mandatory vs optional axes (complexity control)
- Statistical analysis of generation patterns
- Cross-system exclusion rules
- Inspecting raw data structures (AXES, WEIGHTS, EXCLUSIONS, POLICY)

Includes visualization of distributions and 500-sample statistical analysis.

#### `integration_example.py` - Complete Character Generation
**Difficulty**: Intermediate
**Best For**: Real-world usage, complete entities

Combine character and occupation systems:
- Complete entity generation (character + occupation)
- Population generation (multiple entities with unique seeds)
- Narrative vs visual formatting (same data, different outputs)
- Coherence pattern detection
- Archetype generation and filtering (The Desperate Outlaw, The Respected Merchant, etc.)

Shows how to format output for both AI image generation and narrative text.

### Advanced Examples

#### `batch_generation.py` - Scale & Performance
**Difficulty**: Advanced
**Best For**: Bulk content generation, data export

Generate entities efficiently at scale:
- Simple batch generation (moderate scale)
- Export to JSON and CSV formats
- Filtering and selection from batches
- Memory-efficient streaming (for very large batches)
- Parallel generation patterns (conceptual guide)

Essential for generating large populations or integrating with databases and APIs.

#### `custom_axes.py` - Extensibility
**Difficulty**: Advanced
**Best For**: Extending the library, custom domains

Create your own axis systems:
- Complete pattern for custom axes
- Using shared utilities from `_base.py`
- Defining AXES, POLICY, WEIGHTS, EXCLUSIONS
- Writing generation and serialization functions
- Testing exclusion rules
- Combining custom axes with core systems

Includes two complete custom systems:
- **Fantasy Magic System**: affinity, proficiency, manifestation, cost
- **Sci-Fi Technology System**: augmentation, tech_access, integration, stability

#### `image_prompt_generation.py` - AI Image Integration
**Difficulty**: Advanced
**Best For**: AI image generation tools

Generate optimized prompts for image generation:
- Converting conditions to image prompts
- Style modifiers (portrait, oil painting, 3D render, pixel art, concept art, etc.)
- Quality-enhanced prompts (photorealistic, artistic, fantasy presets)
- Positive and negative prompts (Stable Diffusion)
- Batch prompt generation for consistent character sets
- Context-specific additions (tavern, market, alley, throne room)
- Prompt engineering best practices

**Supported Tools**:
- Stable Diffusion (Web UI, ComfyUI)
- DALL-E 3
- Midjourney
- Any text-to-image model

---

## Example Features

All examples include:

- ✅ **Comprehensive type hints** - Full typing for all functions
- ✅ **Google-style docstrings** - Detailed documentation with examples
- ✅ **Working, executable code** - Every example has a `main()` function
- ✅ **Educational comments** - Explanations of concepts throughout
- ✅ **Multiple demonstrations** - Multiple examples per file
- ✅ **Full test coverage** - Comprehensive tests in `tests/test_examples.py`

---

## Testing

All examples are comprehensively tested:

```bash
# Run example tests
pytest tests/test_examples.py -v

# Run all tests
pytest -v
```

**Test Coverage**:
- Import tests (all modules load correctly)
- Function tests (utility functions work as expected)
- Reproducibility tests (seeds produce consistent results)
- Integration tests (systems combine correctly)
- Edge cases (empty inputs, zero counts, etc.)

---

## Next Steps

After exploring the examples:

1. **Review the API documentation** - Run `sphinx-build -b html docs docs/_build/html` or see `docs/` directory
2. **Try the library in your project** - Install with `pip install -e .`
3. **Explore the test suite** - See `tests/` for comprehensive test coverage
4. **Check the development guide** - See `CLAUDE.md` for project guidelines

---

## Contributing

Found a bug or want to add an example?

- **Development guide**: See `CLAUDE.md`
- **API reference**: See `docs/` directory
- **Test suite**: See `tests/` directory
- **GitHub repository**: Submit issues and pull requests

---

## License

GPL-3.0 - See LICENSE file for details.
