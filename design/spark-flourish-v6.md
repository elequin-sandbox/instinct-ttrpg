# Spark / Flourish v6 — attempt cards + minimal Flourish box

*July 2026 playtest direction — locked by Nathan after Discord thread + Squircle poll (left card won).*
*Proof: `flourish-v6-sample-proof.html` · builder: `scripts/build_flourish_v6_samples.py`*

---

## Design goals (why this pass exists)

1. **Combat stays binary Offense/Defense** — players declare before rolling. Splitting dice across
   pools is **not** a default action; only specific cards/Flourishes may dip across categories.
2. **Ability cards no longer guarantee outcomes** — the body describes the **attempt** only. The GM
   and scene frame what “success” looks like; in Deadly Contests the attempt feeds the normal roll
   like any other Action.
3. **Flourishes are the card’s mechanical signature** — earned on natural **6**s, spent *instead of*
   rolling the bonus die for a **guaranteed** category effect (remove dice / help ally / recover).
4. **Global category read, not card jargon** — three shapes + three keywords everywhere:
   - 🔺 red triangle — **Advance** (progress the objective / opposing pool)
   - 🟦 blue square — **Defend** (protect ally / shed threat)
   - 🟢 green dot — **Restore** (recover Resolve or hope)
5. **Content volume matters** — poll favored the **lighter** card: no flavor under title, no Effect
   label, Flourish box with **icons + keywords only** (no per-line narrative gloss). Fiction lives
   in how the player describes the attempt and justifies the Flourish at the table.

---

## Card body anatomy (v6 content — chrome unchanged)

| Zone | Rule |
|---|---|
| **Title + caps** | Unchanged — Ability / Act|React, class idtag, tier. |
| **Flavor** | **Omit** on v6 samples (poll winner). Optional in future if playtest asks for it. |
| **Attempt** | One paragraph: *Perform a **[Skill]** check to [try X]* — no “On success…” clause. |
| **Flourish** | Beige dotted box, **Flourish** label. Max **2** lines. Each line: cost pips + shape(s) + **Advance** / **Defend** / **Restore** (combo = `Defend + Advance`). **No** invite sentences under the keywords. |

**Not on v6 cards:** Effect label, Crit-count keyword lines (Rattled 2, etc.), stacked choose-one
forks in the base attempt, unit-linked condition tracking.

---

## Spend procedure (table)

1. Build pool, roll, remove 1s.
2. For each natural **6**, choose **before** rolling its bonus die:
   - **Explode** — roll the bonus die (classic Crit fun; GM may gain Toll on 1s), or
   - **Flourish** — spend the Crit on one printed Flourish line on the played card (guaranteed
     category effect; narrate how it fits — GM agrees it fits the scene, same social contract as
     Instinct/Flaw picks).
3. Apply Flourish by **shape category** only — the printed keyword is a readable label, not a new
   rules term to memorize.

---

## Language principles

- **Attempt verbs** use existing skills (**Deception**, **Athletics**, **Performance**, …) and
  table verbs (**Strike**, **Move**) — not new subsystem words like Protect 1 or Stagger 1.
- **Flourish combos** use `+` between global keywords when a line costs 2 Crits and spans two
  categories (e.g. `Defend + Advance`).
- **Out of combat** — same attempt line; GM frames a Contest or solo check. Flourishes still key off
  fiction fit.
- **Tactician classes** (Fighter, Bard, Ranger, Rogue) may get more cross-category Flourish lines;
  Paladin/Barbarian/Warlock keep class-owned narrative on attempts, same global Flourish keywords.

---

## Open playtest questions

- Is GM “must fit the scene” gating on Flourish too punitive vs. Aid’s always-correct social loop?
- Sweet spot for invite text: poll rejected heavy Spark invites; retest micro-hints vs. none.
- Spend icon: orange **6** on proof cards is legacy visual — production should use **Spark token**
  (see Spark Lab pay-icon tab), not “spend the die face.”

---

## Related doctrine

- Mechanic truth: `core-rules.md` §5 (Crit / Flourish)
- Visual gospel: `card-anatomy.md` §4 (Flourish colorings — v6 uses shape icons + global keywords)
- Wording: `writing-conventions.md` §3 (attempt setup, Flourish lines)
- Agent rule: `.cursor/rules/instinct-spark-flourish-v6.mdc`
