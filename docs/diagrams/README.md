# Pipeworks Architecture Diagrams

This directory contains comprehensive architectural diagrams visualizing the Pipeworks ecosystem from multiple complementary perspectives.

## Overview

Three diagrams work together to provide a complete understanding of the system:

1. **C4 Container Architecture** - "What exists and how does it connect?"
2. **Layered Architecture with State Boundaries** - "How is the system organized?"
3. **Character Lifecycle Sequence** - "What actually happens?"

---

## Diagram 1: C4 Container Architecture

**File:** `01-c4-container-architecture.svg`
**Type:** C4 Container Diagram
**Purpose:** Shows all five Pipeworks components as containers with their technology boundaries and data flow contracts.

### What You'll See

- 👤 **Player** (External Actor)
- 📋 **pipeworks-artefact** (Canonical Registry) - Database/Registry
- ⚙️ **pipeworks_entity_state_generation** (Generation Engine) - Python Application
- 🌍 **pipeworks_mud_server** (Interactive Runtime) - Application
- 🎨 **pipeworks_image_generator** (Visualisation Layer) - Service
- 🎭 **the_daily_undertaking_ui** (Narrative Singularity) - Web Application

### Key Insights

✅ The Daily Undertaking UI is the **singularity** where all flows converge
✅ Clear separation: pure/stateless (Registry, Generator, Image Gen) vs stateful (MUD, UI)
✅ Bidirectional communication only exists: Player ↔ UI and MUD ↔ UI
✅ Unidirectional pipeline: Registry → Generator → MUD → Images → UI

### When to Use This Diagram

- Executive overview presentations
- System architecture documentation
- Explaining to stakeholders how components interact
- Understanding data flow contracts
- Identifying technology boundaries

---

## Diagram 2: Layered Architecture with State Boundaries

**File:** `02-layered-architecture-state-boundaries.svg`
**Type:** Layered Architecture
**Purpose:** Shows the five architectural layers and the critical pure/stateful boundary.

### What You'll See

```
┌─────────────────────────────────────┐
│ Layer 5: Player (User Domain)      │
├─────────────────────────────────────┤
│ Layer 4: UI (Narrative Singularity)│ ← STATEFUL ZONE
├─────────────────────────────────────┤
│ Layer 3: MUD + Image Gen (Runtime) │ ← Transition Point
├─────────────────────────────────────┤
│ Layer 2: Generator (Transformation)│ ← PURE ZONE
├─────────────────────────────────────┤
│ Layer 1: Registry (Identity)       │
└─────────────────────────────────────┘
```

### Key Insights

✅ **Pure Zone** (Registry, Generator, Image Gen): Deterministic, reproducible, stateless
✅ **Stateful Zone** (MUD, UI): Interactive, adaptive, evolving
✅ **Critical Transition**: Generator → MUD is where determinism ends
✅ **Layer 4 (UI)** is the only component allowed to "gossip across layers"
✅ Each layer has clear responsibilities and boundaries

### When to Use This Diagram

- Understanding architectural layers
- Explaining state management strategy
- Making decisions about where to place new functionality
- Understanding component responsibilities
- Debugging issues related to state management

---

## Diagram 3: Character Lifecycle Sequence

**File:** `03-sequence-character-lifecycle.svg`
**Type:** Sequence Diagram
**Purpose:** Shows a concrete example of how a character appears and is shown to the player.

### What You'll See

The complete flow through **six phases**:

1. **REGISTRATION** - Artefact identity established in Registry
2. **STATE GENERATION** - Pure transformation: ID + config → entity state
3. **WORLD INTEGRATION** - MUD places entity in living world
4. **VISUALIZATION** - Image Generator creates visual representation
5. **PLAYER PRESENTATION** - UI composes coherent narrative experience
6. **INTERACTION** - Player acts, loop continues

### Example: "artf_goblin_merchant"

The diagram follows a goblin merchant from registration through player interaction:
- Registry records the artefact
- Generator produces state: wiry, modest, suspicious, weathered
- MUD places in market square
- Image Gen creates visual
- UI presents: "A wiry, weathered goblin eyes you suspiciously..."
- Player interacts: "Talk to merchant"
- MUD responds with dialogue influenced by entity state

### Key Insights

✅ Complete end-to-end flow through all six phases
✅ Shows how pure and stateful zones interact in practice
✅ Demonstrates the interaction loop
✅ Reveals activation patterns and timing

### When to Use This Diagram

- Understanding actual system behavior
- Debugging issues in the pipeline
- Explaining workflows to developers
- Developer onboarding
- Planning new features that touch multiple components

---

## How These Diagrams Work Together

| Question | Use This Diagram |
|----------|------------------|
| What components exist? | **Diagram 1** (C4 Container) |
| How does data flow between components? | **Diagram 1** (C4 Container) |
| Which components are stateful vs stateless? | **Diagram 2** (Layered Architecture) |
| Where are the architectural layers? | **Diagram 2** (Layered Architecture) |
| What are each component's responsibilities? | **Diagram 2** (Layered Architecture) |
| What happens when a character appears? | **Diagram 3** (Sequence) |
| How does the pipeline work in practice? | **Diagram 3** (Sequence) |
| Where does pure become stateful? | **Diagram 2** + **Diagram 3** |

---

## Recommended Reading Order

### For Newcomers
1. Start with **Diagram 1** - Get the big picture
2. Move to **Diagram 2** - Understand layers and state
3. Finish with **Diagram 3** - See it in action

### For Developers
1. Start with **Diagram 3** - See concrete behavior
2. Reference **Diagram 2** - Understand which layer you're working in
3. Use **Diagram 1** - Verify component interactions

### For Architects
1. Study **Diagram 2** - Understand separation of concerns
2. Review **Diagram 1** - Verify boundaries and contracts
3. Validate with **Diagram 3** - Ensure flows are correct

---

## File Formats

Each diagram is available in two formats:

- **`.mmd`** - Mermaid source code (editable, version-controlled)
- **`.svg`** - Rendered SVG (viewable in browsers, embeddable in docs)

### Viewing the Diagrams

**In Browser:**
```bash
open 01-c4-container-architecture.svg
```

**In VS Code:**
```bash
code .
# Then open the .svg files
```

**In Documentation:**
The diagrams are referenced throughout the Sphinx documentation

---

## Updating the Diagrams

If the architecture changes, update the diagrams:

1. **Edit the `.mmd` source file** using Mermaid syntax
2. **Regenerate the SVG:**
   ```bash
   npx -p @mermaid-js/mermaid-cli mmdc -i diagram.mmd -o diagram.svg
   ```
3. **Commit both files** (`.mmd` and `.svg`)

### Mermaid Resources

- [Mermaid Live Editor](https://mermaid.live) - Test syntax online
- [Mermaid Documentation](https://mermaid.js.org/) - Full syntax reference
- [C4 Model](https://c4model.com/) - C4 diagram concepts

---

## Design Principles

These diagrams follow specific design principles:

### Color Coding
- 🟢 **Green**: User/Player (organic, human)
- 🔴 **Red**: UI Singularity (attention, importance, convergence)
- 🔵 **Blue**: Runtime components (trust, depth, complexity)
- 🟡 **Yellow**: Generation (transformation, energy, process)
- ⚫ **Gray**: Registry (stability, foundation, permanence)

### Emphasis Hierarchy
1. **The Daily Undertaking UI** - Largest, boldest (the singularity)
2. **MUD Server** - Critical stateful runtime
3. **Generator** - Critical pure transformation
4. **Registry & Image Gen** - Supporting components

### Layout Philosophy
- **Vertical layers** show architectural tiers
- **Horizontal zones** show state boundaries
- **Arrow thickness** implies data volume or importance
- **Bidirectional arrows** only where truly interactive

---

## Integration with Documentation

These diagrams are available throughout the documentation:

- **[docs/README.md](../README.md)** - Directory structure overview
- **Sphinx Documentation** - Referenced in API docs and guides
- **GitHub Repository** - Available in the docs/diagrams/ directory

---

## Questions?

If these diagrams don't answer your question, or if you think a new diagram would be helpful:

1. Check if the answer is in the architectural docs
2. Consider whether the question represents a gap in documentation
3. Propose a new diagram type if needed

**Remember:** Good diagrams show structure, flow, or state. If you're explaining behavior, consider a sequence diagram. If you're explaining organization, consider a layered diagram. If you're explaining connections, consider a container diagram.
