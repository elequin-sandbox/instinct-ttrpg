# Core Rules — how Instinct RPG plays

> **Purpose:** The single authoritative source for how the game *currently plays* — the truth any
> card design must obey. If a rule here and a card disagree, this file wins (or the card is wrong).
> **Status:** Post-Playtest #1 · authoritative only (no deprecated or future-scoped content).
> **Last updated:** June 2026.
>
> **Sibling docs:** card structure/colors/tags → `design/card-anatomy.md` · wording, forbidden terms &
> the keyword formatting gospel → `design/writing-conventions.md` · per-class detail →
> `design/classes.md` · what exists/pushed → `card-inventory.md`. Deprecated/future ideas are NOT
> here — they live in the `at-design-archive` skill.

**Legend:** 🔒 = locked · ⚠️ = in flux (see *Open questions* at the end before building hard on it).

**One global constant:** 🔒 **the whole game uses d6s only.** No ability or weapon changes die size in
the current design. Wherever "a die" appears, read "a d6."

---

## §1 — Game philosophy

**The deck is who the character is in general. The hand is who they are right now.**

Cards are prompts, not contracts. The player narrates first; the card confirms the *scope* of what
the fiction may achieve; the GM adjudicates what that means in this scene. Cards never fully
prescribe outcomes — the GM and table fill the gap.

- **A Miss is never a stop.** On a Miss (a natural 1), the fiction advances regardless. The GM takes
  the scene somewhere interesting; the player is never punished with nothing.
- **Fiction-first triggering.** Cards trigger when the fiction supports it, not when a mechanical
  condition is met. Triggers are soft gates; a player should read a trigger and immediately know
  whether this scene qualifies.
- **Conditions are narrative vocabulary.** Words like **Exposed**, **Rooted**, **Rattled** give the
  table a shared label for something happening in the fiction — they carry **no enforced mechanics**.
  Their meaning is the GM's call in the moment (see §11).

**North star (Ben, Playtest #1):** *"The core of the game is giving people funny excuses to use their
cards in unexpected ways."* Measure every rules decision against this. If a rule makes unexpected
card use harder, reconsider it.

---

## §2 — The game loop

1. **Narrate** — a player describes what their character does or says.
2. **Roll & Resolve** — if the outcome is uncertain, build a dice pool and roll against the GM's
   opposing pool. The GM adjudicates.
3. **Story moves** — the fiction advances on the result. Miss → GM gains **[Toll]** and the scene
   moves. Hit → narrate success. Crit → spend [Crit] options.

---

## §3 — Scenes

Scenes are the primary unit of play: a clear location, active participants, and a dramatic question.
No formal initiative or turn order.

**Three scene types:** **Combat · Exploration · Social.**

**The 80% goal (not a strict rule):** aim for roughly **4 of every 5 cards in a hand to be relevant
in whatever scene you're in.** This is a design target that keeps hands live across scene types — not
a hard requirement. Cards are valid in any scene whose fiction supports their trigger; they are never
locked to a scene type.

**Scene end:** hands are discarded and redrawn. Anything a card described mid-scene (e.g. someone
being **Exposed**) carries forward only if the GM rules the fiction says so.

---

## §4 — The hand & card draw

**Your deck is your character. Your hand is their Instincts — what's driving them right now.**

You never have your whole character available at once. Each scene, you draw a partial slice of who
they are; your job is to narrate *why* they act the way the hand suggests. That partial control — and
the fun of justifying unexpected cards — is the core of Instinct RPG.

An **Instinct** in hand = that quality is alive in this moment. A **Bond** = that connection is
present. The hand is not a menu you optimize; it's what your character wants to do in this scene.

- **Hand size:** players draw a full hand at the start of each scene. Not fixed — set by the table
  (typically 5). GM sets the scene; players draw.
- **Playing a card:** narrate the fictional action that triggers it, then resolve its effect.
  Playing ≠ rolling — only uncertain actions call for a roll.
- **Discarding:** cards may be discarded without playing; some effects require a discard as a cost.
- **Deck depletion:** when a deck runs out, the discard shuffles back in automatically.
- **Empty hand:** the player falls back to narrative/basic actions (no card effects). GM guidance:
  transition or end scenes once the party's average hand drops to ~2 or fewer. A depleted hand is a
  **pacing signal, not a punishment** — "read the room by reading the hands."

---

## §5 — Making a check

Roll only when the outcome is genuinely uncertain. All checks — combat and non-combat — use one
**dice-pool-vs-dice-pool** model: the player builds and rolls a pool of d6s; the GM assembles an
opposing pool; player dice clear opposing dice one at a time. This is the entire game's core
resolution.

**Build → Roll → Read.**

**Build — base pool by Tier:**

| Tier | Levels | Base dice |
|---|---|---|
| Tier 1 | 1–3 | 2d6 |
| Tier 2 | 4–6 | 3d6 |
| Tier 3 | 7–9 | 4d6 |

- **Boost:** extra dice arrive as **[Boost N]** — N dice added to the pool from card effects and other
  sources. There are many ways to earn Boost; **players generally cannot discard their own cards to
  boost their own rolls** (the old self-discard-to-add-a-die mechanic is retired — **Aid** took its
  place). All bonus dice behave identically regardless of source; they expire at scene end and are
  removed if they show a 1.
- **Aid (ally assist):** an ally may discard a card from their hand, **describe how that card is
  relevant to the active player's check** (Instinct, Ability, or Item), and add 1 die to **another**
  player's pool ([Boost 1]) if the GM agrees. They are **not** playing the discarded card for its
  normal effect — they are narrating the assist. 🔒 **Capped at one assist per check. Self-Aid does not
  exist — Aid must come from an ally.** When a card names this mechanic it's **Stack** or **Rally**
  (see §10 / `classes.md`).

**Roll** all dice simultaneously.

**Read your dice:**
- **Pull the 1s — those are Misses.** A **Miss** is strictly a natural 1. Each Miss gives the GM 1
  **[Toll]** and is removed from the pool (it contributes nothing). A die that partially resolves its
  target is **not** a Miss — it's a partial success.
- **Sixes are Crits.** Each die showing a **6** explodes: roll one bonus die and add it to your total.
  A bonus die that shows a 6 counts toward your Crit options but does not explode again.
- **Count your Crits** — how many dice across the whole pool still show a **6**. That count is how many
  **Flourishes** you may **gain** from the played card.
- **Read vs. the opposing pool** — assign your dice against the GM's dice one at a time. If your die
  shows **equal or higher** than an opposing die, remove both. If yours is **lower**, you may
  **reduce** that opposing die by 1 and remove yours. Clear all opposing dice: success. Some remain:
  partial success (GM adjudicates). No hidden DC; the GM's pool *is* the difficulty.
- **Deadly Contests deal damage by pool clearing** — face values deal damage to enemy Hit Dice
  directly. Misses (1s) still generate [Toll].

**Crit vs. Flourish:** a natural **6** is a **[Crit]** (the die result). **Flourish** = an individual
bonus option listed on an ability card; you **spend** earned Crits to take Flourishes after the roll
resolves. Card sections may label the spend block **Crit** or **Flourish** — same mechanic.

---

## §6 — The opposing dice pool (difficulty)

Difficulty in *all* checks is the **GM's opposing dice pool** — placed physically on the table before
the roll, making difficulty visible and tactile. No DC ladder, no hidden number.

- **Random method:** GM rolls dice appropriate to the danger level; the values become the opposition.
- **Hand-placed method:** GM selects specific values for specific threats — e.g. a named villain as a
  fixed high-value die among generic random d6s — differentiating bosses from mooks without stat
  blocks.

Player dice clear opposing dice one at a time; clear them all and the check succeeds. Clearing some
but not all = **partial success** (GM adjudicates what was/wasn't achieved) — not a Miss. Surplus
dice after clearing: see §8 spillover.

| Difficulty | Suggested opposing pool |
|---|---|
| Easy | 1–2 dice, low values |
| Moderate | 2–3 mixed dice |
| Hard | 3–4 dice, some high |
| Very Hard | 4–5 dice, high values |
| Boss / Climactic | Mixed pool; hand-placed high-value dice for named threats + random dice for generic |

---

## §7 — Toll

**[Toll]** is a GM resource generated by Misses (any natural 1, even on an otherwise-successful
check) — each 1 = 1 Toll added to the GM's pool. The GM spends Toll to escalate scenes, trigger NPC
reactions, activate enemy abilities, and introduce complications. It is the pressure valve: the world
is always reacting. Some card effects let players spend or reference Toll.

---

## §8 — Deadly Contests (physical conflict)

A **Deadly Contest** is any Contest where Hit Dice can be lost — characters are eligible to die.
(Formerly "combat encounter.")

**🔒 Threat & Open Floor (Playtest #1):** on entering, enemies reveal their **Threat** — the damage
they will deal — *upfront, before players commit*. The GM places Threat dice visibly in front of the
relevant players; Threat is locked at Contest start and resolves regardless of action order. Players
choose **fight** (accepting the incoming Threat), **flee**, or **negotiate** — engaging means
accepting the Threat. **Open Floor:** no fixed turn order; after Threat is revealed, players act in
whatever sequence makes narrative sense, deciding collectively moment to moment. Known stakes, real
tactical choice — not a surprise tax.

**Defensive dice & spillover:** when a player's defensive dice (from a card or React) fully clear an
incoming Threat pool, leftover dice may be applied defensively to **any target, including themselves**
— spillover is not restricted to allies.

**🔒 Resolve pool (replaces Guard):** at the start of any Contest (Deadly or Social), players set up a
**[Resolve]** layer — a temporary Hit Die pool that absorbs damage *before* the health pool. When
Resolve is depleted, damage hits actual Hit Dice. Narrated per class (*Bard's wit worn down /
Paladin's armor battered / Barbarian's rage fueling recklessness*). Cards that once made **Guard** now
heal Resolve or grant rerolls — Guard is eliminated.
- **Setup = a Resolve check.** Players establish Resolve by rolling a check like any other (they can
  Miss or Crit on it). ⚠️ Default pool is **2d6**; exact parameters still settling (see *Open
  questions*).
- **Overflow exists.** Damage overflows between Resolve and the health pool the same way defensive
  actions overflow — there is no hard wall between the two.

**🔒 Threat — the inverse of Resolve:** where **[Resolve]** is the player's *defensive* check,
**[Threat]** is the GM's *offensive* one. The GM determines Threat from the encounter itself (its
default source) and reveals it upfront (see Threat & Open Floor above). It is built/run like a check,
exactly mirroring a Resolve check. Primarily a Deadly-Contest mechanic, but Threat can also appear in
Social Contests (§9).

**Hit Dice (health):** the player's health resource — **always "Hit Dice/Hit Die," never "HP."**
- Level 1: all Hit Dice start at max value; no rolling for health at level 1.
- Damage: Threat dice deal damage equal to their face values, removing dice or reducing values.
- **Full-removal model:** a spent Hit Die is fully removed — no partial "shave." Intentional.
- **Post-Contest recovery:** there is **no breather/recovery rule currently.** (A short-rest effect is
  a known future direction — tracked in the design archive, not a current rule.)
- Enemies use fixed/maximized Hit Die arrangements, visible at Contest start — e.g. "this guard has
  three Hit Dice set at 6, 4, 2" — giving players tactical legibility to plan around.

**NPC threats — two valid GM techniques:** (a) **Real Threat dice** — roll actual Threat against the
NPC so "defend" actions have something physical to intercept (use when the NPC's survival matters
mechanically); (b) **Abstracted description** — give a health/severity description; "defend" changes
the narrated outcome rather than removing dice (use when survival is narratively, not mechanically,
significant). GM's discretion per scene; both legitimate.

**Physical dice as table components:** dice stay on the table as objects, not sheet numbers — enemy
Hit Dice in front of players; the Barbarian Rage pool; Cleric Prayer (Crit dice on the Prayer Core
card); the Druid Grove (d6s on tended cards). Everything is d6s — a handful per player covers it.

---

## §9 — Social Contests

A **Social Contest** is any Contest where Resolve is at risk but Hit Dice are **not**. (Formerly
"non-combat encounter.") 🔒 It uses the **same resolution engine** as a Deadly Contest — same
opposing-pool model, same Open Floor, same Miss/Crit/Toll.

- Both sides have a Resolve pool; "damage" chips at it. When one side's pool is depleted, the
  confrontation ends (defeated in debate as in battle).
- Social Resolve is narrated as *composure, credibility, emotional momentum*.
- "Attacks" are verbal challenges, pressure, or emotional appeals. The roll **is** the damage to the
  other side's Resolve. Cards work the same as anywhere.
- **Threat can appear here too** — social pressure aimed at a player's Resolve, set by the GM exactly
  like any Threat check.

---

## §10 — Card play rules

**Types & timing** (visual anatomy/colors → `design/card-anatomy.md`):

| Type | Cost | When played |
|---|---|---|
| **Act** | 1 (your spotlight) | On your turn — primary action |
| **React** | 0 | Any time, in response to another player's or the GM's action |
| **Core** | — | Always-active; face-up in Active area; never enters the deck |
| **Instinct** | — | **Reveal** when the quality drives an **Action**; choose one path — if the GM agrees: benefit party → `[Boost 2]`, or hinder → **Draw 2** |
| **Background** | — | **React** + Snap Check when trigger fires (card spent on play) · **[Mill]** at scene start |
| **Ancestry** | — | **Once per Scene** when its fictional trigger fires; **Snap Check** (shared bands: 1–3 fail · 4–8 choose 1 · 9+ choose 2). Act or React per card. |
| **Bond** | — | Find the moment; you and the named person each gain `[Boost 1]` |

**React window:** after every roll, before narration, there is a brief beat where React cards may be
played. Name it at the table.

**Zones:**

| Zone | Contents | Persists? |
|---|---|---|
| **Hand** | Currently held cards | Discards at scene end |
| **Active** | Core cards | Always — never discards |
| **Deck** | Undrawn cards | Reshuffles when empty |
| **Discard** | Played/discarded cards | Reshuffles into deck |

Class-specific zones (Druid Grove, Rogue Ace Pile) → `design/classes.md`.

**Equipment:** there is **no** universal equip-slot system or **Equip** keyword. The "always have my
gear" fantasy is baked into specific classes' own Core cards, case by case (currently Fighter and
Paladin). Other classes have no general equipment mechanic.

**Snap Check:** a **reaction check** — a one-die subset of the normal check procedure. Used on React
cards when the table needs a fast, high-variance resolution without building a pool or opposing dice.
Roll **1d6** (no Tier base pool, no opposing pool). Read the card's outcome bands or face table.
**Same Miss/Crit rules as any check:** a natural **1** is a **[Miss]** → 1 **[Toll]**; a natural **6**
**explodes** (roll one bonus die and add it). Most Snap Checks resolve on the single die; cards may
require a total of **7+** (i.e. must Crit) for the highest band. Cards print their own breakpoints or
face effects — there is no global Snap Check band scheme *(except **Ancestry** cards — see below)*.
*(Former **Luck Check** is retired — all full checks use the pool-vs-pool model in §5.)*

**Ancestry Snap Check bands** (locked June 2026 — all 10 Ancestry deck cards): roll **1d6** with
standard Miss/Crit rules. Read bands: **1–3** thematic failure · **4–8** choose **1** of three printed
options · **9+** choose **2** of the same three (requires **6** + explode). Options cap at niche fiction
and **[Boost 1]** max. Proof: `ancestry-snap-proof.html`.

---

## §11 — Keywords & terms

Instinct RPG has **three distinct keyword vocabularies**, each formatted with a different visual
weight so the table can tell at a glance what kind of word it is looking at:

1. **Impact Keywords** — *what the game does* (mechanics). Loudest: **filled color pills**.
2. **Index Keywords** — *what kind of card this is* (card types, class names, sorting/filter tags).
   Medium: **outlined color chips**.
3. **Narrative vocabulary** — *what's happening in the fiction* (descriptors). Quietest: **plain bold**.

The exact pill/chip colors and rendering rules — the **formatting gospel** — live in
`design/card-anatomy.md` (colors/tokens) and `design/writing-conventions.md` (usage). They must look
identical in every context, every time: cards, primer, and references.

### 1. Impact Keywords (mechanical — filled color pills)

Every word that carries a real, functional gameplay effect — the load-bearing terms.

| Impact Keyword | Meaning |
|---|---|
| **[Boost N]** | N dice added to a pool from card effects/other sources. Expire at scene end; removed if they show a 1. (Boost is the elevated keyword that absorbed the old **Bolstered** — Bolstered is retired.) |
| **[Crit]** | A natural **6** on a die (explodes once). After resolution, count Crits — each one lets you **gain** one **Flourish** from the played card. The die stays in the pool. |
| **Flourish** | A bonus option line on an ability card (section header on the card). Gained by spending Crit count — one Crit typically unlocks one Flourish. Not a die result. |
| **[Miss]** | A natural 1. Removed from the pool; gives the GM 1 [Toll]. A partial result is not a Miss. |
| **[Toll]** | GM resource generated by Misses. Escalates scenes. |
| **[Hit Die] / [Hit Dice]** | Player health resource. Always capitalized. Never "HP." |
| **[Resolve]** | Player's *defensive* pool, set up at Contest start via a Resolve check. Lost before the health pool. Replaces retired Guard. |
| **[Threat]** | The GM's *offensive* check — the **inverse of Resolve**. The damage an encounter will deal, determined by the GM from the encounter and revealed upfront. Primarily Deadly Contests; can also appear in Social Contests. |
| **[Aid]** | Ally-only assist: discard a card, narrate how it helps another player's check (not the card's normal effect — GM agrees), add 1 die. Capped at one per check. No Self-Aid. |
| **Mill** | *At scene start, you may discard this to draw 1.* On **Item** cards, **Background** deck cards, and React-subtype class ability cards. Replaces the old soft Mulligan.

**Declared Actions** (a related mechanical set, formatted **Bold + Capitalized**, not as pills):
**Action · Reaction · Draw · Discard · Shuffle · Cleanse · Snap Check · Scene**.

### 2. Index Keywords (sorting/filtering — outlined color chips)

Words that **classify a card so it can be sorted or filtered** — they have **no effect on
resolution**. They render as **outlined chips** in their associated type/class color: more present
than plain text, quieter than a filled Impact pill. This middle tier keeps the card studio, primer,
and filters visually consistent without overloading a card with "loud" mechanical pills.

- **Card types:** Act · React · Core · Instinct · Background · Bond · Flaw · Ancestry · Item
- **Class names:** the canonical roster lives in `design/classes.md` (e.g. Barbarian, Warlock).
- **Other card-sorting tags** as they arise.

### 3. Narrative vocabulary (descriptive only — plain bold)

🔒 **All "conditions" are currently descriptive only.** None carry enforced mechanics. They exist to
give the table a shared word for something in the fiction; **what they mean and how they resolve is
entirely the GM's call.** They are written as plain **bold title case** — never as colored pills.

Current narrative terms: **Exposed · Rattled · Rooted · Hidden · Marked · Sundered · Break.**
*(**Bolstered** is gone — replaced by Boost. Any prior "mechanical" reading of Hidden/Marked/Sundered/
Break is retired; they are descriptions now.)*

> **Planned (Nathan's prerogative):** a GM- and player-facing reference offering *suggested* ways these
> narrative terms might resolve mid-Contest or in exploration — explicitly recommendations only, with
> the GM holding final say. Not a rules change; a guidance aid. Tracked as future scope.

> Forbidden/retired terms and their replacements (Guard, Bolstered, Strong Roll, Encounter,
> Failure-as-trigger, Self-Aid, DC, die-size upgrades, etc.) are catalogued in
> `design/writing-conventions.md`.

---

## §12 — Character creation (creation = play)

*Good enough for now; subject to change.* Character creation is itself play — roughly one hour.
Characters emerge from the cards they choose and the sheet cards they fill in at the table — not from a stat block.

**Steps (playtest flow):** (1) **Choose 5 Instincts** from a pool of **30**; (2) **Choose 1 Bond**;
(3) **1 Connection** — write **your own character's name** on it and set it aside (it shuffles into
*other players'* decks, not yours); (4) **Choose 1 Background** (of 12); (5) **Choose 1 Ancestry**
(of 10); (6) **Choose 1 Item** → shuffled into your deck; (7) **Class Core** — at least **2** Core
cards face-up in front of you (most classes have 2); (8) **Select 12 Class Ability cards** for your
deck; (9) **Read your Core** — grab any extra cards it requires at character creation.

**Deck cards vs sheet cards:** Background, Ancestry, and Bond **deck cards** are fiction triggers + mechanics only (no Origin stems as of June 2026). Persistent backstory and write-in slots live on separate **Character**, **Class**, and **Ancestry sheet cards** (designed separately). Instinct cards use the dual-path fork only — no stems.

**Deck math — 21 cards in the deck:**

| Component | Count |
|---|---|
| Instinct cards | 5 |
| Bond | 1 |
| Background | 1 |
| Ancestry | 1 |
| Item | 1 |
| Class ability cards | 12 |

*Not in the 21:* Connection (other players' decks), Core cards (face-up in front of you). Instinct
draft pool: 30 options at creation.

---

## §13 — Class mechanics (system-level)

Full per-class identity, tag ownership, and unique mechanics live in **`design/classes.md`**. The
system-wide truths that constrain *all* class design:

- **Tag ownership:** one class owns each narrative term it leans on as primary user; overlap is a
  design problem to resolve.
- Misses (natural 1s) **always** generate [Toll], regardless of class or card effect.
- [Resolve] is set up at Contest start (via a Resolve check), before any cards are played.
- [Crit] options (**Flourishes** on the played card) are declared after all dice are fully resolved; spending a Crit does not remove the die from the pool.

Two examples that touch core rules directly (detail in `classes.md`): **Barbarian Frenzy** triggers at
a Rage pool of **5+** dice (grants flat [Boost 3], then fully empties the pool); **Warlock** first
Patron invocation per scene is free (Warlock chooses the Mark), later invocations cost a GM-rolled
random Mark — and this cost must be stated **on the card itself**.

---

## Open questions (not yet locked) ⚠️

1. **Resolve check parameters** — default is 2d6, but the exact setup (cost, action type, dice) is
   still settling. (§8)
2. **Narrative-term guidance reference** — Nathan plans a GM+player aid suggesting how descriptive
   terms (Exposed, Hidden, etc.) might resolve in play; recommendations only, GM has final say. (§11)

---

*Card anatomy & colors → `design/card-anatomy.md` · wording, forbidden terms & keyword formatting
gospel → `design/writing-conventions.md` · classes → `design/classes.md`.*
