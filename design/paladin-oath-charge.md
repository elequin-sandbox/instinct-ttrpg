# Paladin — Oath & Scene Charge (design draft)

> **Status:** draft — June 28 2026. Replaces **Conviction · Defiance** and the GM-awarded story-Oath model for the Paladin **core** loop. Story-level oath-break tokens may still exist at the table; this doc is the **class mechanic**.
>
> **Sibling docs:** `design/classes.md` · `design/card-anatomy.md` · `design/core-rules.md`

---

## One-line identity (updated)

**Paladin:** Oath-bound defender who rolls a fresh **Charge** each scene and spends it to stand for something — Resolve specialist via **Bulwark**.

**Emotional core:** *Righteous — I know what I'm for this scene, and when it matters, I put everything behind it.*

---

## Character creation — pick your Oath

Mirrors the Warlock **Patron** pick:

1. Player receives the pool of Oath Core cards (currently 3 prototypes).
2. Chooses **one** at character creation.
3. That card lives in the **Active area** for the whole campaign (never shuffled into the deck).

**Core auto-cards:** Loadout · Bulwark · Build Your Deck · **+ 1 chosen Oath**.

---

## Oath card anatomy

Each Oath card has two indexed word lists and one shared procedure (printed on every Oath):

| Zone | Content |
|---|---|
| **Verbs** | 6 verbs, d6-indexed (1–5 + ★ Choose on 6) |
| **Nouns** | 6 nouns, d6-indexed (1–5 + ★ Choose on 6) |
| **Set Your Charge** | Scene-start procedure |
| **Fulfill Your Charge** | Once-per-scene payoff |

### Term: **Charge**

The scene phrase formed from one **Verb** + one **Noun** — e.g. *Protect the Innocent*, *Hunt the Betrayer*, *Serve the Realm*.

Non-religious, table-facing. Avoid "prayer" on cards.

---

## Procedure (canonical — must match every Oath card)

### Set Your Charge (scene start)

When you **Enter** a **Scene**, roll **2d6**. Place one die on a **Verb** and one on a **Noun**. Read the matching words as your scene **Charge** — your priority above all else this **Scene**. Leave both dice on the card.

On **6**, choose any word in that list (★ Choose).

### Fulfill Your Charge (once per scene)

Once per **Scene**, when the GM agrees your **Action** fulfills your **Charge**, add **both dice** from the card to that roll, then remove them. Your **Charge** is spent until the next **Scene**.

*(Dice on the card = Charge is live and unpaid. Empty card = Charge spent or not yet set.)*

---

## Design pivots under consideration

These are **alternatives** to the baseline (GM-gated double-dice → effective **[Boost 2]**). Pick one direction after playtest.

| Pivot | Change | Pros | Cons |
|---|---|---|---|
| **A — Baseline (Annie's pitch)** | Add both d6 to the roll when GM agrees | Physical, memorable, variance 2–12 | Can feel swingy; GM gate every time |
| **B — Resolve gift** | On fulfill: add dice to roll **or** convert them to **[Resolve]** for an ally (player chooses before rolling) | Ties to Bulwark / protector identity | Less explosive moment |
| **C — Partial fulfill** | Strong GM yes = both dice; "close enough" = one die only | Softer gate, less all-or-nothing | More GM negotiation |
| **D — Ally echo** | On fulfill: you add both dice; one adjacent ally gains **[Boost 1]** on the same **Action** | Party-facing, less self-centralizing | Complexity on multi-target actions |
| **E — Unused Charge tax** | If both dice still on card at **Scene** end, you start next scene **Rattled** (narrative) or discard 1 card | Incentivizes using it | Punitive; may force bad plays |
| **F — Enter mulligan** | After rolling Charge, once per scene you may reroll **one** die before acting | Fixes bad combos without killing randomness | Extra step at scene open |

**Recommendation for first playtest:** **A** (baseline) with **F** (one die reroll at Enter) as an optional table rule if phrases misfire.

---

## Oath prototypes (mock set)

| Oath | Subtitle | Verb flavor | Noun flavor |
|---|---|---|---|
| **Oath of Devotion** | The good is not safe. You stand anyway. | Protect, Shield, Uphold, Shelter, Answer, Guard | Innocent, Vow, Light, Weak, Truth, Sacred |
| **Oath of Vengeance** | Someone will answer for what was done. | Hunt, Break, Punish, Avenge, Expose, End | Guilty, Betrayer, Debt, Wrath, Wrong, Traitor |
| **Oath of the Crown** | The realm does not hold itself. | Serve, Keep, Hold, Lead, Stand, Guard | Realm, Crown, Law, Banner, Gate, People |

**Visual proof:** [`paladin-oath-proof.html`](../paladin-oath-proof.html)

---

## Retired

- **Conviction · Defiance** — archived; superseded by Oath pick + Scene Charge loop.
- GM-awarded story Oath card in Loadout / Build Your Deck — replaced by player-chosen Oath at creation.

---

*Classes → `design/classes.md` · inventory → `card-inventory.md`*
