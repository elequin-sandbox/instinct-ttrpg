---
name: at-session-close
description: Instinct RPG end-of-session self-audit and doctrine-update workflow. Run this whenever an Instinct RPG / Act Tactics design or rules session is wrapping up, OR any time the session changed game truth (a rule, mechanic, card, term, class identity, asset, rhetoric, or visual/language convention). Triggers on phrases like "close out," "run the audit," "wrap up," "that's all," "we're done," "end of session," "did anything change," or "update the doctrine." Detects what changed, updates the canonical design/ file, repackages only any skill that actually changed, verifies no drift, and confirms. Annie should never have to remember to update doctrine manually.
---

# Instinct RPG — Session Close & Self-Audit

Your job at session end is to make sure the doctrine the NEXT session loads is 100% current — without
Annie having to remember anything. **The living doctrine is the `design/` files** (single source of
truth); skills are thin procedure+pointer wrappers around them.

Run when Annie signals wrap-up ("done", "that's all", "close out", "run the audit") or proactively
whenever the session changed game truth.

## Where each kind of change goes (one fact, one home)

| If this changed...                                                | Update this |
|-------------------------------------------------------------------|-------------|
| How the game plays: rules, combat, checks, Toll, Resolve, Threat, scenes, character creation | `design/core-rules.md` |
| Card wording, formatting, capitalization, conventions, forbidden terms | `design/writing-conventions.md` |
| Card visual anatomy, types, colors, the keyword formatting gospel  | `design/card-anatomy.md` |
| Class identity, term/mechanic ownership, locked/open items         | `design/classes.md` |
| Which cards exist / are pushed to Baserow                          | `card-inventory.md` (repo root) |
| A cut/deprecated mechanic or future-scoped idea                    | `at-design-archive` skill (repackage) |
| A workflow/procedure, or the renderer code                         | the relevant skill (repackage) |

If a change seems to belong in two places, it belongs in one — pick the primary home and
cross-reference. Never duplicate the text.

## ⛔ NEVER touch git

**Never run `git add`, `git commit`, `git push`, or any other git command — ever.** Annie pushes
all changes herself from Sourcetree. Your job is to edit the files; her job is to version them.
Running git commands causes lock file conflicts and broken state. There is no exception to this rule.

## Workflow

1. **Recall the diff.** Review the whole session and list every concrete change to game truth. If
   nothing changed, say so and skip to step 4.

2. **Confirm with Annie.** Show the change list and the file each maps to. A short checklist, not an
   essay. Let her correct before editing.

3. **Edit the doctrine.** For each confirmed change, edit the right `design/` file (or
   `card-inventory.md`). These are plain repo files — **just edit and save, no reinstall.** Make the
   smallest correct edit. Keep `design/INDEX.md` in sync if you added a new doctrine file.

4. **Repackage ONLY skills that changed.** Most sessions change only `design/` files → **no
   repackage needed.** Repackage only if you edited a skill (a procedure, the renderer code, or the
   archive): copy `skill-sources/<name>` → `/tmp/<name>`, run
   `python -m scripts.package_skill /tmp/<name> /mnt/user-data/outputs`, and present the `.skill` with
   `present_files` for Annie to one-click install (Settings → Capabilities). Keep `skill-sources/`
   matching what you packaged.

5. **Verify.** Run `python skill-audit.py` from the repo root. Resolve issues until clean (a
   "needs reinstall" drift warning is expected until Annie installs a freshly repackaged skill).

6. **Close the loop.** Confirm in one or two lines: what changed, which file(s) hold it, any `.skill`
   needing install, and that the audit is clean. Remind Annie to push from Sourcetree.

## Honesty note
Routine game-truth changes are cheap `design/` edits with **no reinstall** — that is the whole point
of the architecture. The one-click reinstall only resurfaces when a skill (procedure/code/archive)
itself changed. Never ask Annie to hand-edit doctrine or to remember something is stale.
