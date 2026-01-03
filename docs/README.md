# Pipeworks Entity State Generation Documentation

This directory contains design documents, technical specifications, and setup guides for the `pipeworks_entity_state_generation` project.

## Quick Navigation

### New to the Project?
Start here:
1. [Character State Model](design/01_character_state_model.md) - Understand the core conceptual model
2. [Pipeworks System Architecture](design/02_pipeworks_system_architecture.md) - See how components fit together **(includes architecture diagrams)**
3. [Character Conditions Spec](design/specifications/condition_axis.md) - Learn the actual implementation

**Visual learner?** Jump straight to the [architecture diagrams](diagrams/) to see the system structure.

### Setting Up Development?
1. [Pre-Commit Hooks Setup Guide](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) - Local development setup
2. [GitHub Actions CI Setup Guide](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) - CI/CD configuration

### Working on Character Generation?
- [Character Conditions System](design/specifications/condition_axis.md) - Physical & social character states
- [Occupation Axis System](design/specifications/occupation_axis.md) - Occupation characteristics
- [Obey the Verb](design/specifications/Obey_the_Verb.md) - AI image generation prompting strategy

---

## Directory Structure

### `design/` - Philosophy & Architecture

Conceptual foundations and architectural decisions. These documents explain *why* things are designed the way they are.

| Document | Purpose |
|----------|---------|
| [00_goblin_laws.md](design/00_goblin_laws.md) | Project philosophy expressed as whimsical "laws" |
| [01_character_state_model.md](design/01_character_state_model.md) | How Pipeworks understands character state |
| [02_pipeworks_system_architecture.md](design/02_pipeworks_system_architecture.md) | High-level system design across all Pipeworks repos |
| [03_pipeworks_components.md](design/03_pipeworks_components.md) | The five load-bearing components of Pipeworks |
| [04_characters_first_narrow_door.md](design/04_characters_first_narrow_door.md) | Why characters came first (design rationale) |

**Read these when:**
- You're new to the project and want to understand the philosophy
- You're making architectural decisions
- You're wondering "why did they do it this way?"

### `design/specifications/` - Conceptual System Design

Implementation details for the generation systems. These documents describe *what* the system does and *how* it works.

| Document | Purpose |
|----------|---------|
| [condition_axis.md](design/specifications/condition_axis.md) | Character condition system (physique, wealth, health, demeanor, age) |
| [occupation_axis.md](design/specifications/occupation_axis.md) | Occupation axis system (legitimacy, visibility, moral load, etc.) |
| [Obey_the_Verb.md](design/specifications/Obey_the_Verb.md) | Image model prompting strategy (verbs > nouns) |

**Read these when:**
- You're implementing character generation features
- You're adding new axes or conditions
- You're integrating with image generation systems

### `guides/` - Setup & Process Guides

Step-by-step instructions for setting up development tools, CI/CD, and migration guides.

| Document | Purpose |
|----------|---------|
| [Pre-Commit Hooks Setup Guide.md](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) | Local git hooks for code quality |
| [GitHub Actions CI Setup Guide.md](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) | Automated testing and linting |
| [ReadTheDocs Setup Guide.md](guides/ReadTheDocs%20Setup%20Guide.md) | Deploying documentation to ReadTheDocs |
| [Migration-v1.0-to-v1.1.md](guides/Migration-v1.0-to-v1.1.md) | Upgrading from v1.0 to v1.1 unified API |

**Read these when:**
- You're setting up your development environment
- You're troubleshooting CI failures
- You're configuring new hooks or workflows
- You're deploying documentation to ReadTheDocs
- You're upgrading from v1.0.0 to v1.1.0

### `diagrams/` - Architecture Diagrams

Visual representations of the Pipeworks system architecture.

| Diagram | Purpose |
|---------|---------|
| [01-c4-container-architecture.svg](diagrams/01-c4-container-architecture.svg) | C4 Container view showing all five components and their data flows |
| [02-layered-architecture-state-boundaries.svg](diagrams/02-layered-architecture-state-boundaries.svg) | Layered architecture showing pure vs stateful zones |
| [03-sequence-character-lifecycle.svg](diagrams/03-sequence-character-lifecycle.svg) | Sequence diagram of character appearing and being shown to player |

**Read these when:**
- You need to understand how components connect
- You're explaining the architecture to others
- You want to see the pure/stateful boundary
- You need to understand the complete data flow

**Best viewed in:**
- System Architecture document: [02_pipeworks_system_architecture.md](design/02_pipeworks_system_architecture.md)
- Or directly: Open the `.svg` files in a browser

### `images/` - Documentation Images

Visual assets referenced in documentation.

- `condition_axis.jpg` - Character condition examples
- `miss_filed.jpg` - Example generated character
- `verbs_conditions.jpg` - Prompting strategy visualization

---

## Documentation Philosophy

### These are working notes
The documentation in this directory reflects ongoing design thinking. It is deliberately informal in places and may contain incomplete thoughts or placeholders for future work.

### Conceptual before practical
Design documents prioritize explaining *why* over *how*. They exist to prevent architectural amnesia and ensure decisions can be revisited with full context.

### Bias over prescription
Like the generation systems themselves, documentation emphasizes bias and suggestion over hard rules. This preserves flexibility and allows systems to evolve.

---

## Reading Paths

### Path 1: I want to understand the big picture
1. [Character State Model](design/01_character_state_model.md) - Core concepts
2. [Pipeworks System Architecture](design/02_pipeworks_system_architecture.md) - How repos connect
3. [Pipeworks Components](design/03_pipeworks_components.md) - Component responsibilities

### Path 2: I want to generate characters
1. [Character Conditions Spec](design/specifications/condition_axis.md) - Implementation details
2. [Occupation Axis Spec](design/specifications/occupation_axis.md) - Occupation system
3. Check the main [CLAUDE.md](../CLAUDE.md) in repo root for code examples

### Path 3: I want to understand the philosophy
1. [Goblin Laws](design/00_goblin_laws.md) - Project principles
2. [Characters First](design/04_characters_first_narrow_door.md) - Design rationale
3. [Obey the Verb](design/specifications/Obey_the_Verb.md) - Prompting philosophy

### Path 4: I want to set up my environment
1. [Pre-Commit Hooks Setup](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) - Start here
2. [GitHub Actions Setup](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) - If configuring CI
3. Main [CLAUDE.md](../CLAUDE.md) for development commands

---

## Related Documentation

- **[CLAUDE.md](../CLAUDE.md)** - Main project documentation with commands, architecture overview, and code examples
- **[README.md](../README.md)** - Project README with installation and quick start
- **[Project_TODO_List.md](../Project_TODO_List.md)** - Current project status and tasks

---

## Document Status

All frontmatter has been removed from these documents. They are currently personal working notes and further refinement is needed before they can be considered complete reference documentation.

---

## Building the Documentation

This documentation is built using **Sphinx** and hosted on **ReadTheDocs**. You can build and preview the documentation locally before pushing changes.

### For Beginners: What is Sphinx?

Sphinx is a tool that takes your Markdown files and Python docstrings and turns them into beautiful, searchable HTML documentation. Think of it as a website generator specifically designed for software documentation.

### Quick Start: Build Documentation Locally

```bash
# 1. Install documentation tools
pip install -e ".[docs]"

# 2. Navigate to the docs directory
cd docs

# 3. Build the HTML documentation
sphinx-build -b html . _build/html

# 4. Open the documentation in your browser
# On macOS:
open _build/html/index.html
# On Linux:
xdg-open _build/html/index.html
# On Windows:
start _build/html/index.html
```

### What Gets Built?

When you run Sphinx, it:
1. Reads all the `.md` files in this directory
2. Reads the `.rst` files (like `index.rst`)
3. Extracts documentation from Python docstrings in `src/condition_axis/`
4. Generates a complete website in `_build/html/`

The built documentation includes:
- **Searchable content** - Full-text search across all docs
- **Navigation sidebar** - Easy browsing between sections
- **Syntax highlighting** - Properly formatted code examples
- **Cross-references** - Clickable links between related docs
- **Multiple formats** - HTML (web), PDF, and ePub

### Understanding the Sphinx Files

- **`conf.py`** - Sphinx configuration (theme, extensions, settings)
- **`index.rst`** - Main entry point that defines the table of contents
- **`_build/`** - Generated documentation (git-ignored, not committed)
- **`_static/`** - Custom CSS, JavaScript, and images for the docs
- **`_templates/`** - Custom HTML templates (if needed)

### Online Documentation (ReadTheDocs)

Once connected to ReadTheDocs, this documentation is automatically built and published whenever you push to GitHub. No manual deployment needed!

**Access the docs at:**
- Latest: `https://pipeworks-conditional-axis.readthedocs.io/en/latest/`
- Stable: `https://pipeworks-conditional-axis.readthedocs.io/en/stable/`

### Troubleshooting

**"sphinx-build: command not found"**
→ Install docs dependencies: `pip install -e ".[docs]"`

**"WARNING: toctree contains reference to nonexisting document"**
→ Check that all files referenced in `index.rst` actually exist

**"Build succeeded, X warnings"**
→ Warnings are usually safe to ignore, but check them to ensure links work correctly

---

## Contributing to Documentation

When adding or updating documentation:

1. **Design docs** (`design/`) - For architectural decisions and philosophy
2. **Specifications** (`design/specifications/`) - For technical implementation details
3. **Guides** (`guides/`) - For step-by-step processes and setup instructions
4. **Images** should go in `images/` and be referenced with relative paths

**Note**: These are currently working notes. Formal contribution guidelines will be established as the documentation matures.
