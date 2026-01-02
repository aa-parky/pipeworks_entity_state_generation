# 1 Pipeworks System Architecture

## 1.1 A Holistic View of Repositories, Responsibilities, and Data Flow

This document describes how the Pipeworks ecosystem fits together at a system level: the role of each repository, the direction of data flow, and the high-level integration contracts between components.

It is not a protocol specification.

It is not an API reference.

It is not a per-repo implementation guide.

It exists to keep the system comprehensible as it grows.

---

## 1.2 Pipeworks Context

| Repository                        | Role in Pipeworks                                     | Relationship to this Document                                                    |
| --------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------------------- |
| pipeworks-artefact                | Canonical Registry and memory layer for all artefacts | Defines identity, registration, and what may be persisted and resurfaced         |
| pipeworks_entity_state_generation | Generation engine for entity and character states     | Produces entity state snapshots from artefact identity and configuration         |
| pipeworks_mud_server              | Interactive runtime and game logic                    | Consumes entity states to run the world, respond to players, and manage sessions |
| pipeworks_image_generator         | Visualisation and image synthesis                     | Interprets entity states to generate images (on-demand or batch)                 |
| the_daily_undertaking_ui          | Narrative and user-facing singularity                 | Presents world state, narrative, and images to the player                        |

---

# 2 Core Philosophy

Pipeworks is built around **separation of concerns**.

Each repository is a narrowly-scoped component with an explicit responsibility. This prevents monolithic complexity and keeps the system extensible without requiring cross-repo entanglement.

The system follows the Goblin Laws in practice:

- keep boundaries clear
- avoid implementation leakage
- resist premature generality
- let complexity emerge only where proven necessary

Only _The Daily Undertaking_ may gossip across layers.

The real-world architecture documents do not.

---

# 3 Architecture at a Glance

Pipeworks is best understood as a pipeline. Data flows primarily in one direction through a set of transformation stages.

**(HOLD for MERMAID DIAGRAM)**

## 3.1 The Data Pipeline

1. **Registry (pipeworks-artefact)**
   The canonical source of truth for what exists (or is missing). Provides stable identity and minimal metadata.

2. **Generation Engine (pipeworks_entity_state_generation)**
   Takes identity + configuration and produces a resolved **entity state** (conditions, quirks, derived flags, generation metadata).

3. **MUD Server (pipeworks_mud_server)**
   Consumes entity state to instantiate and operate a living world: game logic, interactions, persistence of the _world_, and player sessions.

4. **Image Generator (pipeworks_image_generator)**
   Consumes entity state (plus context when useful) to generate a visual representation and associated metadata.

5. **UI (the_daily_undertaking_ui)**
   The singularity: presents narrative and world state to the player, blending text, interaction, and imagery.

---

# 4 Transition Zones (Where the System Hands Off)

Pipeworks remains manageable if hand-offs are explicit. Each boundary has a contract and an expected direction of responsibility.

## 4.1 Registry → Generation Engine

**Contract (high level):**

- Input: artefact identity + artefact kind + minimal metadata
- Output: entity state snapshot + generation metadata (seed/version/time)

**Responsibility split:**

- Registry: “this exists / existed / is missing”
- Generator: “this is what it is like _right now_”

## 4.2 Generation Engine → MUD Server

**Contract (high level):**

- Input: entity state snapshot
- Output: world integration (placement, behaviour context, interaction availability)

**Responsibility split:**

- Generator: produces state (pure, reproducible)
- MUD: uses state (situational, interactive, evolving)

## 4.3 MUD Server → Image Generator

**Contract (high level):**

- Input: entity state snapshot (+ optional situation context)
- Output: image artefact (bytes/url) + image metadata (model/settings/version)

**Responsibility split:**

- MUD: decides when imagery is needed and what context matters
- Image generator: produces visuals deterministically or acceptably-repeatably

## 4.4 MUD Server ↔ UI

**Contract (high level):**

- UI → MUD: player actions + session context
- MUD → UI: game state + narrative + entity info + references to images

**Communication pattern:**

- REST for discrete requests is acceptable
- WebSocket for continuous play / live updates is acceptable
- The interface should remain thin: the UI does not own world logic

## 4.5 Image Generator → UI

**Contract (high level):**

- UI consumes image references (URL/path) and displays them
- UI does not need to understand image generation internals

---

# 5 Data Contracts: What Moves Between Components

This section defines the _shape_ of interop without specifying schemas.

## 5.1 Artefact Identity (Registry output)

Artefact identity is:

- stable
- human-readable
- usable across logs, UI, and references

Example: `artf_mistress_of_mayhem`

## 5.2 Entity State (Generation output)

Entity state is a snapshot that typically includes:

- resolved conditions by axis (e.g., health/wealth/demeanour)
- quirks and modifiers
- derived flags used by downstream systems
- generation metadata (seed, version, timestamp)

Entity state is not “the character forever.”

It is “the character _as generated for this moment_.”

## 5.3 World State and Narrative (MUD output)

The MUD provides:

- current world state relevant to the player
- narrative response to player actions
- entity references (IDs, descriptions, optional pointers to state)

The MUD may persist world evolution independent of generator purity.

---

# 6 Example Flows

These examples illustrate system intent without locking implementation.

## 6.1 Character Appears and Is Shown

1. Registry records a character artefact (ID exists)
2. Generation Engine produces entity state for that ID
3. MUD Server places the entity in the world and exposes it to play
4. Image generator produces a visual for the entity state (on-demand)
5. UI presents narrative + image to the player

## 6.2 Player Interaction

1. UI sends a player action (e.g., “talk to goblin”)
2. MUD processes action using world state + entity state influences
3. MUD returns narrative outcome (+ any updated state references)
4. UI displays results

---

# 7 Key System Properties (Targets, Not Dogma)

- **Decoupling:** Components rely on contracts, not internal structures.
- **Reproducibility where useful:** The generator can be deterministic given the same inputs.
- **Extensibility:** New pipeline components may be added without rewriting existing ones.
- **Traceability:** When the system changes, we can say what changed and why.

Note: “statelessness” applies most strongly to the generator and image layer.

The MUD server and UI are expected to be sessionful.

---

# 8 Non-Goals

To avoid architectural drift, this document explicitly does not attempt to:

- define the full schema of entity state JSON
- define REST routes or WebSocket message formats
- specify database tables or migrations
- describe UI components or layout decisions
- describe image prompting strategies

Those details belong in component repositories and focused contract documents.

---

# 9 Future Extensions

Pipeworks may later add additional pipeline components (examples only):

- Audio generation
- Narrative synthesis modules
- Analytics / observability tooling

Any new component should integrate by:

- declaring its contract
- stating where it sits in the pipeline
- describing its responsibility boundary

---

# 10 Closing Note

This architecture is intentionally simple at the top level.

Simplicity here is what allows complexity in play.

Pipeworks can be chaotic in-world because it is disciplined out-of-world.
