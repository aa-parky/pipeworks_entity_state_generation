# Pipeworks System Architecture

## Overview

This document describes how the Pipeworks ecosystem fits together: the five primary components, their responsibilities, the direction of data flow, and the integration contracts between them.

It is not a protocol specification.

It is not an API reference.

It is not a per-repo implementation guide.

It exists to keep the system comprehensible as it grows, providing a single stable point of architectural orientation.

---

# Core Philosophy

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

# Architecture at a Glance

Pipeworks is best understood as a pipeline. Data flows primarily in one direction through a set of transformation stages.

## System Architecture Diagrams

Three complementary diagrams visualize the Pipeworks ecosystem from different perspectives:

### Diagram 1: C4 Container Architecture

Shows all five components, their technology boundaries, and data flow contracts.

![C4 Container Architecture](../../diagrams/01-c4-container-architecture.svg)

**Key Insights:**
- The Daily Undertaking UI is the **singularity** where all flows converge
- Clear separation between pure/stateless components (Registry, Generator, Image Gen) and stateful components (MUD, UI)
- Bidirectional communication only exists between Player ↔ UI and MUD ↔ UI
- Unidirectional pipeline: Registry → Generator → MUD → Images → UI

### Diagram 2: Layered Architecture with State Boundaries

Shows the five architectural layers and the critical pure/stateful boundary.

![Layered Architecture](../../diagrams/02-layered-architecture-state-boundaries.svg)

**Key Insights:**
- **Pure Zone** (Registry, Generator, Image Gen): Deterministic, reproducible, stateless
- **Stateful Zone** (MUD, UI): Interactive, adaptive, evolving
- **Critical Transition**: Generator → MUD is where determinism ends and adaptation begins
- **Layer 4 (UI)** is the only component allowed to "gossip across layers"
- Each layer has clear responsibilities and boundaries

### Diagram 3: Character Lifecycle Sequence

Shows a concrete example: how a character appears and is shown to the player.

![Sequence Diagram](../../diagrams/03-sequence-character-lifecycle.svg)

**Key Insights:**
- Complete end-to-end flow through all six phases
- Registry provides identity → Generator produces state → MUD integrates into world → Image Gen visualizes → UI presents to player
- Shows the interaction loop: player actions feed back into the MUD
- Demonstrates how pure and stateful zones interact in practice

---

# The Five Components

Each component has a distinct responsibility and fits into the overall data pipeline.

## pipeworks-artefact: The Registry Layer

The artefact repository provides the **canonical register** for Pipeworks.

Its responsibility is not behaviour, simulation, or narrative.
Its responsibility is **memory**.

The registry records:

- that something exists (or existed)
- what kind of thing it is
- when it was registered or last observed
- minimal descriptive context

It does not attempt to fully describe or explain artefacts.
It provides stable identity and continuity so that other systems can safely refer to the same thing over time.

If an entity appears anywhere in Pipeworks, it should be possible to trace it back to an artefact entry.

**Pipeline position:** Provides canonical identity (entry point)

---

## pipeworks_entity_state_generation: The Generation Engine

The generation engine is responsible for **producing entity state**.

Given:

- an artefact identity
- configuration
- conditional axes
- weights and quirks

it produces a **resolved state snapshot** describing what that entity is like at a particular moment.

The generation engine:

- is intentionally pure
- does not store long-term memory
- does not manage identity lifecycle
- does not know how or where the state will be used

It answers the question:

> _"Given what this thing is, what is it like right now?"_

**Pipeline position:** Transforms identity into resolved state

---

## pipeworks_mud_server: The Interactive Runtime

The MUD server is the **heart of the live system**.

It consumes entity state and:

- places entities into a world
- manages player sessions
- enforces game logic
- evolves world state over time
- responds to player actions

Unlike the generation engine, the MUD server is expected to be:

- stateful
- situational
- adaptive

It is where chaos is allowed — and controlled.

The MUD server does not generate entities from scratch and does not own canonical identity.
It operates on what has already been defined and generated.

**Pipeline position:** Runs the living world (stateful transition point)

---

## pipeworks_image_generator: The Visualisation Layer

The image generator creates **visual representations** of entities.

It consumes:

- entity state snapshots
- optional contextual information

and produces:

- images
- associated generation metadata

The image generator:

- does not own narrative meaning
- does not manage world state
- does not decide when images are required

It exists to translate state into imagery when requested by upstream systems.

**Pipeline position:** Produces visual representations on demand

---

## the_daily_undertaking_ui: The Narrative Singularity

The Daily Undertaking UI is the **only place where everything comes together**.

It is:

- player-facing
- narrative-driven
- allowed to gossip across layers

The UI:

- receives world state and narrative from the MUD server
- displays images generated elsewhere
- surfaces artefacts and characters to the player
- presents the world as a coherent experience

Unlike the other components, the UI is not required to be restrained.
Its job is to _feel alive_.

**Pipeline position:** Converges all flows for player experience (singularity)

---

# Component Integration

## How the Pipeline Flows

At a high level, Pipeworks operates as a directional pipeline:

1. **Artefacts are registered** (Registry)
2. **Entity state is generated** (Generator)
3. **The world is run interactively** (MUD)
4. **Images are produced as needed** (Image Gen)
5. **The experience is presented to the player** (UI)

Each component:

- does one job
- hands off cleanly
- avoids reaching backward into other layers

## Transition Zones (Where the System Hands Off)

Pipeworks remains manageable if hand-offs are explicit. Each boundary has a contract and an expected direction of responsibility.

### Registry → Generation Engine

**Contract (high level):**

- Input: artefact identity + artefact kind + minimal metadata
- Output: entity state snapshot + generation metadata (seed/version/time)

**Responsibility split:**

- Registry: "this exists / existed / is missing"
- Generator: "this is what it is like _right now_"

### Generation Engine → MUD Server

**Contract (high level):**

- Input: entity state snapshot
- Output: world integration (placement, behaviour context, interaction availability)

**Responsibility split:**

- Generator: produces state (pure, reproducible)
- MUD: uses state (situational, interactive, evolving)

### MUD Server → Image Generator

**Contract (high level):**

- Input: entity state snapshot (+ optional situation context)
- Output: image artefact (bytes/url) + image metadata (model/settings/version)

**Responsibility split:**

- MUD: decides when imagery is needed and what context matters
- Image generator: produces visuals deterministically or acceptably-repeatably

### MUD Server ↔ UI

**Contract (high level):**

- UI → MUD: player actions + session context
- MUD → UI: game state + narrative + entity info + references to images

**Communication pattern:**

- REST for discrete requests is acceptable
- WebSocket for continuous play / live updates is acceptable
- The interface should remain thin: the UI does not own world logic

### Image Generator → UI

**Contract (high level):**

- UI consumes image references (URL/path) and displays them
- UI does not need to understand image generation internals

---

# Data Contracts: What Moves Between Components

This section defines the _shape_ of interop without specifying schemas.

## Artefact Identity (Registry output)

Artefact identity is:

- stable
- human-readable
- usable across logs, UI, and references

Example: `artf_mistress_of_mayhem`

## Entity State (Generation output)

Entity state is a snapshot that typically includes:

- resolved conditions by axis (e.g., health/wealth/demeanour)
- quirks and modifiers
- derived flags used by downstream systems
- generation metadata (seed, version, timestamp)

Entity state is not "the character forever."

It is "the character _as generated for this moment_."

## World State and Narrative (MUD output)

The MUD provides:

- current world state relevant to the player
- narrative response to player actions
- entity references (IDs, descriptions, optional pointers to state)

The MUD may persist world evolution independent of generator purity.

---

# Example Flows

These examples illustrate system intent without locking implementation.

## Character Appears and Is Shown

1. Registry records a character artefact (ID exists)
2. Generation Engine produces entity state for that ID
3. MUD Server places the entity in the world and exposes it to play
4. Image generator produces a visual for the entity state (on-demand)
5. UI presents narrative + image to the player

## Player Interaction

1. UI sends a player action (e.g., "talk to goblin")
2. MUD processes action using world state + entity state influences
3. MUD returns narrative outcome (+ any updated state references)
4. UI displays results

---

# Boundary Discipline

The system remains manageable because boundaries are respected:

- The registry remembers, but does not simulate
- The generator describes, but does not persist
- The MUD runs the world, but does not redefine entities
- The image layer visualises, but does not narrate
- The UI narrates, but does not govern the world

If a concern feels like it belongs to more than one component, it probably belongs in **none of them yet**.

---

# Key System Properties (Targets, Not Dogma)

- **Decoupling:** Components rely on contracts, not internal structures.
- **Reproducibility where useful:** The generator can be deterministic given the same inputs.
- **Extensibility:** New pipeline components may be added without rewriting existing ones.
- **Traceability:** When the system changes, we can say what changed and why.

Note: "statelessness" applies most strongly to the generator and image layer.

The MUD server and UI are expected to be sessionful.

---

# Non-Goals

To avoid architectural drift, this document explicitly does not attempt to:

- define the full schema of entity state JSON
- define REST routes or WebSocket message formats
- specify database tables or migrations
- describe UI components or layout decisions
- describe image prompting strategies

Those details belong in component repositories and focused contract documents.

---

# Future Extensions

Pipeworks may later add additional pipeline components (examples only):

- Audio generation
- Narrative synthesis modules
- Analytics / observability tooling

Any new component should integrate by:

- declaring its contract
- stating where it sits in the pipeline
- describing its responsibility boundary

---

# Closing Note

Pipeworks is deliberately boring at the architectural level.

That boredom is what allows the in-world system to be strange, surprising, and alive.

When in doubt:

- clarify the boundary
- respect the hand-off
- resist cleverness

This architecture is intentionally simple at the top level. Simplicity here is what allows complexity in play.

Pipeworks can be chaotic in-world because it is disciplined out-of-world.

The chaos belongs on the inside.
