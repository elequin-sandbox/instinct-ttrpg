# Paste this into your GLOBAL CLAUDE.md

Your global file lives at:
`C:\Users\Natha\AppData\Roaming\Claude\local-agent-mode-sessions\...\local_<id>\.claude\CLAUDE.md`

I can't write there from a session (it's an app-internal path), so replace its contents with the
block below. It keeps only what is **universally true across all your projects** — the skill
update workflow — and adds the read-only-skills rule. Everything Instinct-specific now lives in
the project CLAUDE.md instead.

---

```markdown
# Global instructions

## Updating or creating skills
Installed skills are read-only mid-session. Never edit them in place and never write to the
installed skills directory directly. To change a skill:

1. Copy the skill to `/tmp/<name>`, make edits there.
2. From `/mnt/skills/examples/skill-creator/scripts/`, run:
   `python -m scripts.package_skill /tmp/<name> /mnt/user-data/outputs`
3. Present the resulting `.skill` file so I can install it via Settings → Capabilities.

If a project keeps a git-tracked mirror of its skills (e.g. a `skill-sources/` folder), make
sure that mirror ends up matching the newly packaged skill — one skill, one home, no duplicates.
```
