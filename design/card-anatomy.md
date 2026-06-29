# Card Anatomy & Visual System

> **Purpose:** The single source of truth for what a card looks like — type hierarchy, colors,
> ornaments, per-type body anatomy, and the **keyword formatting gospel** (`core-rules.md` points
> here for it). Design/tokens live here; the copy-paste rendering **code** that implements them lives
> in the `at-card-renderer` skill.
> **Status:** current. **Last updated:** June 29 2026.
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
  └── Flaw         ✖✖✖   Crimson       #3d0a0a  *(retired June 2026 — merged into Instinct)*

Instinct (independent)  ◇◇◇   Slate indigo  #1e2540
   Dual-purpose: positive path [Boost 2] OR negative path Draw 2 (formerly separate Flaw cards)

Connection (session-start template)  *(no ornament — name blank)*   Deep rose  #2d1020
   One per player; filled in at session start with character name; shuffled into other players' decks.

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
| Connection | `#2d1020` | `#905070` | `#f0d0e0` | *(no ornament — name blank + italic instruction)* |

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
| **Hit Dice** | `#991B1B` (deep red) | `#FEF2F2` |
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

**Instinct** *(the card name IS the word — e.g. Bold, Perceptive — shown very large)* 🔒 *redesigned June 2026*
- **Preamble** (italic): *"This instinct is driving your behavior this scene."* When you **Reveal** this card, perform an **Action** in a **[Word]** manner. **Choose one:**
- **Fork stack** (fills remaining card height, split **50/50** vertically) — **visual: V1 Band Wash** (locked):
  - **Strength** (top half, centered subtitle chip): Describe how it benefits your party. If the GM agrees, gain `[Boost 2]` on the **Action**.
  - **Divider**: gold rail + circular **OR** medallion
  - **Flaw** (bottom half, centered subtitle chip): Describe how it hinders you or your party. If the GM agrees, **Draw 2**.
- No Origin stem, no Crit, no post-path text. Playing the card spends it (implicit).
- Header: `Instinct` badge · `Act` cost · ★ pip
- Design proofs: [`instinct-dual-pilot-proof.html`](../instinct-dual-pilot-proof.html) (Bold × 4 variants)

**Flaw** *(retired June 2026 — merged into Instinct; legacy Baserow rows only)*
- Former anatomy: flavor · stem fill-in · Dramatic/Suppression choose-one · Dismiss/Cleanse · ✕ pip

**Background**
- Flavor (italic, 2nd person present): 1 sentence thematic core
- Trigger (italic): the conditional situation that activates the card
- Body — one of three variants: *Choose-one* (3 options in CRPG verb format) · *Luck-check*
  · *Passive-question* (3 GM-answerable questions + "The GM answers honestly.")
- No Origin stem, no writing lines (backstory write-in lives on Character sheet cards) · ★ pip

**Ancestry** *(Snap Check — locked June 2026; proof: `ancestry-snap-proof.html`)*
- Flavor (italic, 2nd person present): 1 sentence thematic core
- **Once per Scene** — muted label (`anc-freq`) above the callout; not repeated inside it
- Trigger callout (`anc-callout`) — **not italic**; left-rail highlight the player scans for:
  - **Act:** *You may take an **Action** to [ancestry thing] by making a **Snap Check**:*
  - **React:** *When [condition], **React** with a **Snap Check**:* (violet rail)
- **Three options** — self / ally / scene vectors; any two should combine on **9+**
- **Three options** — CRPG verb stack (`bf-choice` rows), same list for all bands
- **Snap bands** — one compact footer line: **1–3** Fails · **4–8** Choose 1 · **9+** Choose 2
- Header: `Ancestry` chip + **`Act`** or **`React`** (defensive/underdog cards may be React)
- No Origin stem (heritage write-in lives on Ancestry sheet card) · ★ pip

**Bond**
- Flavor (italic, 2nd person present): 1 sentence
- **Find / Act / Then** zones: *Find* (who or what to look for) · *Act* (what to do in conversation)
  · *Then* (if it lands, you both gain `[Boost 1]`)
- No Bond stem (relationship write-in lives on Character sheet card) · ★ pip

**Connection** *(session-start template — one per player, filled at table)*
- Header top row: `CONNECTION` badge (left) · `Act` badge (right) — no ⚡, no 🔒
- Name area: large fill-in blank with italic placeholder *"(name)"* below — no ornament row
- Preamble (italic): *"Find a moment in this scene to connect with this character. Choose one:"*
- Three bold-imperative choose-one options (PbtA parallel syntax): **Share** · **Ask** · **Challenge them —**
- Reward line: *"Then, each player chooses: gain* `[Boost 1]` *, reclaim a* `[Hit Die]` *, or* **Draw 1***."*
- OR divider: horizontal gold rule with **OR** centered in it
- Aid clause (italic): *"When discarding this card to* `[Aid]` *this character, grant* `[Boost 2]`*."*
- Footer: `any · connection` · ★ pip · no flavor text · no origin stem
- Deck placement: shuffled into class deck like Bonds/Flaws

**Ability (Act / React / Core)** — class-deck cards. Header = class color + name + type badge; body =
labeled zones; cost pip in footer. Full design system in `at-card-renderer` + `at-design-session`.

**React + Snap Check** *(prototype anatomy — see `snap-check-react-proof.html`)*:
- **Flavor** · **Effect** setup (attempt language only — what you *try* to do; ends with **Snap Check**)
- **Snap Check** label + outcome block — violet band pills (`1–2`, `1–5`, etc.) for threshold/step
  formats, or six face-keyed rows for face-oracle format. Mirrors Crit-block layout but band-colored,
  not gold Crit-count pills. Cards do not re-explain Snap Check procedure.

---

## §6 — Layout constants

**Card Studio / print (Core & Ability):** **2.5″ × 3.5″** fixed (`width: 2.5in; height: 3.5in` in
`index.html` `.scope-core .card`). Proof HTML must use **fixed height**, not `min-height`, so layout
matches print. Body regions reserve **~26–32px bottom padding** for the floating `.idtag`.

Legacy renderer grid: card width `195px` · grid `repeat(auto-fill, minmax(195px, 1fr))` · print
`repeat(3, 63mm)` + `@page { size: A4 }`. Implementation: `at-card-renderer` (CSS, `parse()`,
`resolveBase()`, `renderCard()`).

**Dense Core layouts** (Oath vow grid, Patron marks): see `design/paladin-oath-charge.md` and
`.cursor/rules/instinct-core-card-design.mdc`.

---

*Rules/keyword meanings → `design/core-rules.md` · wording & forbidden terms →
`design/writing-conventions.md` · classes → `design/classes.md`.*
                     

---

## §7 — Unified header system (LOCKED June 24 2026) 🔒  *(supersedes §3 header row & §6 footer)*

The whole card library was normalized to ONE structure so every card reads as the same game.
**There are no footers.** Everything lives in the header + two floating corner marks.

**Per-card structure**
- **Header bar** (`.hdr`): light wash background tinted with the card's accent color; dark text.
  - **Top-left** (`.cap`): the **card TYPE** — `Ability`, `Core`, `Background`, `Bond`, `Flaw`,
    `Ancestry`, `Instinct`, `Connection`. Outlined capsule, sans-serif, 800 weight.
    On class cards the type is neutral ink; on non-class cards it carries the type's accent color.
  - **Top-right** (`.cap`): the **play COST** — `Act` / `React`. Blank on Core (no cost) except
    dual-purpose cards (e.g. Warlock Patron, flagged manually). Neutral-ink outlined capsule.
  - **Name ribbon** (`.hdr-name`): centered, EB Garamond 700, **banner ribbon** with notched ends
    (clip-path), filled with a light tint of the accent, dark accent text, accent top/bottom borders.
    Connection's ribbon is left blank for writing the character name in (tiny faint placeholder).
  - **Subtitle** (`.hdr-sub`): italic flavor line under the name. **Exception:** Paladin **Oath** Core
    cards omit on-card subtitle — flavor lives in `design/paladin-oath-charge.md` only (print space).
- **Bottom-left** (`.idtag`, floating, no footer): the **CLASS** name (Rogue, Fighter, …) in an
  accent-colored capsule. **Class cards only** — empty on Instinct/Boon-family/Connection.
- **Bottom-right** (`.tier-float`, floating): muted-gray italic **tier** circle (`t1`). **Ability +
  Item cards only**; everything else leaves it blank.
- **Left edge**: 5px accent-color border on the whole card — carries color identity in print.

**Color authority is centralized.** Accent colors live as CSS variables in `.acc-<key>` classes
(`canon_accents.css`, injected into `index.html`). Recolor a class/type in ONE place. Brighter
"accent" hues are used here (e.g. Flaw `#b3261e`) than the deep doctrine band colors in §2, because
the header is now light — §2's deep colors are retired for the header layer.

**Keyword layer (LOCKED June 24 2026)** — pills are now **class-based**, colored from `canon_keywords.css`:
- **Impact keywords** → `<span class="kw kw-ID">` filled pills: Boost, Resolve, Hit Dice/Die (`hd`),
  Threat, Crit, Toll, Miss, Aid, Mill. Crit-count numbers use `kw-crit` (gold).
- **CRPG action verbs** (Move, Strike, Enter, …) → **DEMOTED to plain bold** (no longer pills).
- **Skill / check names** (Athletics, Stealth, Faith, Nature, Spellcast, Item Check, …) → **plain bold**
  ("generic checks").
- **Narrative conditions** (Exposed, Rattled, Rooted, Hidden, Marked, …) → **plain bold**.
- **In-text card-type / class names** → outlined **Index chips** (`<span class="ix ix-KEY">`).
- **Term renames applied:** Bolstered→Boost, Trait→Instinct.

Implementation (CSS + normalizer) lives in the project workspace (`canon_*.css`, `normalize.py`) and is
injected into `index.html`. Status: current.

