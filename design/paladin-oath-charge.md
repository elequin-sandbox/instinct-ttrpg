# Paladin — Oath & Scene Stand (design draft)

> **Status:** draft — June 2026. Replaces **Conviction · Defiance** for the Paladin **core** loop.
> The **Oath** card is your permanent creation pick; your **Stand** is the scene phrase rolled on it.
>
> **Sibling docs:** `design/classes.md` · `design/card-anatomy.md` · `design/core-rules.md`

---

## Terminology

| Term | Scope | Notes |
|---|---|---|
| **Oath** | Campaign — the Core card you pick at creation | Stays in Active area; defines your word pools |
| **Stand** | Scene — Verb + Noun phrase | Lighter than *Vow*; changes every scene. Colloquial: *"What's your stand this scene?"* |
| **Fulfill** | Once per scene | Primary purpose of the **Action** must serve the **Stand** (GM gate) |
| **Break** | Optional at **Enter** | Old Defiance fantasy — without losing the Oath card for the session |

*Rejected:* Charge (too generic), Mandate (clunky), Vow (too weighty for scene-to-scene).

---

## Character creation

Mirrors Warlock **Patron** pick:

1. Pool of Oath Core cards (5 prototypes + blank template for homebrew).
2. Pick **one** — lives in **Active area** permanently.
3. Auto cores: Loadout · Bulwark · Build Your Deck.

**Blank template:** `oath-template-paladin-core` — fill title, subtitle, verbs, nouns; procedure is pre-printed.

---

## Oath card anatomy

| Zone | Content |
|---|---|
| **Verbs** | 6 indexed (1–5 + ★ Choose) — lateral, spread-out word choice |
| **Nouns** | 6 indexed — avoid redundant pairs (not Innocent + Weak) |
| **Set Your Stand** | Roll 2d6 at **Enter**, place dice on Verb + Noun |
| **Fulfill Your Stand** | Once/scene: primary-purpose GM yes → add both dice to roll |
| **Break Your Stand** | Optional at **Enter** before rolling (see below) |

### Word-pool design rules

- Prefer **lateral nouns** (Frail, Threshold, Silence) over literal class-fiction (Innocent, Guilty, Realm).
- Verbs should span modes: protect *and* witness *and* carry — not five synonyms for "hit."
- Goal: players **argue creatively** what *Shelter the Ember* means this scene.

---

## Procedure (canonical — every Oath card)

### Set Your Stand

When you **Enter** a **Scene**, roll **2d6**. Place one die on a **Verb** and one on a **Noun**. Your **Stand** is that phrase. It is your priority above all else this **Scene**. On **6**, choose any word in that list.

### Fulfill Your Stand

Once per **Scene**, when the GM agrees your **Action**'s *primary purpose* fulfills your **Stand**, add **both dice** from the card to that roll, then remove them.

Defensive stands naturally pair with **Bulwark** / **[Resolve]** cards in combat — no extra rule required on the Oath card.

### Break Your Stand (replaces old Defiance shuffle)

When you **Enter** a **Scene**, *before* rolling, you may **Break** your **Stand** — narrate turning from it.

- **Discard** your hand, **Draw** that many (hand cleanse — rare debuff/bane relief path).
- You do **not** roll a **Stand** this scene.
- Your Oath card **stays in the Active area** — no shuffle into the deck.

**Why not shuffle the Oath into the deck?** In a ≤4-scene session the card may never return — anticlimactic inverse of Warlock Patron highs. Break is a **scene mulligan**, not exiling your class identity.

#### Break — open tuning (pick one after playtest)

| Option | Extra cost | Feel |
|---|---|---|
| **A — Free once/session** | None beyond skipping Stand | Generous; enables big narrative pivots |
| **B — Stand debt** | Cannot **Fulfill** next scene | Soft cooldown |
| **C — Remorse chip** | GM places 1 Remorse; clear via hard narrative act or **Cleanse** | Fiction-forward |
| **D — Stain bane** | Shuffle **Stain** (single-scene bane, auto-clears at scene end) | Mechanical bite without losing Oath |

**Recommendation:** **A** for first playtest; add **B** if Break dominates.

---

## Oath pool (current)

| Oath | Subtitle | Sample Stand |
|---|---|---|
| **The Open Hand** | What you reach for defines you. | *Shelter the Frail* · *Witness the Stranger* |
| **The Severed Ledger** | Some accounts refuse to stay closed. | *Name the Liar* · *Settle the Debt* |
| **The Last Bastion** | When everything else gives way, something must not. | *Hold the Line* · *Seal the Gate* |
| **The Wax and the Wick** | You carry fire where the map runs out. | *Reveal the Path* · *Kindle the Spark* |
| **The Old Compass** | North is whoever needs you when you arrive. | *Find the Lost* · *Answer the Promise* |

**Visual proof:** [`paladin-oath-proof.html`](../paladin-oath-proof.html)

**Templates:** `oath-template-paladin-core` · `patron-template-warlock-core`

---

## Retired

- **Conviction · Defiance** — archived.
- Scene **Charge** terminology — renamed **Stand** (June 2026).
- D&D-subtype names (Devotion / Vengeance / Crown) — replaced with lateral titles.

---

*Classes → `design/classes.md` · inventory → `card-inventory.md`*
