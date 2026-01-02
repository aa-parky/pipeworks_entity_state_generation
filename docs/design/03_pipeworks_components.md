# 1 Pipeworks Components

## 1.1 The Five Load-Bearing Parts of the System

This document describes the five primary components that make up the Pipeworks ecosystem, their individual responsibilities, and how they fit together as a coherent system.

It does not describe internal implementation.
It does not replace per-repository documentation.
It exists to provide a single, stable point of architectural orientation.

---

## 1.2 Pipeworks Context

| Repository                        | Role in Pipeworks     | Responsibility Summary                                           |
| --------------------------------- | --------------------- | ---------------------------------------------------------------- |
| pipeworks-artefact                | Canonical Registry    | Defines what exists, what is missing, and what may be remembered |
| pipeworks_entity_state_generation | Generation Engine     | Produces resolved entity and character state snapshots           |
| pipeworks_mud_server              | Interactive Runtime   | Operates the living world and responds to player actions         |
| pipeworks_image_generator         | Visualisation Layer   | Generates images from entity state                               |
| the_daily_undertaking_ui          | Narrative Singularity | Presents the world to the player                                 |

---

## 1.3 pipeworks-artefact

### 1.3.1 The Registry Layer

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

---

## 1.4 pipeworks_entity_state_generation

### 1.4.1 The Generation Engine

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

> _“Given what this thing is, what is it like right now?”_

---

## 1.5 pipeworks_mud_server

### 1.5.1 The Interactive Runtime

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

---

## 1.6 pipeworks_image_generator

### 1.6.1 The Visualisation Layer

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

---

## 1.7 the_daily_undertaking_ui

### 1.7.1 The Narrative Singularity

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

---

## 1.8 How the Components Work Together

At a high level, Pipeworks operates as a directional pipeline:

1. **Artefacts are registered**
2. **Entity state is generated**
3. **The world is run interactively**
4. **Images are produced as needed**
5. **The experience is presented to the player**

Each component:

- does one job
- hands off cleanly
- avoids reaching backward into other layers

---

## 1.9 Boundary Discipline

The system remains manageable because boundaries are respected:

- The registry remembers, but does not simulate
- The generator describes, but does not persist
- The MUD runs the world, but does not redefine entities
- The image layer visualises, but does not narrate
- The UI narrates, but does not govern the world

If a concern feels like it belongs to more than one component,
it probably belongs in **none of them yet**.

---

## 1.10 Closing Note

Pipeworks is deliberately boring at the architectural level.

That boredom is what allows the in-world system to be strange, surprising, and alive.

When in doubt:

- clarify the boundary
- respect the hand-off
- resist cleverness

The chaos belongs on the inside.
