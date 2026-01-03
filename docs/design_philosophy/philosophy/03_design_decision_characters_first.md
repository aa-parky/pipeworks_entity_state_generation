# Design Decision: Characters First

> _This document records a deliberate early decision in the design of the Pipeworks Register:
> to introduce characters as the first specialised artefact domain, without abandoning the principle that everything is, ultimately, an artefact._
>
> _This was a narrow door into the Register—a deliberate sequencing choice, not an optimisation._
>
> _Future readers (including future-us) are encouraged to read this document before questioning the structure._

---

## Boundary Contract

### What Character Generation Hands to the Register

The[ pipeworks_entity_state_generation ](https://github.com/aa-parky/pipeworks_entity_state_generation.git) project is responsible for **how characters come to be**.

The `pipeworks-artefact` project is responsible for **that a character exists**.

These responsibilities must not blur.

### Character Generation Responsibilities

Character generation:

- operates as a **pure system**
- consumes configuration, weights, axes, and conditions
- produces a **generated character state**
- does not care whether the character is remembered, reused, or discarded

Its output is a _snapshot_, not a commitment.

### The Hand-off Object (Conceptual)

Character generation hands the Register a package containing:

- a **stable artefact identifier** (or a request for one)
- a **generation timestamp**
- the **resolved axis outcomes**
- any **generation metadata** (seed, version, profile)
- an optional **narrative summary** suitable for registration

It does **not**:

- write directly to the database
- manage identity lifecycle
- decide canonical status
- know where or how the character will reappear

The Register decides what happens next.

### Register Responsibilities

Upon receiving a generated character state, the Register may:

- register it as a new artefact
- associate it with an existing artefact
- mark it as provisional, dormant, or active
- store the state verbatim, without interpretation

The Register records.

It does not judge.

---

## The Minimal Character Table

### A Specialisation That Still Belongs to the Artefact World

Although all things are artefacts in principle, this project introduces a **character-specific table early** as a practical concession.

This does not violate the artefact model.

It demonstrates it.

### Why a Character Table Exists

Characters:

- are stateful
- are revisited
- evolve over time
- are frequently referenced
- are central to Page 2 continuity

Attempting to model this cleanly inside a single generic table too early would increase cognitive load and slow iteration.

The character table exists to make early work **tractable**, not permanent.

### Conceptual Structure (Non-SQL)

At minimum, a character record captures:

- artefact identity
- generation provenance
- resolved condition axes
- current narrative state
- timestamps

Crucially:

> **Every character row is anchored to an artefact identity.**

The character table does not replace the Register.

It **folds back into it**.

### Folding Back into Artefact Thinking

The governing rule is:

> _A character is an artefact with character-specific structure._

This means:

- artefact identity remains stable
- characters can be referenced without knowing their schema
- characters can later gain relationships to places, notices, titles, or absences
- future artefact queries do not need to understand character internals

If the character table disappeared tomorrow, the Register would still know:

- that the character existed
- that it mattered
- that it was registered

This is the litmus test.

---

## Why Characters First

### A Note for Future-Us

Characters are not philosophically privileged.

They are **operationally demanding**.

Starting with characters is a deliberate stress test of the Register’s design, because characters:

- require memory
- require revision
- require resurfacing
- require reconciliation between generated state and narrative use

If the Register can support characters cleanly, it can support anything.

Places, timetables, rooms, notices, and titles are structurally simpler.

They can follow once the character pathway is proven.

This choice aligns with Goblin Law principles:

- build the smallest thing that proves the rule
- resist premature generality
- prefer clarity over cleverness
- allow the system to grow under real pressure

If you are reading this and wondering:

> “Why didn’t we just make everything generic from the start?”

The answer is:

> Because we were building a system meant to last, not one meant to look complete early.

Characters came first so the Register could learn to remember.

---

## Closing Note

This document exists to prevent architectural amnesia.

If you are about to:

- remove the character table
- generalise everything
- introduce a framework
- or declare this decision “temporary and messy”

Pause.

Read this again.

Then check whether the current pain actually justifies the change.

Most of the time, it won’t.
