# Instinct RPG — Project Instructions

Instinct RPG (formerly "Act Tactics" / AT) is a card-based tabletop RPG. This repo holds the
card-viewer web app, game documents, playtest notes, the **living design doctrine** (`design/`), and
the git-tracked mirror of the game's skills (`skill-sources/`). These rules apply to **every** session
in this project, without exception.

---

## 1. SESSION-START PROTOCOL — always read the doctrine first 🔒

At the start of ANY Instinct RPG work — designing/reworking cards, answering a rules question, or
writing a player/GM asset — **read the relevant doctrine files in `design/` BEFORE responding.** They
are the single source of current truth. Never answer from memory or from old HTML/notes.

**Start with `design/INDEX.md`** (the manifest), then read what the task needs:

- **`design/core-rules.md`** — how the game plays (checks, d6 dice, Toll, Resolve, Threat, Contests,
  scenes, character creation, keyword meanings).
- **`design/card-anatomy.md`** — card types, colors, ornaments, and the keyword **formatting gospel**
  (Impact pills / Index chips / Narrative bold).
- **`design/writing-conventions.md`** — wording, voice, section names, forbidden terms, Term Audit.
- **`design/classes.md`** — class identity, term/mechanic ownership, locked + open items.
- **`card-inventory.md`** — live tally of what exists / is pushed to Baserow.

This is guaranteed two ways: this file is loaded every session, and the `at-design-system` skill
auto-triggers on any Instinct term and routes to the same `design/INDEX.md`. If those two ever
disagree with the files present, `skill-audit.py` will flag it.

## 2. One fact, one home — doctrine lives in `design/`

- **`design/` is the single source of truth** for rules, card anatomy, wording, and class identity.
  Edit doctrine THERE — never restate a rule in a skill, an HTML doc, or a stray `.md`.
- **Skills are procedure + pointer, not doctrine.** Workflow skills (`at-design-session`,
  `at-card-renderer`, `at-baserow-push`, `at-review-changes-*`) describe *how* to work and point back
  to `design/` for facts. The doctrine skills (`at-core-rules`, `at-design-system`, `at-card-language`,
  `at-class-quick-ref`) are thin routers that auto-trigger and send you to `design/`.
- **`skill-sources/`** is the git-tracked mirror of the installed skills (see its README).
- Never create a second copy of any doctrine or skill elsewhere — that is the "silent divergence" we
  cleaned up.

## 3. Keep doctrine current AS THE GAME CHANGES (no manual nagging)

Whenever Annie states a change during a session — a rule, mechanic, card, term, class identity,
rhetoric/asset text, or visual/language convention — you OWN keeping it current:

1. Identify the home in `design/` (rules → `core-rules.md`; wording → `writing-conventions.md`;
   visuals/colors/anatomy → `card-anatomy.md`; class identity → `classes.md`; inventory →
   `card-inventory.md`).
2. **Edit that file immediately** — it's a plain repo file, so it just needs a save + commit. No
   reinstall, no waiting, and never ask Annie to remember to do it.
3. Note it in the running change log for the session-close audit.

Repackaging a skill is only needed when a *procedure or the renderer code* changes — rare. Routine
game-truth changes are cheap edits to `design/`.

## 4. End every session with a self-audit (`at-session-close`)

When Annie signals wrap-up ("done", "that's all", "closing out", "thanks, that's it") OR any time the
session changed game truth, proactively run the **`at-session-close`** skill. It reviews what changed,
updates the right `design/` file(s), commits, repackages any skill that actually changed (presenting
the `.skill` for one-click reinstall), and runs `skill-audit.py`. Annie can also trigger it by saying
"close out" or "run the audit".

## 5. Updating a skill — the mechanics (never edit installed skills directly)

Installed skills are read-only mid-session. To change one:

1. Edit `skill-sources/<name>` (or copy to `/tmp/<name>` and edit there).
2. From `/mnt/skills/examples/skill-creator/scripts/` (or wherever skill-creator lives), run:
   `python -m scripts.package_skill <path> /mnt/user-data/outputs`.
3. Present the resulting `.skill` so Annie installs it via Settings → Capabilities.
4. Ensure `skill-sources/<name>` matches the packaged version.

Never write directly to the installed skills directory.

## 6. Verify integrity

Run `python skill-audit.py` (repo root) before closing a session. It checks: drift between
`skill-sources/` and installed skills, folder structure, stray duplicate skill/doctrine copies, that
`design/INDEX.md` is wired into this file, and that the doctrine files the manifest lists actually
exist. Aim for 0 violations (a "needs reinstall" drift warning is expected until Annie installs a
freshly repackaged skill).

## 7. Git — direct to main (no PRs)

**`.cursor/rules/instinct-git.mdc`** is binding for this repo. After any coherent change (especially
the web app), **commit on `main` and `git push origin main`** without asking. No feature branches or
PRs unless Annie explicitly requests them. See that file for exclusions and safety rules.

---

## Repo orientation

- `design/` — **the living doctrine** (`INDEX.md`, `core-rules.md`, `card-anatomy.md`,
  `writing-conventions.md`, `classes.md`). Edit game truth here.
- `card-inventory.md` — living tally of which cards exist / are pushed to Baserow. Keep current.
- `index.html` + `config.js` + `local-cards.js` — the LIVE card-viewer app (deployed to GitHub Pages
  via `.github/workflows/deploy.yml`; the whole dir is published). Do not break these.
- `skill-sources/` — canonical mirror of the installed skills (see its README).
- `instinct-rpg-primer-updated.html`, `gm-guide-updated.html`, `instinct-rpg-quick-ref.html`,
  `completion-guide.html`, `*-draft.html` — game documents/deliverables.
- `Jun 20 *` — playtest notes & analysis.
- Baserow card data + viewer workflow: see the `at-baserow-push` skill.
