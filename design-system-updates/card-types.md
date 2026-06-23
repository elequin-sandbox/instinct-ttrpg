# Card Types — Visual System & Anatomy

*Read this file before any card design, rendering, or print work.*

---

## TYPE HIERARCHY

```
Boon (umbrella — positive)
  ├── Background   ✦✦✦   Ocean blue    #0f2d45
  ├── Bond         ◦◦◦   Forest green  #0f2b15
  └── Ancestry     ◆◆◆   Amber-brown   #2a1a08

Bane (umbrella — negative)
  ├── Flaw         ✖✖✖   Crimson       #3d0a0a  🔒
  └── Status       (future)

Instinct (independent)    ◇◇◇   Slate indigo  #1e2540

Ability (class deck)
  ├── Act
  ├── React
  └── Core
```

**Pip system:**
- ★ warm gold = Boon-family AND Instinct (all positive/neutral cards)
- ✕ muted red = Bane-family cards

**Lock icon 🔒:**
- Appears on Bane-family cards ONLY (Flaw, Status)
- Signals: punishing to hold, hard to remove, does NOT clear at scene end
- Never appears on Boon-family or Instinct cards

---

## HEADER LAYOUT (all character creation cards)

```
┌──────────────────────────────────────┐
│  [BADGE left]               [⚡or🔒] │  ← top row
│                                      │
│              CARD NAME               │  ← large, centered
│            ◇ ◇ ◇  (ornament)        │  ← centered, 65% opacity
└──────────────────────────────────────┘
```

- **⚡** on all Boon-family and Instinct cards — freely triggered
- **🔒** on all Bane-family cards — locked, replaces ⚡
- Card name is the dominant visual element — substantially larger than old design
- Ornament row sits below the name

---

## COLOR SPECIFICATIONS

| Type | Header bg | Badge color | Name color | Ornament |
|---|---|---|---|---|
| Instinct | `#1e2540` | `#6a80a8` | `#d4e0f0` | `◇ ◇ ◇` |
| Background | `#0f2d45` | `#5080a0` | `#c4d8e8` | `✦ ✦ ✦` |
| Bond | `#0f2b15` | `#7a9070` | `#b8d0b0` | `◦ ◦ ◦` |
| Flaw | `#3d0a0a` | `#a85050` | `#f0c0b8` | `✖ ✖ ✖` |
| Ancestry | `#2a1a08` | `#9a7a40` | `#d8c080` | `◆ ◆ ◆` |

**Shared shell (all card types):**
- Body: `#f7f0e0` parchment
- Border: `1.5px solid #c8a96e` gold
- Footer: `#ede0c4` with same gold border
- Shadow: 5px offset dark (`#0e0b06`)
- Fonts: Cinzel (headers, labels) + IM Fell English (body text)

**Inline pill colors:**
- Boost N: background `#0F766E`, text `#CCFBF1` (teal)
- Luck Check: background `#B8860B`, text `#FFFDE7` (amber)
- Hit Die: background `#6B21A8`, text `#EDE9FE` (purple)

---

## CARD BODY ANATOMY — PER TYPE

### Instinct
- **Universal flavor** (italic): *"True to their nature, your character is moved by this quality in this scene."*
- Thin rule (0.35 opacity)
- **Universal effect**: *"When you act, describe how this quality is driving you right now. Gain* `[Boost 2]`*."*
- Full rule
- **ORIGIN** label → word-specific stem (1st person, past tense) → 3 writing lines
- Footer: `any · instinct` · ★ pip

**The card name IS the word** (Bold, Perceptive, etc.) — displayed very large in header.

---

### Background
- **Trigger** (italic): conditional clause — the situation that activates this card
- Thin rule
- **Body (one of three variants):**
  - *Choose-one:* 3 options in CRPG verb format
  - *Luck-check:* narration + `[Luck Check]` pill + GM adjudicates
  - *Passive-question:* 3 GM-answerable questions + "The GM answers honestly."
- Full rule
- **ORIGIN** label → past-tense stem → 4 writing lines
- Footer: `any · background` · ★ pip

No separate flavor line — the trigger carries the framing.

---

### Ancestry
- **Flavor** (italic, 2nd person, present tense): 1 sentence capturing thematic core
- Thin rule
- **Trigger** (italic): conditional clause
- **Body:** same three variants as Background
- Full rule
- **ORIGIN** label → stem → 3 writing lines (flavor takes one line vs Background's 4)
- Footer: `any · ancestry` · ★ pip

Dragonborn has a special two-blank stem: *"My blood runs ___ — I claimed it when ___"*

---

### Bond
- **Flavor** (italic, 2nd person, present tense): 1 sentence
- Thin rule
- **Trigger**: *"Find [someone/something]. [Action]. If the moment happens, you both gain* `[Boost 1]`*."*
- Full rule
- **ORIGIN** label → stem → 3 writing lines
- Footer: `any · bond` · ★ pip

---

### Flaw
- **Flavor** (italic, 2nd person, present tense): 1 sentence — the core truth of the flaw
- **Stem fill-in**: dotted-underline blank(s), 1st person — filled at character creation
  - Format A: `___ sets me off.` (blank before post)
  - Format B: `I won't back down when ___.` (blank after pre)
- Thin rule
- **Universal trigger**: *"Find something in this scene that fits. Name it aloud, then choose:"*
- 2 choices:
  - **Dramatic path** — narrate reaction + GM makes one free move
  - **Suppression path** — ongoing cost/disadvantage while card is held
- Full rule
- **DISMISS** label (small Cinzel caps, `#8a3030`) → dismiss condition (italic)
- Footer: `any · flaw` · ✕ pip

No writing box — the stem fill-in IS the player's written record.

---

### Ability Cards (Act / React / Core)
These live in the class deck alongside character creation cards. Full design system documented in `at-card-renderer` skill and `at-design-session` skill.

Key anatomy:
- Header: class-specific color + card name + type badge
- Body zones: labeled sections (Active, Passive, Resonance, etc.)
- Conditions use canonical names (see `design-principles.md`)
- Cost pip in footer

---

## CHARACTER CREATION DECK MATH

- Target deck: **20 cards**
- **6 Instincts** shuffled in (hypergeometric: median 1 Instinct per 5-card hand, ~13% zero-instinct scenes)
- **1 Background** shuffled in
- **1 Ancestry** shuffled in
- **2 Bonds** shuffled in (approximate — varies by character)
- Remaining: class ability cards (Act, React, Core)
- Flaws: shuffled in as assigned during character creation

Character creation draws:
1. **Draw 5 Instincts** at random from the Instinct tableau
2. **Choose 1 Background** from the 12 available
3. **Choose 1 Ancestry** from the 10 available

---

## Changelog
- [June 2025] — Complete redesign. Boon → Background, Bane → Flaw (sub-types). New types: Trait, Ancestry. Header layout changed to badge-left/icon-right/large-name. Lock icon moved to Bane-family only. ⚡ icon added to all freely-triggered cards.
- [June 2026] — **Trait → Instinct** (card type renamed everywhere). Universal effect text updated to: *"When you act, describe how this quality is driving you right now. Gain [Boost 2]."* CSS class `.bf-trait` → `.bf-instinct` in index.html; JS type key `'Trait'` → `'Instinct'`.
