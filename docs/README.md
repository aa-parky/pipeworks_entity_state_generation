# Pipeworks Entity State Generation Documentation

This directory contains design documents, technical specifications, and setup guides for the `pipeworks_entity_state_generation` project.

## Quick Navigation

### New to the Project?
Start here:
1. [Character State Model](design/01_character_state_model.md) - Understand the core conceptual model
2. [Pipeworks System Architecture](design/02_pipeworks_system_architecture.md) - See how components fit together
3. [Character Conditions Spec](specifications/condition_axis.md) - Learn the actual implementation

### Setting Up Development?
1. [Pre-Commit Hooks Setup Guide](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) - Local development setup
2. [GitHub Actions CI Setup Guide](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) - CI/CD configuration

### Working on Character Generation?
- [Character Conditions System](specifications/condition_axis.md) - Physical & social character states
- [Occupation Axis System](specifications/occupation_axis.md) - Occupation characteristics
- [Obey the Verb](specifications/Obey_the_Verb.md) - AI image generation prompting strategy

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

### `specifications/` - Technical Specifications

Implementation details for the generation systems. These documents describe *what* the system does and *how* it works.

| Document | Purpose |
|----------|---------|
| [condition_axis.md](specifications/condition_axis.md) | Character condition system (physique, wealth, health, demeanor, age) |
| [occupation_axis.md](specifications/occupation_axis.md) | Occupation axis system (legitimacy, visibility, moral load, etc.) |
| [Obey_the_Verb.md](specifications/Obey_the_Verb.md) | Image model prompting strategy (verbs > nouns) |

**Read these when:**
- You're implementing character generation features
- You're adding new axes or conditions
- You're integrating with image generation systems

### `guides/` - Setup & Process Guides

Step-by-step instructions for setting up development tools and CI/CD.

| Document | Purpose |
|----------|---------|
| [Pre-Commit Hooks Setup Guide.md](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) | Local git hooks for code quality |
| [GitHub Actions CI Setup Guide.md](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) | Automated testing and linting |

**Read these when:**
- You're setting up your development environment
- You're troubleshooting CI failures
- You're configuring new hooks or workflows

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
1. [Character Conditions Spec](specifications/condition_axis.md) - Implementation details
2. [Occupation Axis Spec](specifications/occupation_axis.md) - Occupation system
3. Check the main [CLAUDE.md](../CLAUDE.md) in repo root for code examples

### Path 3: I want to understand the philosophy
1. [Goblin Laws](design/00_goblin_laws.md) - Project principles
2. [Characters First](design/04_characters_first_narrow_door.md) - Design rationale
3. [Obey the Verb](specifications/Obey_the_Verb.md) - Prompting philosophy

### Path 4: I want to set up my environment
1. [Pre-Commit Hooks Setup](guides/Pre-Commit%20Hooks%20Setup%20Guide.md) - Start here
2. [GitHub Actions Setup](guides/GitHub%20Actions%20CI%20Setup%20Guide.md) - If configuring CI
3. Main [CLAUDE.md](../CLAUDE.md) for development commands

---

## Related Documentation

- **[../CLAUDE.md](../CLAUDE.md)** - Main project documentation with commands, architecture overview, and code examples
- **[../README.md](../README.md)** - Project README with installation and quick start
- **[../Project_TODO_List.md](../Project_TODO_List.md)** - Current project status and tasks

---

## Document Status

All frontmatter has been removed from these documents. They are currently personal working notes and further refinement is needed before they can be considered complete reference documentation.

---

## Contributing to Documentation

When adding or updating documentation:

1. **Design docs** (`design/`) - For architectural decisions and philosophy
2. **Specifications** (`specifications/`) - For technical implementation details
3. **Guides** (`guides/`) - For step-by-step processes and setup instructions
4. **Images** should go in `images/` and be referenced with relative paths

**Note**: These are currently working notes. Formal contribution guidelines will be established as the documentation matures.
