# Character State Model

## Conditions, Axes, and Bias in Pipeworks

This document defines how Pipeworks understands and describes the _state_ of a character.

It does not describe how characters are generated, stored, or rendered.

It describes what a character _is allowed to be_, conceptually, so that generation,

registration, and narrative systems can operate without contradiction.

---

# Character State as a Concept

In Pipeworks, a character is not defined by a fixed set of traits or statistics. Instead, a character is understood as a **stateful composition of conditions** observed along multiple axes.

**A character state:**

- is descriptive, not prescriptive
- represents how a character is perceived or situated
- may change over time without invalidating past states
- is always incomplete

This allows characters to evolve, contradict themselves, or be remembered differently without requiring retroactive correction.

---

# Conditions

A **condition** is a qualitative descriptor that captures an aspect of a character’s current state.

**Examples include:**

- weary
- well-kept
- suspicious
- limping
- modest
- proud

**Conditions are:**

- intentionally imprecise
- culturally and narratively legible
- interpretable across species, roles, and embodiments

A condition does not encode mechanics.

It encodes _signal_.

---

# Axes

An **axis** is a bounded conceptual dimension along which one or more conditions may apply.

**Typical axes include:**

- Physique
- Wealth
- Health
- Demeanour
- Age

Axes exist to:

- prevent combinatorial chaos
- ensure conditions are contextually compatible
- provide structure without enforcing specificity

An axis does not describe a character directly.

It defines _where interpretation is allowed to operate_.

---

# Bias, Not Definition

Pipeworks deliberately avoids defining characters through fixed attributes or prohibitions.

Instead, it uses **bias**.

Conditions and axes bias how a character is interpreted by:

- generation systems
- narrative framing
- visual rendering
- player perception

**For example:**

- “weathered” biases emphasis toward age, wear, or exposure
- “well-kept” biases restraint, order, and maintenance
- “suspicious” biases posture, gaze, and interaction tone

**This approach:**

- preserves flexibility
- avoids over-specification
- allows meaning to emerge through context

Good systems shape behaviour by biasing interpretation, not by narrowing possibility.

---

# Weighted Presence

Conditions are not equally likely.

Each axis maintains an internal weighting that reflects:

- population realism
- cultural context
- narrative tone

This allows Pipeworks to generate characters that feel:

- statistically grounded
- socially plausible
- narratively coherent

Weights influence _frequency_, not _certainty_.

Rare conditions are possible.

Common conditions are not guaranteed.

---

# Compatibility and Exclusion

Some conditions are incompatible or contextually unlikely when combined.

Rather than hard rules, Pipeworks uses **semantic exclusion**:

- certain combinations are suppressed
- others are merely discouraged
- no combination is absolutely forbidden without cause

This keeps the system expressive while avoiding obvious contradictions.

---

# Independence from Implementation

This model intentionally avoids reference to:

- database schema
- APIs
- storage format
- rendering logic

Those concerns belong elsewhere.

This document exists so that:

- generation can remain pure
- registration can remain cautious
- narrative can remain flexible

If an implementation detail contradicts this model, the implementation is wrong.

---

# Relationship to the Register

A character state is registrable.

When a character is remembered, the Register records:

- that this state existed
- when it was observed
- under what circumstances

Past states are not overwritten. They become part of the character’s history.

This allows Pipeworks to support:

- change over time
- unreliable memory
- narrative drift
- rediscovery

---

# Closing Note

This model is deliberately modest.

It prefers suggestion over assertion, bias over definition, and structure over exhaustiveness.

Its purpose is not to describe characters completely, but to ensure they can exist, change, and be remembered without collapsing the system around them.
