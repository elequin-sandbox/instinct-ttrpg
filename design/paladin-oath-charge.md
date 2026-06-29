# Paladin — Oath & Scene Vow (design draft)

> **Status:** draft — June 2026. Replaces **Conviction · Defiance** for the Paladin **core** loop.
> The **Oath** card is your permanent creation pick; your **Vow** is the scene phrase rolled on it.
>
> **Sibling docs:** `design/classes.md` · `design/card-anatomy.md` · `design/core-rules.md`

---

## Terminology

| Term | Scope | Notes |
|---|---|---|
| **Oath** | Campaign — the Core card you pick at creation | Stays in Active area; defines your word pools |
| **Vow** | Scene — Verb + *the* + Noun phrase | Changes every scene. Colloquial: *"What's your vow this scene?"* |
| **Fulfill** | Once per scene | GM agrees your **Action** fulfills your **Vow** → add both dice to **Boost** the roll |
| **Break** | Optional at **Enter** | Old Defiance fantasy — without losing the Oath card for the session |

*Rejected:* Charge (too generic), Mandate (clunky), Stand (June 2026 interim — replaced by **Vow**).

**Card vs table:** Oath cards show the minimum text; GM / creation supplement explains placing dice on Verb + Noun lists and reading the phrase aloud.

---

## Character creation

Mirrors Warlock **Patron** pick:

1. Pool of Oath Core cards (5 prototypes + blank template for homebrew).
2. Pick **one** — lives in **Active area** permanently.
3. Auto cores: Loadout · Bulwark · Build Your Deck.

**Blank template:** `oath-template-paladin-core` — fill title, subtitle, verbs, nouns; procedure is pre-printed.

---

## Oath card anatomy (on-card text)

| Zone | Content |
|---|---|
| **Enter line** | Roll 2d6 to determine your **Vow** |
| **Verb** | 6 indexed pills (1–5 + ★ Choose), centered |
| ***the*** | Centered divider (visual read-aloud cue) |
| **Noun** | 6 indexed pills, centered |
| **Priority** | One line — priority above all else this **Scene** |
| **Fulfill** | Once/scene GM yes → both dice **Boost** the roll |
| **Break** | Optional at **Enter** before rolling (italic box) |

### Word-pool design rules

- Prefer **lateral nouns** (Frail, Threshold, Silence) over literal class-fiction (Innocent, Guilty, Realm).
- Verbs should span modes: protect *and* witness *and* carry — not five synonyms for "hit."
- Goal: players **argue creatively** what *Shelter the Ember* means this scene.

---

## Procedure (canonical — full rules; not all on card)

### Determine your Vow

When you **Enter** a **Scene**, roll **2d6**. Place one die on a **Verb** and one on a **Noun**. Your **Vow** is that phrase (*Verb the Noun*). On **6**, choose any word in that list.

### Priority

It is your priority above all else in this **Scene**.

### Fulfill your Vow

Once per **Scene**, if the GM agrees that your **Action** fulfills your **Vow**, add both dice from this card to **Boost** the roll, then remove them.

Defensive vows naturally pair with **Bulwark** / **[Resolve]** cards in combat — no extra rule required on the Oath card.

### Break your Vow (replaces old Defiance shuffle)

When you **Enter** a **Scene**, *before* rolling, you may **Break** your **Vow** — narrate turning from it.

- **Discard** your hand, **Draw** that many (hand cleanse — rare debuff/bane relief path).
- You do **not** roll a **Vow** this scene.
- Your Oath card **stays in the Active area** — no shuffle into the deck.

#### Break — open tuning (pick one after playtest)

| Option | Extra cost | Feel |
|---|---|---|
| **A — Free** | None beyond skipping Vow | Generous; enables big narrative pivots |
| **B — Vow debt** | Cannot **Fulfill** next scene | Soft cooldown |
| **C — Remorse chip** | GM places 1 Remorse; clear via hard narrative act or **Cleanse** | Fiction-forward |
| **D — Stain bane** | Shuffle **Stain** (single-scene bane, auto-clears at scene end) | Mechanical bite without losing Oath |

**Recommendation:** **A** for first playtest; add **B** if Break dominates.

---

## Oath pool (current)

| Oath | Subtitle | Sample Vow |
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
- Scene **Charge** and **Stand** terminology — superseded by **Vow** (June 2026).
- D&D-subtype names (Devotion / Vengeance / Crown) — replaced with lateral titles.

---

*Classes → `design/classes.md` · inventory → `card-inventory.md`*
