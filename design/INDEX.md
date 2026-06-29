# Instinct RPG — Doctrine Index (READ FIRST)

> **This is the manifest.** It is the single list of living-doctrine files for Instinct RPG. Both the
> project `CLAUDE.md` (always loaded) and the `at-design-system` skill (auto-triggered) point here, so
> every session has two independent paths to find current truth. `skill-audit.py` verifies this list
> matches the files actually present — if they drift, the audit fails.

## Session-start protocol

At the start of **any** Instinct RPG work — designing or reworking cards, answering a rules question,
or writing a player/GM asset — **read the relevant files below before responding.** They are the
current truth; never answer from memory or from old HTML/notes. They are cheap to read in full.

| Read this | When |
|---|---|
| **`core-rules.md`** | Any question about how the game *plays* — checks, dice, Toll, Resolve, Threat, Contests, scenes, character creation, keyword *meanings*. Always read for rules-compliance checks and any player/GM-facing asset. |
| **`card-anatomy.md`** | Any card visual/structure work — types, colors, ornaments, per-type body anatomy, and the **keyword formatting gospel** (Impact pills / Index chips / Narrative bold + the canonical pill colors). |
| **`writing-conventions.md`** | Writing or reviewing any card text — formatting tiers, voice, section names, the forbidden-terms list, and the pre-push **Term Audit**. |
| **`classes.md`** | Any class work — identity, term/mechanic ownership, what's locked, what's open (Paladin Oath/Charge, Cleric/Bard post-Bolstered, etc.). |
| **`paladin-oath-charge.md`** | Paladin Oath pick + Scene **Vow** mechanic — draft/prototype detail. |
| **`../card-inventory.md`** | What cards exist and what's pushed to Baserow (live production tally). |

## What is NOT doctrine

- **Procedures/workflows** (how to run a design session, push to Baserow, render a card, review
  changes) live in the **skills** (`at-design-session`, `at-baserow-push`, `at-card-renderer`,
  `at-review-changes-*`). Skills point back here for facts.
- **Deprecated / future-scoped ideas** live in the **`at-design-archive`** skill — never current truth.

## Keeping this current

Whenever a rule, card, term, or convention changes mid-session, the change is written to the relevant
file here immediately (no reinstall needed — these are plain repo files). At session end,
`at-session-close` commits them and repackages any skill that actually changed. If you add a new
doctrine file, add it to this table **and** to `CLAUDE.md`'s read list, or the audit will flag it.
