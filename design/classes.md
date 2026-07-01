# Classes — identity, associations & locked mechanics

> **Purpose:** What each class *is*, the narrative terms and mechanics it owns, what's locked, and
> what's still open. Verify a class's identity and open items here before writing new cards for it.
> **Status:** current, but several classes have ⚠️ open redesigns (see flags). **Last updated:** July 1 2026.
>
> **Sibling docs:** rules → `design/core-rules.md` · card look → `design/card-anatomy.md` · wording →
> `design/writing-conventions.md` · inventory → `card-inventory.md`.

**Legend:** 🔒 locked · ⚠️ in flux / needs a design decision.

> ⚠️ **Global ripple to reconcile here:** two recent system changes cut across class identities and are
> only *word-swapped* below, not fully redesigned — flagged where they bite:
> - **Bolstered is retired → folded into [Boost].** Classes previously defined as "Bolstered
>   specialists" (Cleric, Bard) need their identity re-confirmed, not just the word changed.
> - **All conditions are narrative-only now** (Exposed, Rattled, Rooted, Hidden, Marked, Sundered,
>   Break). "Tag ownership" is therefore reframed as *which class is the primary user/associate of a
>   narrative term*, plus each class's own **mechanics** (Rage, Beastform, etc.), which are unaffected.
> - Also global: **Guard eliminated**, **d6-only**, **Strong Roll → [Crit]**, **Failure → Miss**.
> - **Playtest 4 addition:** the class's narrative term (Exposed, Sundered, Marked, etc.) is now also
>   the natural **Crit Flourish keyword** for that class's cards (`core-rules.md` §5, three colorings).
>   The ownership table below is unaffected — it still names who *primarily uses* each term; the
>   flourish-cards track decides, card by card, which of those terms get a printed Flourish number.

---

## §1 — Class identities

| Class | One-line identity | Emotional core |
|---|---|---|
| **Cleric** | Reactive protector — ⚠️ *was "Bolstered specialist"; re-confirm as [Boost]/Resolve protector* | *Devoted:* I am building toward something. My faith accumulates. |
| **Barbarian** | Hand-burn engine — trades future options for present devastation | *Unstoppable:* The worse it gets, the more dangerous I am. |
| **Wizard** | Preparation + precision + consequence — reshapes scene geometry | *Careful:* I am always three steps ahead. My power has a cost. |
| **Fighter** | Weapon master & deckbuilder — weapon in hand = passive + React | *Inevitable:* I am always prepared. My loadout IS my strategy. |
| **Bard** | Amplifier who plays best last — accumulates power as allies act | *Magnetic:* I make everyone look good. Then I steal the scene. |
| **Warlock** | Transactional engine — two cost currencies (Hit Dice & Debt) | *Desperate:* I am spending myself. Every hit is a deal with darkness. |
| **Druid** | Terrain owner — cards read differently in Beastform | *Accepting:* Failure grows into something. Nothing is wasted. |
| **Monk** | Momentum builder — stances modify chaining rules, not damage | *Present:* I am the stillness before the strike. Then everything. |
| **Paladin** | Oath-bound defender — **Vow** each scene; **[Resolve]** via Bulwark | *Righteous:* I know what I'm vowed to this scene — and when it matters, I put everything behind it. |
| **Rogue** | Information broker — Stow as intentional planning | *Inevitable (other direction):* I already know how this ends. |
| **Ranger** | Patient planner — Trap cards, environmental control | *Patient:* I already planned for this. I'm three steps ahead. |

> 🔒 **Paladin (June 2026):** Player picks 1 **Oath** Core card at creation (Warlock Patron parallel).
> Each scene: at **Scene start**, roll 2d6 onto Verb + Noun lists → **Vow** phrase; once per scene,
> GM-gated fulfill adds both dice → **Boost 2**. **Break Your Oath:** defiance → dice to **Resolve**;
> GM **Toll 2** vs you. **Bulwark** = extra **[Resolve]** die + re-rolls; **Parry This** adds
> **[Resolve]** to **Defensive** rolls in **Contests** (no Oath tie-in). Detail →
> `design/paladin-oath-charge.md`.

---

## §2 — Narrative-term association & class mechanics

Conditions are narrative now, so this is "which class primarily *leans on* a term," plus the class's
own mechanics. 🔒 **Ownership rule:** one class is the primary user of each term/mechanic — overlap is
a design problem; retire it from one class or build a distinct parallel.

| Class | Primarily uses / produces | Responds to |
|---|---|---|
| **Cleric** | ⚠️ [Boost] (was Bolstered) | allies who are Exposed/Rattled — React triggers |
| **Barbarian** | Rage, Blood Price; **Sundered** (narrative) via Break on Crit Strike | Exposed (self via Rage), damage to self |
| **Wizard** | Arcane Burn, Prepared | Marked, Exposed, Sundered (hooks open ⚠️) |
| **Fighter** | Marked (narrative), Battle-Hardened, Exchange | weapon in hand, Marked targets, Sundered (hooks open ⚠️) |
| **Bard** | Rally Token, Performance, Notoriety; ⚠️ [Boost] (was Bolstered) | Rally Tokens (party spends), ally actions (Resonance) |
| **Warlock** | Debt (GM-held), Pact, Hunger | Hit Die cost, Debt resolution, Patron Entry windows |
| **Druid** | Beastform, Living Ground | Living Ground presence, Beastform alternate effects |
| **Monk** | Iron Palm / Wind Step / Cobra (stances) | Strike-chain states, prior-contact flags |
| **Paladin** | **Vow** (scene Verb+Noun), **[Resolve]** via Bulwark | Vow broken / left unfulfilled (table narrative) |
| **Rogue** | Exposed, Hidden (narrative), Stow | Stow (own), Exposed targets for strikes |
| **Ranger** | Marked, Rooted (narrative), trap placement | Marked targets, Exposed, environmental states |

---

## §3 — Locked mechanics per class

- **Cleric:** Reactive protector. `Called to Hand` searches for Reacts. Oath of the Threshold = only
  non-Warlock Debt source. Builds up, releases through allies. ⚠️ confirm post-Bolstered identity.
- **Barbarian:** `Rage` + `Blood Price` are the defining mechanics — don't add a third stacking one
  without discussion. Break on Strike, augmented on Crit → **Sundered** (party gift). Hand-burn is
  intentional.
- **Wizard:** `Prepared` loads one Act before the scene. `Study` can immediately Prepare a searched
  card. Arcane Burn enters on overload — gives Focus advantage, ⚠️ (formerly "blocks Bolstered" —
  restate vs [Boost]).
- **Fighter (v2):** Selects 3 weapons from a pool of 8. All weapons have **Exchange**. Weapon in hand
  = passive + potential React + maneuver roll. Stances moved to Monk — Fighter has no stance cards.
- **Bard:** Performance names a term — allies gain advantage on it. `Improvise` gives cards away.
  Resonance = italicized effect text, no label. Encore is Tier 2+. ⚠️ confirm post-Bolstered identity.
- **Warlock:** Hit Die costs (immediate) + Debt (GM timing). Pact halves Hit Die costs, grants Patron
  Entry. Hunger ⚠️ (formerly "blocks Bolstered" — restate). Pact + Hunger stacking is intentionally
  dangerous — trust the table.
- **Druid:** Only class with dual effect lines (normal + BEASTFORM). Beastform blocks Speak entirely.
  Living Ground is a persistent zone — not a separate card.
- **Monk:** Owns stance-switching (modifies chaining, not damage). Iron Palm: Strike→Strike chain
  (cap 2; Crit removes cap once/scene). Wind Step: Move↔Strike freely; full Rooted immunity. Cobra:
  prior-contact becomes a standing counter.
- **Paladin:** Pick 1 **Oath** at creation (Active area). **Vow:** 2d6 at **Scene start** on Verb+Noun;
  once/scene GM-gated fulfill adds both dice → **Boost 2**. **Break Your Oath:** defiance → dice to
  **Resolve**; GM **Toll 2** vs you this scene. **Bulwark:** roll an extra **[Resolve]** die and
  re-roll any **[Resolve]** dice; **Parry This** adds **[Resolve]** to **Defensive** rolls in
  **Contests**. Replaces Conviction·Defiance.
- **Rogue:** Owns **Stow** (intentional planning). Primary Exposed user. Hidden = primary defensive
  framing. Stow = cards hidden from other players.
- **Ranger:** Owns **Trap** cards (place roll → trigger-condition fire). Shares Rooted framing with
  Druid. Primary Marked user.

---

## §4 — Open design items

| Class | Open items |
|---|---|
| **Paladin** | Oath pool expansion; playtest Break (Resolve + Toll 2) at table. |
| **Fighter** | Redesign in progress — 9 Act cards drafted; Crit blanks need Nathan; Arms at the Ready + Arsenal revised for weapon slots. |
| **Cleric / Bard** | ⚠️ Re-confirm identity now that Bolstered is folded into [Boost]. |
| **Wizard / Fighter** | Sundered consumption hooks needed. |
| **Warlock** | Party-gift card not yet designed. |
| **Ranger / all** | Marked expansion to at least 3 classes total. |
| **All classes** | 🔒 **Playtest 4 card audit (P4)** — strip legacy unit-linked condition complexity from active pool cards (PbtA-style: one clear effect + optional Flourish band, not stacked forks); replace GM-tracked per-unit conditions with the Crit Flourish system (`core-rules.md` §5) wherever it cleanly applies. Model cards: pared **Smite** (Paladin) / **Strike** (Barbarian). Owned by the flourish-cards + pool-simplification Playtest 4 tracks; top ~20 active abilities first. |

---

## §5 — System-level locked decisions (all classes)

- A **Miss** always advances the scene — never a dead stop.
- Balance is deferred to the table — no preemptive caps.
- **Passive OR active — never both** on the same card.
- Color in `.chead` = class ability cards ONLY.
- Crit "draw a card" is not a default option.
- Impact pills always inline in effect text — never in a separate header.
- Minimum **20-card deck**; weapons count toward it.
- **Exchange** is system-wide — any weapon card may be discarded at scene opening.
- **Guard is eliminated** — never a tag or mechanic.
- **Strong Roll → [Crit]** throughout.
- 🔒 **Crit Flourishes resolve immediately when spent** (Playtest 4/P2) — no card should require the
  GM to track a lingering per-unit condition between turns. Full mechanic → `core-rules.md` §5.

---

## §6 — Tutorial playtest party

**Playtest #1 (June 4, 2025):** Rogue · Barbarian · Warlock.
**Target tutorial party (design goal):** Rogue · Fighter · Bard · Warlock — these four should be fully
audited before tutorial deck lists are written.

---

*Rules → `core-rules.md` · card look → `card-anatomy.md` · wording → `writing-conventions.md`.*
