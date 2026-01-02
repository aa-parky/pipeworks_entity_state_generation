# 1 Character Conditions System

The Character Conditions system provides structured, rule-based character state generation for procedural content. Unlike simple text file lookups, it uses weighted probability distributions, semantic exclusion rules, and mandatory/optional axis policies to generate coherent character descriptions.

## 1.1 Overview

The system generates character states across multiple axes:

- **Physique**: Body structure (skinny, wiry, stocky, hunched, frail, broad)
- **Wealth**: Economic status (poor, modest, well-kept, wealthy, decadent)
- **Health**: Physical condition (sickly, scarred, weary, hale, limping)
- **Demeanor**: Behavioral presentation (timid, suspicious, resentful, alert, proud)
- **Age**: Life stage (young, middle-aged, old, ancient)

## 1.2 Key Features

### 1.2.1 Weighted Probability

The system uses realistic population distributions:

```python
WEIGHTS = {
	"wealth": {
	"poor": 4.0, # Most common
	"modest": 3.0,
	"well-kept": 2.0,
	"wealthy": 1.0,
	"decadent": 0.5, # Rare
	}
}
```

This creates a believable population where most characters are poor or modest, and wealthy/decadent characters are rare.

### 1.2.2 Semantic Exclusions

Rules prevent illogical combinations:

- Decadent characters can’t be frail or sickly (wealth enables health care)
- Ancient characters aren’t timid (age brings confidence)
- Broad, strong physiques don’t pair with sickness
- Hale (healthy) characters shouldn’t have frail physiques

### 1.2.3 Mandatory/Optional Axes

- **Mandatory**: Always include physique and wealth (establish baseline)
- **Optional**: Include 0-2 additional axes (add narrative detail)
- **Max Optional**: Prevents prompt dilution and maintains clarity

# 2 Condition Axis System (Working Notes)

## 2.1 Purpose

This note explores the idea of **conditions as axes** rather than states, flags, or debuffs.

The intent is not to define what *is true* about a character, system, or situation, but to **bias how outcomes are interpreted and resolved**.

Conditions operate as *signals*, not diagnoses.

---

## 2.2 Core Philosophy

### 2.2.1 Conditions Are Not States

A condition is **not**:

- a binary flag
- a hard rule
- a medical, mechanical, or moral judgement

A condition **does not say**:

> “You are injured.”

It **suggests**:

> “Resolution should lean toward fragility, hesitation, or cost.”

---

### 2.2.2 Axes, Not Labels

Each condition exists on an **axis**, not as an on/off switch.

Examples:

- Clear ↔ Clouded
- Stable ↔ Precarious
- Ready ↔ Unprepared
- Legitimate ↔ Questioned
- Rested ↔ Strained

The system never asks *“Do you have the condition?”*

It asks *“Where along this axis does interpretation tilt?”*

---

### 2.2.3 Modulation Over Definition

Conditions **modulate resolution**, they do not define outcomes.

They:

- influence success vs. failure *margins*
- bias tone, consequence, and cost
- colour narrative and mechanical interpretation

They **do not**:

- prescribe specific actions
- forbid attempts
- override agency

This preserves play, ambiguity, and emergence.

---

## 2.3 Behavioural Effects

### 2.3.1 Conditions Bias Interpretation

Good systems shape behaviour by **biasing interpretation**, not by narrowing possibility.

A strained character may still succeed —

but success may:

- cost more
- take longer
- attract attention
- leave residue in the ledger

Failure is not punishment.

It is **data**.

---

### 2.3.2 Conditions Can Coexist

Multiple axes may be active simultaneously.

Examples:

- High readiness + low legitimacy
- Physical stability + cognitive strain
- Strong authority + eroding trust

Conditions compound **softly**, not arithmetically.

No single axis should dominate resolution unless deliberately designed to.

---

## 2.4 System Perspective

### 2.4.1 Observed, Not Owned

Conditions are not something a character *has*.

They are something the **system observes**:

- about a situation
- about context
- about accumulated history

This avoids:

- medicalisation
- moral judgement
- RPG-style debuff stacking

It aligns conditions with **ledger thinking**:

what has happened leaves traces.

---

### 2.4.2 No Hard Locks

Conditions should rarely — if ever — hard-lock actions.

Instead, they:

- increase risk
- alter narrative framing
- change secondary effects
- influence downstream consequences

Attempt is always allowed.

Interpretation is where weight lives.

---

## 2.5 Design Implications

### 2.5.1 Conditions as Resolution Inputs

In resolution logic, conditions act as:

- bias weights
- threshold nudges
- narrative tone selectors
- consequence multipliers

They should be:

- readable
- explainable
- inspectable after the fact

Nothing hidden. Everything accountable.

---

### 2.5.2 Language Matters

Condition language should avoid:

- clinical terminology
- punitive framing
- RPG optimisation language

Prefer:

- situational
- descriptive
- slightly deniable phrasing

Conditions should feel *observed*, not *assigned*.

---

## 2.6 Status

This is a **conceptual foundation**, not a final system.

Formalisation should emerge *after*:

- play
- misuse
- edge cases
- narrative friction

You’ve crossed the important threshold already.
