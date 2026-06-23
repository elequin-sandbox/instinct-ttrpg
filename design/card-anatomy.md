# Card Anatomy & Visual System

> **Purpose:** The single source of truth for what a card looks like — type hierarchy, colors,
> ornaments, per-type body anatomy, and the **keyword formatting gospel** (`core-rules.md` points
> here for it). Design/tokens live here; the copy-paste rendering **code** that implements them lives
> in the `at-card-renderer` skill.
> **Status:** current. **Last updated:** June 2026.
>
> **Sibling docs:** rules/keyword meanings → `design/core-rules.md` · wording & forbidden terms →
> `design/writing-conventions.md` · classes → `design/classes.md` · inventory → `card-inventory.md`.

**Legend:** 🔒 locked · ⚠️ in flux.

> ⚠️ **Renderer reconciliation pending:** the live `at-card-renderer` TAG_MAP predates the rules in
> this file — it still renders conditions as filled pills and contains the retired `Bolstered`. The
> gospel below is canonical; the renderer code will be updated to match in a dedicated pass (tracked).

---

## §1 — Type hierarchy

```
Boon (umbrella — positive)
  ├── Background   ✦✦✦   Ocean blue    #0f2d45
  ├── Bond         ◦◦◦   Forest green  #0f2b15
  └── Ancestry     ◆◆◆   Amber-brown   #2a1a08

Bane (umbrella — negative)
  └── Flaw         ✖✖✖   Crimson       #3d0a0a  🔒

Instinct (independent)  ◇◇◇   Slate indigo  #1e2540
   (formerly "Trait" — renamed everywhere June 2026)

Ability (class deck)
  ├── Act
  ├── React
  └── Core
```

**Pip system:** ★ warm gold = Boon-family **and** Instinct (all positive/neutral cards) · ✕ muted red
= Bane-family cards.

**Trigger / lock icon:** ⚡ on all Boon-family and Instinct cards (freely triggered) · 🔒 on all
Bane-family cards (locked — punishing to hold, hard to remove, does **not** clear at scene end;
replaces ⚡). 🔒 never appears on Boon/Instinct cards.

---

## §2 — Card type color spec

| Type | Header bg | Badge | Name | Ornament |
|---|---|---|---|---|
| Instinct | `#1e2540` | `#6a80a8` | `#d4e0f0` | `◇ ◇ ◇` |
| Background | `#0f2d45` | `#5080a0` | `#c4d8e8` | `✦ ✦ ✦` |
| Bond | `#0f2b15` | `#7a9070` | `#b8d0b0` | `◦ ◦ ◦` |
| Flaw | `#3d0a0a` | `#a85050` | `#f0c0b8` | `✖ ✖ ✖` |
| Ancestry | `#2a1a08` | `#9a7a40` | `#d8c080` | `◆ ◆ ◆` |

**Shared shell (all types):** body `#f7f0e0` parchment · border `1.5px solid #c8a96e` gold · footer
`#ede0c4` with the same gold border · shadow hard offset `5px 5px 0 #1a1a1a` (woodblock — never soft
blur) · fonts **Cinzel** (headers/labels) + **IM Fell English** (body).

**Class ability cards** use a class-specific header color (see `at-card-renderer` `TYPE_COLORS`). The
color in the header is for class ability cards **only** — Boons, Bonds, Flaws, and Instincts use the
ink/parchment/gold palette above.

---

## §3 — Header layout

```
┌──────────────────────────────────────┐
│  [BADGE left]               [⚡ or 🔒] │  ← top row
│              CARD NAME               │  ← large, centered, dominant element
│            ◇ ◇ ◇  (ornament)        │  ← centered, ~65% opacity
└──────────────────────────────────────┘
```

The card name is the dominant visual element. The ornament row sits below it. (Flaw uses a
type-specific top row: **Flaw** subtype label left, **Bane 🔒** badge right.)

---

## §4 — The keyword formatting gospel 🔒

Three keyword vocabularies, three visual weights. This is the canon that must look **identical in
every context** — cards, the player primer, and all reference materials. (Mechanical *meanings* are in
`core-rules.md §11`; this file owns the *look*.)

### Tier 1 — Impact Keywords → filled color pills (loudest)

Every word that carries a real gameplay effect. Rendered as a filled inline pill (`.tp`: padded,
3px radius, 700 weight) in its canonical color:

| Impact Keyword | Pill bg | Pill text |
|---|---|---|
| **Boost** | `#0F766E` (teal) | `#CCFBF1` |
| **Resolve** | `#166534` (green) | `#F0FDF4` |
| **Hit Dice** | `#6B21A8` (purple) | `#EDE9FE` |
| **Threat** | `#991B1B` (deep red) | `#FEF2F2` |
| **Crit** *(player-facing: Flourish)* | `#B8860B` (gold) | `#FFFDE7` |
| **Toll** | `#B45309` (bronze) | `#FFFBEB` |
| **Miss** | `#7F1D1D` (dark red) | `#FEF2F2` |
| **Aid** | `#2563EB` (steel blue) | `#EFF6FF` |
| **Mill** | `#0C4A6E` (deep sky) | `#BAE6FD` |

*(Pill text colors are the light on-color values; tune for contrast if a color changes.)*

**Declared Actions** — a related mechanical set rendered **Bold + Capitalized** (not pills):
**Action · Reaction · Draw · Discard · Shuffle · Cleanse · Luck Check · Scene**.

**CRPG action verbs** (Move, Strike, Speak, Sense, Know, Focus, Enter, Exit, Read, Summon, Lift,
Restrain) are the effect-syntax layer — their own established set, rendered as **steel-blue pills**
(`#1D4ED8` / `#EFF6FF`, locked v0.3). Catalogued in `at-card-renderer`.

### Tier 2 — Index Keywords → outlined color chips (medium)

Words that **classify a card for sorting/filtering** with no gameplay effect: card types (Act, React,
Core, Instinct, Background, Bond, Flaw, Ancestry, Item) and class names. Rendered as an **outlined
chip** — transparent fill, 1.5px border + text in the associated type/class color:

```html
<span class="ix" style="background:transparent;border:1.5px solid VAR;color:VAR;
  border-radius:3px;padding:0 5px;font-weight:700;box-sizing:border-box">Item</span>
```

Use the type's header color (§2) or the class color as `VAR`. More present than plain text, quieter
than a filled Impact pill.

### Tier 3 — Narrative vocabulary → plain bold (quietest)

Descriptive conditions with **no enforced mechanics** (GM adjudicates): **Exposed · Rattled · Rooted ·
Hidden · Marked · Sundered · Break.** Rendered as plain **bold title case** — never a pill, never a
chip, no color. *(Bolstered retired → Boost; any old "mechanical" reading of these is gone.)*

---

## §5 — Body anatomy per type

**Instinct** *(the card name IS the word — e.g. Bold, Perceptive — shown very large)*
- Universal flavor (italic): *"True to their nature, your character is moved by this quality in this scene."*
- Thin rule (0.35 opacity)
- Universal effect: *"When you perform any action, reveal this card and explain how your character is driven by this quality. Gain* `[Boost 2]`*."*
- **ORIGIN** label → word-specific stem (1st person, past tense) → 3 writing lines
- Footer: `any · instinct` · ★ pip

**Background**
- Trigger (italic): the conditional situation that activates the card (no separate flavor line)
- Body — one of three variants: *Choose-one* (3 options in CRPG verb format) · *Luck-check*
  (narration + `[Luck Check]` + GM adjudicates) · *Passive-question* (3 GM-answerable questions +
  "The GM answers honestly.")
- **ORIGIN** label → past-tense stem → 4 writing lines · Footer: `any · background` · ★ pip

**Ancestry**
- Flavor (italic, 2nd person present): 1 sentence thematic core
- Trigger (italic) + Body: same three variants as Background
- **ORIGIN** → stem → 3 writing lines · Footer: `any · ancestry` · ★ pip
- *(Dragonborn special two-blank stem: "My blood runs ___ — I claimed it when ___")*

**Bond**
- Flavor (italic, 2nd person present): 1 sentence
- Trigger: *"Find [someone/something]. [Action]. If the moment happens, you both gain* `[Boost 1]`*."*
- **ORIGIN** → stem → 3 writing lines · Footer: `any · bond` · ★ pip

**Flaw**
- Flavor (italic, 2nd person present): the core truth of the flaw
- Stem fill-in (dotted-underline blank, 1st person, filled at creation): Format A `___ sets me off.`
  / Format B `I won't back down when ___.`
- Thin rule → Universal trigger: *"Find something in this scene that fits. Name it aloud, then choose:"*
- Two choices: **Dramatic path** (narrate reaction + GM makes one free move) · **Suppression path**
  (ongoing cost/disadvantage while held)
- Footer: `any · flaw` · ✕ pip · *(no writing box — the stem fill-in is the written record)*

**Ability (Act / React / Core)** — class-deck cards. Header = class color + name + type badge; body =
labeled zones; cost pip in footer. Full design system in `at-card-renderer` + `at-design-session`.

---

## §6 — Layout constants

Card width `195px` · grid `repeat(auto-fill, minmax(195px, 1fr))` · print `repeat(3, 63mm)` +
`@page { size: A4 }` · pip cost circle in footer. Implementation: `at-card-renderer` (CSS, `parse()`,
`resolveBase()`, `renderCard()`).

---

*Rules/keyword meanings → `design/core-rules.md` · wording & forbidden terms →
`design/writing-conventions.md` · classes → `design/classes.md`.*
