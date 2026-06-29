# Paladin — Oath & Scene Vow (design draft)

> **Status:** draft — June 2026. Replaces **Conviction · Defiance** for the Paladin **core** loop.
> The **Oath** card is your permanent creation pick; your **Vow** is the scene phrase rolled on it.
>
> **Sibling docs:** `design/classes.md` · `design/card-anatomy.md` · `design/core-rules.md`

---

## Terminology

| Term | Scope | Notes |
|---|---|---|
| **Oath** | Campaign — the Core card you pick at creation | Stays in Active area; defines your word pools. Header tags: **Core** + **Oath**; ribbon reads *Oath of …* |
| **Vow** | Scene — Verb + *the* + Noun phrase | Changes every scene. Colloquial: *"What's your vow this scene?"* |
| **Fulfill** | Once per scene | GM agrees your **Action** fulfills your **Vow** → add both dice to **Boost 2** on that roll |
| **Break** | Defy your **Vow** mid-scene | Describe defiance; place dice into **Resolve**; GM gains **Toll 2** (must use against you this scene) |

*Rejected:* Charge (too generic), Mandate (clunky), Stand (June 2026 interim — replaced by **Vow**). Old Break (hand mulligan at Enter) — replaced June 2026 v6.

**Card vs table:** Oath cards show the minimum text; GM / creation supplement explains placing dice on Verb + Noun lists and reading the phrase aloud.

---

## Character creation

Mirrors Warlock **Patron** pick:

1. Pool of Oath Core cards (5 prototypes + blank template for homebrew).
2. Pick **one** — lives in **Active area** permanently.
3. Auto cores: Loadout · Bulwark · Build Your Deck.

**Blank template:** `oath-template-paladin-core` — fill title, subtitle, verbs, nouns; procedure is pre-printed. Word slots use dashed **write-in lines** (3×2 grid, pen-sized).

---

## Oath card anatomy (on-card text)

| Zone | Content |
|---|---|
| **Header caps** | **Core** · **Oath** (sorting) |
| **Ribbon title** | **Oath of** prefix pill + card name (e.g. *Oath of The Open Hand*) |
| **Scene start line** | At **Scene start**: roll 2d6 to determine your new **Vow**: |
| **Word stack** | L→R mad lib — dice in top slots; verb column left, noun column right; gold row indices |
| **Fulfill** | Once per **Scene** … add these dice → **Boost 2** |
| **Break Your Oath:** | Defiance → dice to **Resolve**; GM **Toll 2** vs you this scene |

### Word-pool design rules

- Prefer **lateral nouns** (Frail, Threshold, Silence) over literal class-fiction (Innocent, Guilty, Realm).
- Verbs should span modes: protect *and* witness *and* carry — not five synonyms for "hit."
- Goal: players **argue creatively** what *Shelter the Ember* means this scene.

---

## Procedure (canonical — full rules; not all on card)

### Determine your Vow

At **Scene start**, roll **2d6**. Place one die on a **Verb** and one on a **Noun** (same column on the card). Your **Vow** is that phrase (*Verb the Noun*).

### Fulfill your Vow

Once per **Scene**, if any **Action** you are taking fulfills your **Vow** and the GM agrees, add both dice to give that roll **Boost 2**, then remove them.

### Break Your Oath

Describe how you are defying your **Vow**, then place these dice into your **Resolve**. The GM gains **Toll 2** and must use it against you this scene.

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
- Break-at-Enter hand mulligan — superseded by **Break Your Oath** (Resolve + GM Toll 2).

---

*Classes → `design/classes.md` · inventory → `card-inventory.md`*
