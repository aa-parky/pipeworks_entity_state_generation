# 1 **The Model Obeys Verbs and Conditions, Not Nouns**

_Notes on Job Titles, Occupation Design, and Prompt Nudging_

## 1.1 **Summary (Read This First)**

Image-generation models do **not** primarily reason about _job titles_.

They reason about **actions being performed** and **conditions under which those actions occur**.

In practical terms:

> **Verbs + conditions drive image generation.**

> **Nouns are decorative unless grounded in action.**

This principle underpins the design of the occupation axis, archetype bundles, and the safe use of whimsical or fictional job titles in _The Undertaking_.

---

## 1.2 **The Common Mistake: Title-First Prompting**

A frequent failure mode in prompting is assuming that naming a role is sufficient:

- “Goblin Time Warden”
- “Soul Auditor”
- “Memory Shepherd”

To a human reader, these are rich and evocative.

To an image model, they are **semantically thin** unless backed by physical action.

The model asks, implicitly:

- What is the body doing?
- What objects are being handled?
- What posture is required?
- What environment supports this activity?

If the prompt does not answer these questions, the model defaults to:

- generic fantasy poses
- static character portraits
- or unrelated visual tropes

---

## 1.3 **What The Model Actually Responds To**

Through testing, a consistent pattern emerges:

### 1.3.1 **The Model Responds Strongly to:**

- **Verbs** (writing, sorting, lifting, recording, repairing, observing)
- **Conditions** (heavy, unavoidable, discreet, corrosive, tolerated)
- **Material cues** (tools, desks, boxes, ledgers, debris)
- **Posture and repetition** (hunched, routine, methodical)

### 1.3.2 **The Model Responds Weakly to:**

- Abstract job titles
- Fictional institutional language
- Symbolic nouns without physical grounding

This is why the occupation axis works:

it encodes _how work is experienced_, not what it is called.

---

## 1.4 **The Safe Pattern: Activity-First, Title-Second**

To reliably nudge the model, occupation prompts should follow this structure:

```
[Activity Anchor] + [Condition Axis] (+ optional Job Title)
```

### 1.4.1 **Example (Effective)**

> “Their work is questioned, discreet, heavy, unavoidable, corrosive as they busy themselves with their tasks.”

This already produces a coherent image.

Adding a title:

> “Their work as a Soul Ledger Clerk is questioned, discreet, heavy, unavoidable, corrosive…”

…_does not change the core behaviour_.

The title rides on top of an already legible activity.

---

## 1.5 **Whimsical Job Titles: When They Work**

Whimsical or fictional occupations are **safe** _only_ when they decompose into mundane activities.

### 1.5.1 **Good (Activity-Legible)**

| **Job Title**     | **Implied Activities**           |
| ----------------- | -------------------------------- |
| Soul Ledger Clerk | writing, recording, counting     |
| Promise Sorter    | sorting, checking, filing        |
| Dream Tallyman    | observing, noting, waiting       |
| Rust Registrar    | inspecting, marking, cataloguing |

### 1.5.2 **Risky (Activity-Ambiguous)**

| **Job Title**    | **Problem**        |
| ---------------- | ------------------ |
| Time Warden      | No physical verb   |
| Fate Engineer    | Abstract, symbolic |
| Reality Shepherd | No material action |

If you cannot answer “what are their hands doing?”

the model probably can’t either.

---

## 1.6 **Why Conditions Matter More Than Titles**

Conditions such as:

- questioned
- tolerated
- unavoidable
- corrosive
- discreet

…do the real narrative and visual work.

They bias:

- posture (defensive, resigned, habitual)
- clothing (worn, functional, repaired)
- environment (expected but uncelebrated)
- emotional tone (routine, burdened, cautious)

A strong condition axis can carry a prompt _without any job title at all_.

This is intentional.

---

## 1.7 **Design Implication for The Undertaking**

In-world, this implies something important:

- Work exists **before** it is named
- Titles are coping mechanisms, not definitions
- Bureaucracy follows labour, not the other way around
- No one fully understands what the job is “for”

This aligns perfectly with:

- ledger-first storytelling
- archetype bundles
- goblin institutional drift

---

## 1.8 **Practical Heuristic (Use This)**

Before introducing a new job title, ask:

> **If I remove the title entirely, does the prompt still make sense?**

- If yes → the title is safe
- If no → add or clarify the activity and conditions

---

## 1.9 **Final Rule (Put This on a Wall)**

> **Image models obey verbs and conditions, not nouns.**

> **Titles decorate; actions decide.**

Everything in the occupation axis system is designed to exploit this fact — quietly, consistently, and without locking users into specific settings or genres.

---

If you want, next we can:

- turn this into a **Goblin Training Poster** (in-world),
- condense it into a **one-paragraph “law”**, or
- explicitly link it to archetype bundle design as a formal rule.

But as it stands: this is a _gold-standard note_.
