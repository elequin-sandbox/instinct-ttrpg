# Writing Conventions

> **Purpose:** How to put words on a card — formatting tiers, voice, section anatomy, the forbidden-
> terms list, and the pre-finalize audit. Run the **Term Audit** (bottom) before any card is approved
> or pushed to Baserow.
> **Status:** current, Playtest 4 prep. **Last updated:** July 1 2026.
>
> **Sibling docs:** keyword *meanings* → `design/core-rules.md` · pill/chip *colors* →
> `design/card-anatomy.md` · classes → `design/classes.md`. Rendering **code** + Baserow viewer CSS
> classes → the `at-card-renderer` and `at-baserow-push` skills.

**Legend:** 🔒 locked · ⚠️ in flux.

---

## §1 — The three formatting tiers (how to write each)

Mirrors the keyword taxonomy in `core-rules.md §11`; exact colors live in `card-anatomy.md §4`.

1. **Impact Keywords → pills.** Write as `[Term]` or `[Term N]` (e.g. `[Boost 2]`, `[Resolve]`,
   `[Threat]`, `[Crit]`, `[Toll]`, `[Hit Dice]`, `[Aid]`, `[Miss]`, `[Mill]`). Never write an Impact
   Keyword as plain text. Always include the number when one applies: `[Boost 1]`, not "Boost."
2. **Index Keywords → outlined chips.** Card types and class names used to *classify* a card
   (Act, React, Core, Instinct, Background, Bond, Flaw, Ancestry, Item; class names). Rendered as
   outlined chips in their type/class color — see `card-anatomy.md`.
3. **Narrative vocabulary → plain bold.** Descriptive terms with no built-in mechanics
   (**Exposed, Rattled, Rooted, Hidden, Marked, Sundered, Break**). Bold title case, no pill, no color.
   **Always gloss on the card** — a few words of scene-specific meaning (em dash or choose-one fork).
   Split combined crit spends into separate Crit lines (one keyword + gloss per line). Never “immune to
   **Rattled**,” “remove condition,” or “this condition persists.” **Exception (locked Playtest 4/P2):**
   when one of these words is printed as a card's **Flourish** option (a Crit line), it *does* carry a
   printed number and a coloring — see the Crit/Flourish line format above and `core-rules.md` §5. The
   word alone, anywhere else, stays exactly as described in this bullet.

**Declared Actions → Bold + Capitalized** (not pills): **Action · Reaction · Draw · Discard ·
Shuffle · Cleanse · Snap Check · Scene** (plus **Combat · Rest** as scene/time terms).

**CRPG action verbs** (Move, Strike, Speak, Sense, Know, Focus, Enter, Exit, Read, Summon, Lift,
Restrain) — effect-syntax verbs, rendered as steel-blue pills. Used for choose-one option lines.

**Choose-one list syntax — bold imperative verb leads every option (PbtA parallel syntax).** 🔒
Each bullet in a choose-one list opens with a bold imperative verb or verb phrase, followed by the
elaboration. All options in a list must follow the same pattern.
- ✓ **Share** a memory between you that feels like this moment.
- ✓ **Challenge them** — push them to grow or change in a way this scene requires.
- ✗ ~~A memory you share that feels like this moment.~~ (no leading verb)
- ✗ ~~You can ask them a question.~~ (not imperative, not parallel)
When workshopping choose-one option language, pitch **6–8 distinct phrasings** per option so
Annie can select. Don't settle on one phrasing and ask "is this good?" — show the range.

**Rule of thumb for a new term:** can it carry a number / change the dice? → Impact pill. Does it
sort/filter a card? → Index chip. Is it just a named scene/action? → Bold+Cap. A fictional descriptor?
→ plain bold. Otherwise → lowercase prose. **Do not invent new pill terms without explicit approval.**

---

## §2 — Voice & writing principles (priority order)

1. **Brevity.** If a word can be cut without losing meaning, cut it. Cards are read mid-play.
2. **Syntactic parallelism.** Same construction across cards reads the same way. If one card says
   "Gain `[Boost 2]` for the Action," another must not say "earn a `[Boost 2]` bonus."
3. **User-centric.** Write for the player holding the card. "You" = direct/present. "Your character"
   = deliberate narrative distance — use intentionally, not by default.
4. **No ambiguity.** If a player could read it two ways, rewrite it. The GM should never have to
   settle a wording dispute.
5. **No negation-passive.** Never "you cannot," "you are immune," "you are not." Reframe as an active
   state or advantage.
6. **"This scene," not "the scene ahead."** The hand is who the character is *right now*.
7. **No designer-speak.** Never "the fiction advances," "narratively," "mechanically speaking,"
   "spotlight" on player-facing text.

---

## §3 — Section anatomy & names

Use these exact section names in design work.

**Ability cards (Act / React / Core):** **Flavor Text** (2nd person, present, 1 sentence — only when
the card earns framing) · **Trigger** (italic conditional, soft fiction-first gate, should fit most
scenes) · **Effect** (main outcome; CRPG verb format for choose-one; hint direction, never prescribe)
· **Crit** (only when the fiction earns it; 3–6 words/option, 2–3 options max) · **Discard** (one
short clause).

🔒 **Crit/Flourish line format (locked Playtest 4 — P2):** lead with the **bold Flourish keyword**
(often a Tier 3 narrative term — Exposed, Rattled, etc.), then the **printed numeric effect** — e.g.
**Exposed 2** — remove 2 dice from the objective pool. Assign one of the three colorings (red
offensive / blue defensive / green resolve — `card-anatomy.md`). One keyword + effect per line; split
combined spends into separate lines (§1 below). No GM-adjudicated magnitude language ("some," "a
lot") — the number on the card is the whole effect. Full mechanic → `core-rules.md` §5.

🔒 **Flourish v6 content (July 2026 prototype — Nathan):** supersedes P2 *wording on new Ability
cards* — attempt paragraph only (no Effect label, no on-success clause); Flourish box uses **global
keywords** Advance / Defend / Restore + shape icons, not card-specific mechanical tags. See
`design/spark-flourish-v6.md`. P2 colored-keyword lines remain on cards not yet migrated.

**Ability attempt setup (v6):** *Perform a **[Skill]** check to [try X]* — describes the **attempt**,
never a guaranteed outcome. In combat the attempt feeds the normal Offense/Defense roll; out of
combat the GM frames a Contest. No stacked forks in the base paragraph.

**React + Snap Check cards** (high-variance Reactions — see `core-rules.md` §10): **Flavor** ·
**Setup** (everything *before* the Snap Check bands — describes the **attempt**, never a guaranteed
outcome; ends with *make a* **Snap Check***) · **Snap Check** section (card-printed bands or face
table — one of three formats, no global scheme):
1. **Threshold** — success/fail breakpoints only (e.g. 1–5 / 6, or 1–3 / 4–6).
2. **Step ladder** — each band names its own mixed or full result (e.g. 1–2 fail · 3–4 partial · 5–6 full).
3. **Face oracle** — six distinct outcomes keyed to die face (wild-surge table; read the face rolled).
No Crit block unless the card also uses pool checks. Snap Check cards may omit Crit spend — the bands
*are* the payoff. A natural 1 is always a **[Miss]**; a natural 6 always **explodes** per §5.

**Character-creation cards:** **Flavor** (Background, Bond, Ancestry) · **Preamble + choose-one fork**
(Instinct — dual-path; see `card-anatomy.md` §5) · **React callout + options + Snap bands + Mill**
(Background — all React) · **Act/React callout + options + Snap bands** (Ancestry — no Mill) ·
**Find / Act / Then** (Bond) ·
~~**Origin Stem**~~ *(retired June 2026 — write-in lives on Character / Class / Ancestry sheet cards)* ·
~~**Writing Lines**~~ *(retired with Origin stems)* · ~~**Flaw fill-in stem**~~ *(retired June 2026)* ·
~~**Dismiss**~~ *(retired with Flaw type)*

**Item cards:** Items remain a classless card type, but ⚠️ the item system is being **stripped back to
its simplest form for the next playtest** — the old Item Check / placed-dice / Save anatomy is retired
(§5). Keep items to Flavor + Effect (+ optional Crit) until the simpler version is designed.

---

## §4 — Special word rules

| Term | Rule |
|---|---|
| **GM** | Always abbreviated — never "Game Master." |
| beat | Lowercase — informal time language, not a game term. |
| Pact | A card name, not a game term — no special formatting. |
| Distances | Write in **feet**, never named ranges ("Near"/"Close"). |
| Card-specific nouns | Bold+Cap on that card only (e.g. "Nature" on a Druid card); don't add to the global glossary unless it goes cross-card. |
| Class economy terms | **Rally · Notoriety** *(Rogue)* · **Performance** *(Bard)* · **Debt** *(Warlock)* — Bold+Cap; more added as classes are designed (see `classes.md`). |

---

## §5 — Retired / forbidden terms — DO NOT USE 🔒

The single catalogue of dead terms and their replacements. The *live* mechanic that replaced each is
described in `core-rules.md`.

| Don't write | Use instead / status |
|---|---|
| ~~Guard~~ | **[Resolve]** only — Guard does not exist; never a pill, keyword, or pool name on cards |
| ~~Bolstered~~ | **[Boost]** (Boost absorbed it) |
| ~~Strong Roll~~ | **[Crit]** |
| ~~Rattled~~ | plain-bold narrative only — carries no mechanic |
| ~~Encounter~~ | **Contest** (umbrella) / **Deadly Contest** / **Social Contest** |
| ~~Combat encounter / Non-combat encounter~~ | **Deadly Contest** / **Social Contest** |
| ~~Failure~~ (as a trigger) | **Miss** (a natural 1 only; a partial result is not a Miss) |
| ~~Self-Aid~~ | Aid must come from an ally; self-assist does not exist |
| ~~DC / target number / DC ladder~~ | difficulty is the GM's physical opposing dice pool |
| ~~d8 / d10 / die-size upgrades~~ | the whole game is **d6 only** |
| ~~Item Check~~ | **retired** — item system stripped back for next playtest |
| ~~Placed dice / Save throws~~ | **retired** — the place-dice-and-Save loop is cut |
| ~~[Rooted] / [Exposed] / [Hidden] as pills~~ | now **plain-bold narrative** terms, no mechanics |
| ~~Disguised~~ | **retired** (was a placed-dice buff) |
| ~~Buff/debuff pill distinction~~ | **retired** with the placed-dice system |
| ~~"while held, [negative effect]"~~ on Flaws | the hand-slot cost IS the consequence |
| ~~"the fiction advances"~~ | designer-speak — never on player-facing text |
| ~~Luck Check~~ | **retired** — full checks use §5 pools; Reactions use **Snap Check** (1d6 subset) |

---

## §6 — Term Audit Checklist

Run on every card before approval or Baserow push. Fix violations immediately.

- [ ] Impact Keywords written as pills (`[Boost 2]`), never plain text
- [ ] Index keywords (types/classes) styled as outlined chips, not loud pills
- [ ] Narrative conditions (Exposed, Rooted, Hidden, etc.) are **plain bold** — NOT pills
- [ ] Declared actions capitalized: action → **Action**, scene → **Scene**, combat → **Combat**, rest → **Rest**
- [ ] No retired terms (§5): no Guard, Bolstered, Strong Roll, Item Check, placed dice, Disguised, die upgrades
- [ ] "GM" not "Game Master"; "beat" lowercase
- [ ] Distances in feet, not Near/Close
- [ ] Syntactic parallelism — compare phrasing to similar cards in the same deck
- [ ] Brevity pass — any words to cut?
- [ ] No negation-passive language; no designer-speak
- [ ] "this scene" not "the scene ahead"
- [ ] Section names match §3

---

## §7 — Baserow viewer rendering note

When writing card HTML for the Baserow viewer, use the **viewer app CSS classes** (`.elbl`, `.csec`,
`.clbl`, `.crow`, `.ci`) — **not** the renderer-preview classes (`.slbl`, `.srlbl`, `.sropt`), which
render grey/incorrectly in the viewer. Full CSS and the `parse()`/`renderCard()` stack live in the
`at-card-renderer` skill; the push workflow lives in `at-baserow-push`.

---

*Keyword meanings → `core-rules.md` · colors → `card-anatomy.md` · classes → `classes.md`.*
