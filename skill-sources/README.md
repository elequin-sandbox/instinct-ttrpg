# skill-sources/ — Canonical skill mirror (SINGLE SOURCE OF TRUTH)

This folder is the **git-tracked backup and edit-staging area** for every Instinct RPG skill.

## Rules

1. **The installed skills (Settings → Capabilities) and these files must always match.**
   These folders are mirrored 1:1 from the live installed `at-*` skills.

2. **To change a skill, edit the file *here* first**, then repackage and reinstall.
   Never keep a second copy of a skill anywhere else in this repo — that is exactly the
   "silent divergence" failure we cleaned up. One skill = one home.

3. **Editing + packaging is automated.** The `at-session-close` skill (and the
   `skill-audit.py` script) handle detecting changes, updating the right file here,
   repackaging the `.skill`, and handing you a one-click install file. You should never
   have to hand-edit these or remember to update them.

4. **If a file here ever differs from the installed skill, the installed skill wins**
   (it is what Claude actually loads). Run `python skill-audit.py` to detect drift.

## What lives here

13 skills: at-baserow-push, at-boon-design, at-card-edit, at-card-language,
at-card-renderer, at-card-rework, at-class-quick-ref, at-core-rules, at-design-archive,
at-design-session, at-design-system, at-review-changes-deep, at-review-changes-light.

(Plus `at-session-close` once installed.)
