# Part 1 — Baseline Occupation Axis Bundle (Template)

This is the **minimum viable bundle** that:

- biases image generation
- informs character narrative
- scales beyond goblins
- doesn’t collapse into class mechanics

Think of this as the _ledger header_ for an occupation.

---

## Occupation Axis Bundle (v0.1)

Each occupation expresses **pressure**, not identity, across five axes.

```
occupation_axis = {
    "legitimacy":        "",  # sanctioned | tolerated | questioned | illicit
    "visibility":        "",  # hidden | discreet | routine | conspicuous
    "moral_load":        "",  # neutral | burdened | conflicted | corrosive
    "dependency":        "",  # optional | useful | necessary | unavoidable
    "risk_exposure":     "",  # benign | straining | hazardous | eroding
}
```

### Why These Five (brief rationale)

- **Legitimacy** → posture, confidence, dress coherence
- **Visibility** → lighting, eye-line, staging
- **Moral Load** → facial tension, age, restraint
- **Dependency** → status _without_ hierarchy
- **Risk Exposure** → physical & environmental wear

These map _beautifully_ onto:

- your existing physical / facial axes
- diffusion model priors
- narrative tone

No axis says _what_ the job is.

They only say _what living with it feels like_.

---

## Axis Language Rule (important)

Axis values must be:

- adjectival
- socially legible
- deniable

❌ bad: evil, heroic, important

✅ good: questioned, routine, eroding

---

# Part 2 — 10 Whimsical Goblin Occupation Archetypes

Each archetype includes:

1. Axis Bundle (system-facing)
2. Narrative Handles (text-facing examples)

I’ll keep the prose light but _very goblin_.

---

## Fishing Lure Tuner

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "routine",
  "moral_load": "neutral",
  "dependency": "useful",
  "risk_exposure": "benign",
}
```

**Narrative Handles**

- “An apprentice fishing lure tuner”
- “Works mornings by ear, afternoons by water”
- “Paid mostly in small coin and opinions”

---

## Corpse Collector

**Axis Bundle**

```
{
  "legitimacy": "tolerated",
  "visibility": "routine",
  "moral_load": "burdened",
  "dependency": "necessary",
  "risk_exposure": "eroding",
}
```

**Narrative Handles**

- “Licensed for after-hours recovery”
- “Knows which doors are never opened”
- “Doesn’t eat near work”

---

## Graveward Bell Ringer

(One who signals deaths, funerals, disturbances)

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "conspicuous",
  "moral_load": "burdened",
  "dependency": "necessary",
  "risk_exposure": "straining",
}
```

**Narrative Handles**

- “Trusted with the long tolls”
- “Learnt the difference between summons and warning”
- “Sleeps lightly”

---

## Mushroom Taxonomist

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "discreet",
  "moral_load": "neutral",
  "dependency": "useful",
  "risk_exposure": "straining",
}
```

**Narrative Handles**

- “Keeps careful notes, eats cautiously”
- “Knows which spores forgive mistakes”
- “Often consulted, rarely thanked”

---

## Soul Ledger Clerk

(Notice: _not_ “Soul Trader”)

**Axis Bundle**

```
{
  "legitimacy": "questioned",
  "visibility": "discreet",
  "moral_load": "heavy",
  "dependency": "unavoidable",
  "risk_exposure": "corrosive",
}
```

**Narrative Handles**

- “Keeps books that never balance”
- “Works under private remit”
- “Ink stains never fully wash out”

---

## Boundary Marker

(One who maintains wards, borders, signs)

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "routine",
  "moral_load": "conflicted",
  "dependency": "necessary",
  "risk_exposure": "hazardous",
}
```

**Narrative Handles**

- “Knows where paths _used_ to be”
- “Fixes signs no one reads”
- “Often blamed”

---

## Whisper-Net Maintainer

(Rumours, messages, informal comms)

**Axis Bundle**

```
{
  "legitimacy": "tolerated",
  "visibility": "hidden",
  "moral_load": "conflicted",
  "dependency": "necessary",
  "risk_exposure": "eroding",
}
```

**Narrative Handles**

- “Keeps the messages moving”
- “Never quotes sources”
- “Rarely surprised”

---

## Relic Dust Cleaner

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "routine",
  "moral_load": "burdened",
  "dependency": "useful",
  "risk_exposure": "hazardous",
}
```

**Narrative Handles**

- “Assigned to low shelves only”
- “Knows which cloths not to reuse”
- “Has lost gloves before”

---

## Apprentice Rune-Filer

**Axis Bundle**

```
{
  "legitimacy": "sanctioned",
  "visibility": "routine",
  "moral_load": "neutral",
  "dependency": "useful",
  "risk_exposure": "straining",
}
```

**Narrative Handles**

- “Still learning the safe angles”
- “Files until symbols behave”
- “Mistakes hum for days”

---

## Unofficial Problem Resolver

(This one’s very you.)

**Axis Bundle**

```
{
  "legitimacy": "questioned",
  "visibility": "discreet",
  "moral_load": "conflicted",
  "dependency": "unavoidable",
  "risk_exposure": "hazardous",
}
```

**Narrative Handles**

- “Works without appointment”
- “Paid after results”
- “Never advertised”

---

# Why This Works (quietly)

- The **axis template is stable**
- Archetypes differ by _pressure pattern_, not lore
- Narrative can be explicit without poisoning renderers
- You can add 50 more occupations without changing the system

Most importantly:

> The job does not define the goblin.

> The pressures of the job do.

---

## Example Prompt Template

```
{STYLE_PREFIX}

illustration of a pale blue-green goblin,

{condition_axis},{facial_axis},

whose work operates under the following conditions:

{occupation_axis}

They are dressed in clothing appropriate to their work and current standing,
showing signs of routine use rather than display. Their posture and expression
reflect familiarity with the demands placed upon them, without overt dramatization.

The environment suggests a place where this kind of work is expected,
but not celebrated.

{STYLE_SUFFIX}
```
