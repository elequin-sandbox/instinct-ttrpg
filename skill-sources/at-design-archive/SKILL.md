---
name: at-design-archive
description: Instinct RPG design archive — a holding area for DEPRECATED mechanics and FUTURE-SCOPED ideas that are NOT currently in the game. Load this skill ONLY when Annie explicitly wants to revisit a cut design, research what was tried before, or explore future directions. NEVER load this skill during card design sessions, rework sessions, tutorial writing, asset creation, or any session that produces content a real player or GM would read. This skill must never be used as a source of truth for how the game currently plays. The authoritative current rules are in at-core-rules. Triggers ONLY on phrases like "what did we try before," "what was the old version," "what's in the archive," "revisit a cut mechanic," "what are the future scope ideas," or "what was deprecated." If you are unsure whether to load this skill, load at-core-rules instead.
---

# Instinct RPG — Design Archive

⚠️ **ARCHIVE ONLY.** Nothing in this file reflects the current rules of Instinct RPG. For current rules, load **at-core-rules**. For current card design, load **at-design-system** and **at-card-language**.

This file exists so no idea is lost. It does not mean these ideas are coming back. Entries are organized by status (deprecated vs. future-scope) and topic within each.

---

## HOW TO USE THIS FILE

- **Deprecated:** Mechanics that were tried and deliberately cut. They exist here as a record of what was tried and why it was removed. Do not bring them back without explicit design discussion and Annie's approval.
- **Future-scope:** Ideas that are interesting but not ready — open design questions, proposed directions that haven't been decided, and systems flagged for later tiers or sessions.

Entries include: *what it was, why it was cut or deferred, and any open directions discussed.*

---

## SECTION A — DEPRECATED MECHANICS

These were once part of the game. They are no longer in the game. Do not use them on cards, in tutorials, or in any game-facing material.

---

### A0 — Item Check / Placed Dice / Saves (Retired: June 2026)

**What it was:** A late item subsystem. An *Item Check* (roll 2d6) let a player physically *place*
the rolled dice on a target as a condition — **[Rooted]**, **[Exposed]** (debuffs, filled pills) or
**[Disguised]** (buff, outline pill). The target cleared them with a **Save** (GM rolls equal dice;
each that matched-or-beat a placed die removed it). Came with buff/debuff pill distinction, fixed vs.
variable placement (e.g. `Rooted 1`), and item card anatomy built around it.

**Why cut:** Too complex. Stripped back to the simplest possible item system for the next playtest.
As of June 2026 there is **no** Item Check, no placed dice, and no Saves. Items remain a classless
card type but use only Flavor + Effect (+ optional Crit) until the simpler version is designed. All
former condition words (Rooted, Exposed, Hidden, etc.) are now plain-bold **narrative** terms with no
mechanics (see `design/core-rules.md §11`).

### A0b — Bolstered (Retired: June 2026 — folded into Boost)

**What it was:** A positive-state condition (deep-green pill) meaning strengthened/healed/fortified;
several class abilities "blocked Bolstered." **Why cut:** Boost was elevated to the general
dice-adding / strengthening keyword and absorbed Bolstered's role. Do not use Bolstered; use
**[Boost]**.

### A0c — Catch Your Breath (FUTURE-SCOPE, not yet designed)

**Direction:** A planned short-rest effect that lives *in the deck* as a card, replacing the old
post-Contest "breather" recovery (which was removed). Currently there is no recovery rule. Annie will
design Catch Your Breath later; noted here so the intent isn't lost.

---

### A1 — Guard (Retired: Playtest #1, June 2025)

**What it was:** A temporary protective pool placed at the start of combat. Guard dice absorbed incoming damage before hitting the health pool. Paladin was the proactive Guard specialist; Cleric was the reactive provider.

**Why it was cut:** Combat and social encounters felt like two different games (Playtest #1, Weakness W1). Guard was a combat-only mechanic that created a distinct conceptual layer separating physical and social encounters. Unification required a mechanic that worked in both modes.

**What replaced it:** **[Resolve]** — same function (temporary buffer before health pool), but narrated differently per class and context, and applicable to both physical and social combat. See at-core-rules.

**Implication:** Any card referencing Guard should be reworked to reference Resolve, healing, or reroll mechanics. Guard does not exist in the current system.

---

### A2 — Strong Roll (Retired: Playtest #1, June 2025)

**What it was:** The original name for the top result tier (above Success). Cards referenced "Strong Roll rewards" and the "STRONG ROLL" section heading.

**Why it was cut:** "Crit" is more intuitive, more universally understood, and shorter on card text. The change was made alongside the full terminology audit post-Playtest #1.

**What replaced it:** **[Crit]** throughout. The card section heading is now "CRIT." The term "Strong Roll" is retired.

---

### A3 — Bane Passive Debuffs (Retired: Playtest #1, June 2025)

**What it was:** Flaw (then called Bane) cards had "while held, [negative effect]" language — a passive mechanical penalty that applied for as long as the card sat in your hand.

**Why it was cut:** Cognitive overhead without drama. Jimmy at Playtest #1: "Do I just track this in my head while holding the card?" Nathan cut it on the fly mid-session and confirmed the cut in post-playtest discussion.

**The principle that replaced it:** The hand slot cost IS the consequence. Holding a Flaw takes up a hand slot that could hold something useful. That is punishing enough. No passive tracking required.

**What this means for card text:** No Flaw or Bane card should have "while held, [negative effect]" language. The Dismiss condition is how Flaws leave the hand.

---

### A4 — Fighter Stance Cards (Retired: Post-Session, pre-Playtest #1)

**What it was:** Fighter used a stance system. Stances modified the Fighter's action profile while held — a persistent positional identity.

**Why it was cut:** Stances are mechanically cleaner as a Monk-owned concept. Stances work better in the Monk's chaining and sequencing identity (Iron Palm / Wind Step / Cobra) than in Fighter's loadout/weapon identity.

**What replaced it:** Fighter v2 uses a **weapon slot system**: Active and Sheathed slots. Discard 1 to swap. Draw 1 when using Active weapon. Fighter's identity is about loadout and weapon mastery, not stance-based positioning.

**Note:** Monk now owns stance mechanics — Iron Palm, Wind Step, Cobra. These are not Fighter cards.

---

### A5 — React as Standalone Card Type (Retired: Post-Playtest #1 redesign)

**What it was:** React was a separate card type — a distinct category from Act. Condition was also its own type.

**What changed:** Condition cards were converted to Act cards (passive-while-held effect, but live in the Act category). React timing is still a valid card timing, but React is now a property of certain cards (cost 0, triggered timing) rather than a distinct type in its own right.

**In the current system:** Card types are: Act, React, Core, Instinct, Background, Bond, Ancestry, Flaw, Boon-family umbrella (Background + Bond + Ancestry), Bane-family umbrella (Flaw + Status). React is a timing modifier, not a separate category requiring its own type entry.

---

### A6 — 4-Band Result System (Retired: June 2026, replaced by DC Ladder)

**What it was:** An earlier resolution framework describing four result tiers — **Crit** (success + bonus options), **Success** (clean hit), **Partial** (success with cost), **Miss** (failure). Referenced in some design session files and class-identity.md.

**Why it was retired:** Annie confirmed in June 2026 that the DC Ladder (Binary succeed/fail against a target number, 3–16) is the actual resolution system. The 4-band framework was never implemented in the v3 tutorial and was not recognized as the active system. "Partial" has no equivalent in the current ruleset.

**What replaced it:** The DC Ladder (§6 in at-core-rules). Toll comes from rolling 1s (miss dice), not from a result tier. Crit options come from rolling max-face dice (6s), not from a result tier. Failure is simply falling short of the DC.

---

### A7 — Luck Check as a Pill (Retired: June 2026 language audit)

**What it was:** `[Luck Check]` was formatted as an inline colored pill, like `[Boost 2]`.

**Why it was changed:** Luck Check is not countable or trackable — it's a declared action, not an effect keyword. It belongs in the Bold+Cap tier, not the pill tier.

**Current standard:** **Luck Check** (Bold+Cap, no pill, no color). See at-card-language for the full formatting tier system.

---

## SECTION B — FUTURE-SCOPE & OPEN DESIGN ITEMS

These are not currently part of the game. They are ideas that have been flagged as worth exploring — either directions from Playtest #1 that were proposed but not decided, or systems that have been deferred to a later design tier.

**Do not treat any of these as current rules.** They are staging, not canon.

---

### B1 — Empty Hand Rule (Open Item — No Rule Yet)

**Why it matters:** When a player exhausts their hand, currently nothing happens. This is a missed dramatic opportunity. Jimmy at Playtest #1 observed that card depletion naturally functions as spotlight management — but only if the GM recognizes and leverages it.

**Proposed directions (not decided):**

- **Desperation Draw:** When your hand hits zero, immediately draw 1 card. Play it or discard it — your last instinct before running on pure adrenaline.
- **Empty hand = GM gets Toll:** When a player empties their hand without ending the scene themselves, GM gains 1 [Toll]. Rewards bold card play while giving the GM an escalation tool.
- **Scene-end trigger:** Emptying your hand is a GM signal to transition the scene away from that player. Write explicitly into the GM guide: "When a player plays their last card, find a way to shift focus before the next beat."

---

### B2 — Cards Mandatory vs. Optional (Open Philosophical Question)

**Current state:** Cards are optional but strongly incentivized. A player can make a vanilla check without playing a card — just dice, no bonus. This is the implied rule but has not been formally decided.

**Why it matters:** Jimmy at Playtest #1 pushed for mandatory cards. Ben's analysis suggested players were already treating cards as close to mandatory in practice. The gap between written rule and felt experience is worth closing deliberately.

**Proposed directions (not decided):**

- **Cards mandatory, always:** No card = no action. Running out of hand = out of the scene until it resets. High stakes, maximum commitment.
- **Cards mandatory for upside:** Vanilla check (2d6 base, no bonus) is always available. Cards give access to the upside layer — Boost dice, Crit options, class abilities, conditions. Playing without cards isn't forbidden, but it's thin and accumulates Toll on 1s.
- **Cards mandatory for identity, with safety valve:** Cards required to trigger anything above a basic check — but every player has one "Gut Instinct" free action per scene (basic attack or social move, no card required). Preserves accessibility, maintains intent.

---

### B3 — Wave Structure in Combat (Open Item)

**The question:** When combat damage hits, does it overflow between layers (Resolve → Hit Dice) in the same hit, or does each layer need to be cleared fully before the next can be damaged?

**Positions discussed at Playtest #1:**
- **No overflow (wave structure):** Players must clear the Resolve layer fully before Hit Dice can be touched. Adds tactical depth about when to engage.
- **Allow overflow (Nathan's lean):** Cleaner, simpler, and more dramatic. A single big hit can punch through both layers. Needs playtesting to confirm.

No direction chosen yet.

---

### B4 — Universal Discard-to-React (Proposed Direction, Not Locked)

**What was proposed (C5, Playtest #1):** Discard 2 cards to use any Act card as a React. This would give every player a baseline reaction option — costly, but always available.

**Why it was proposed:** Players repeatedly tried to react to things mid-session and were stopped because they had no React cards. The impulse to react seems natural to the game's implicit promise.

**Status:** Direction proposed but not locked. Needs to be tested before appearing in any player-facing material.

---

### B5 — React Window Naming (Proposed Addition)

**What was proposed:** After every roll, before narration, there is a brief beat where React cards can be played. Naming this window explicitly in the rules would make it feel more alive.

**Status:** The window exists informally. Naming it in the teach and GM guide is a pending improvement, not yet a formal rule.

---

### B6 — Scar Cards (Future Design — Campaign Mechanic)

**What it is:** When a player drops to zero Hit Dice, they gain a Scar card — a new Flaw that enters their deck, themed to how they were injured. The Scar card has a damage type, a fill-in ("Caused by ___"), and a double-edged hook (drawback in some contexts, triggerable positive in others).

**Example:** *Concussed: once per scene, play through the disorientation — describe how — and gain [Boost 2] on your next check.*

**Status:** Flagged as a high-value campaign mechanic at Playtest #1. Not urgent for one-shots. Ready to design when campaign play is prioritized.

---

### B7 — Context Tags on Cards (Proposed Component)

**What was proposed:** Add small icons to cards indicating primary scene context (⚔️ combat / 🗣️ social / 🔍 exploration). Non-restrictive — just sets player expectations at deck-build time.

**Why it was proposed:** Jimmy at Playtest #1 drew Barbarian cards that were combat-relevant but couldn't predict this at deck-build. Context tags would let players map their deck before play starts.

**Status:** Pending decision. Would require a visual system and placement standard. Not in any current card design.

---

### B8 — GM-Facing Cards / Scene Frames (Open Question)

**The question:** Does the GM have their own cards? Scene frames? Pressure cards? Enemy ability decks?

**What exists now:** Enemy cards with Hit Dice and modifier cards (Protected, Berserker, Vampiric). The GM doesn't have a hand or deck in the current design.

**Status:** Unresolved system-level design question. May intersect with how Toll is spent formally.

---

### B9 — Leveling Design (Deferred)

**The question:** Does leveling add new cards to the deck, or do the cards themselves change (upgrades, transformations)?

**Status:** Tiers are defined (1-3 = Tier 1, 4-6 = Tier 2, 7-9 = Tier 3) but the mechanical process of leveling up has not been designed. Currently: players acquire higher-tier class cards when leveling; exact procedure unspecified.

---

### B10 — Stack / Rally Roll Resolution (Unresolved)

**The question:** When multiple players Stack on a single action, who rolls? The initiating player only, or does each player roll and contribute their dice?

**Status:** Unresolved. Needs a rule before Stack cards can be reliably taught.

---

### B11 — Distance Band Definitions (Deferred)

**The question:** Does Instinct RPG use Daggerheart-style distance bands (Close / Near / Far / Very Far) or a custom system?

**Status:** No decision made. Some cards use spatial language without a defined framework. Needs resolution before spatial cards are finalized.

---

### B12 — Open Design Tensions from Playtest #1

**T1 — Conditions: Mechanical Facts vs. Narrative Vocabulary**

Currently: conditions are narrative vocabulary adjudicated by the GM contextually. Rich and flexible; potentially inaccessible for GMs who aren't comfortable improvising. The "here: [interpretation]" parenthetical is a middle path.

The underlying question: does Instinct RPG want to be a game where rules guide to consistent outcomes, or a game where rules give vocabulary and trust the table? These produce different GM skill requirements and different review profiles.

*No direction recommended — this is a values decision for the designer.*

**T2 — Cards Optional vs. Mandatory**

See B2. The written rule and the felt experience don't match. Worth closing deliberately before next playtest.

---

### B13 — Warlock Wave Architecture (Deprecated but Revisitable)

**What existed:** Multiple Warlock ability design experiments including different Patron mark architectures. Some early Patron designs used per-patron color schemes.

**Current state:** Unified standard Warlock color for all Patron cards. Patron Bane section uses boxed treatment. Mark tables per Patron are locked (see project knowledge). The per-p