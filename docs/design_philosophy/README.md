# Design & Philosophy

This directory documents the conceptual foundations, architectural decisions, and design philosophy behind the Pipeworks Conditional Axis system.

## Purpose

These documents exist to:

- **Preserve design intent** - Why decisions were made, not just what was built
- **Maintain philosophical alignment** - Keep the broader Pipeworks vision coherent across repositories
- **Prevent architectural amnesia** - Record the reasoning so future-us doesn't undo good decisions

This is not API documentation. This is not a tutorial. This is the **why** behind the **what**.

---

## Pipeworks Context

The `pipeworks_entity_state_generation` repository is one component in a larger ecosystem:

| Repository                        | Role in Pipeworks                                     | Relationship to this Repository                                   |
| --------------------------------- | ----------------------------------------------------- | ----------------------------------------------------------------- |
| pipeworks-artefact                | Canonical Registry and memory layer for all artefacts | Receives generated character states for registration and storage  |
| pipeworks_entity_state_generation | Generation engine for entity and character states     | **This repository** - produces character states from axis systems |
| pipeworks_mud_server              | Interactive runtime and game logic                    | Consumes entity states to run the living world                    |
| pipeworks_image_generator         | Visualisation and image synthesis                     | Interprets entity states for visual representation                |
| the_daily_undertaking_ui          | Narrative and user-facing singularity                 | Presents characters and world state to the player                 |

---

## Navigation

### Philosophy

Core design philosophy, architectural principles, and system thinking.

- **[Goblin Laws](philosophy/00_goblin_laws.md)** - Universal design principles for tinkering, systems, and survival
- **[Character State Model](philosophy/01_character_state_model.md)** - How Pipeworks understands character state as bias, not definition
- **[System Architecture](philosophy/02_system_architecture.md)** - The five components, their responsibilities, data flow, and integration contracts
- **[Design Decision: Characters First](philosophy/03_design_decision_characters_first.md)** - Why characters were the first artefact domain (design decision record)

### Conceptual Design

Detailed axis specifications, templates, and implementation patterns.

- **[Condition Axis Specification](conceptual_design/condition_axis.md)** - Character conditions system (physique, wealth, health, demeanor, age)
- **[Occupation Axis Specification](conceptual_design/occupation_axis.md)** - Occupation characteristics (legitimacy, visibility, moral load, dependency, risk)
- **[Prompt Design Principles](conceptual_design/Obey_the_Verb.md)** - How image models respond to verbs and conditions, not nouns

---

## Document Types

You'll encounter three kinds of documents here:

1. **Philosophical Foundations** - Conceptual models and core principles (e.g., Goblin Laws, Character State Model)
2. **Architectural Decisions** - Why the system is structured this way (e.g., Characters First)
3. **Technical Specifications** - What the system actually does (e.g., axis definitions, weights, exclusions)

---

## Reading Guidance

- **New to Pipeworks?** Start with Goblin Laws → System Architecture → Character State Model
- **Implementing a feature?** Check the relevant specification in `conceptual_design/`
- **Questioning a design choice?** Look for the decision record (e.g., Characters First)
- **Adding a new axis or system?** Read the existing specifications to understand the pattern

---

## Contributing to Design Docs

These documents should remain:

- **Deliberately modest** - Prefer suggestion over assertion
- **Implementation-independent** - Don't lock in database schemas or API routes here
- **Narrative-driven** - Written for humans trying to understand intent, not machines
- **Stable** - Changes should be rare and well-considered

If you're about to add a new document, ask:

- Does this explain **why** something is designed this way?
- Or does it describe **how** to use it? (That might belong in technical docs instead)

---

## Maintenance Notes

- The **Pipeworks Context table** is maintained once, in this README
- Documents are intentionally standalone-readable (minimal cross-references)
- Numbering (00, 01, 02...) indicates suggested reading order, not importance
