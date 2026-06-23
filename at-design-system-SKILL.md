---
name: at-design-system
description: Instinct RPG (fka Act Tactics) complete design system. Read this skill at the start of ANY session involving Instinct RPG — card design, writing, visual rendering, class mechanics, character creation, printing, or any game work. Triggers on any mention of "Instinct RPG," "Act Tactics," any card type name (Trait, Background, Bond, Flaw, Ancestry, Act, React, Core), any class name (Rogue, Warlock, Fighter, etc.), "Baserow," "card viewer," "print cards," "design a card," or any AT mechanical term (Boost, Hit Dice, Crit, Exposed, Rooted, Resolve, etc.). This is the authoritative source of truth — always consult before making recommendations, designing cards, or writing any game text.
---

# Instinct RPG (fka Act Tactics) — Design System

**Version:** June 2025, updated Playtest #1 · Supersedes all prior session artifacts where contradicted.

This skill is the ship's log. Claude reads it first, surfaces the current state, flags contradictions, and asks the captain before changing course.

---

## ★ SESSION STARTUP PROTOCOL

Do this every time this skill loads — without exception.

### Step 1 — Surface Current State
State aloud what this skill believes the current state is:
- How many cards exist and of what types (see `references/card-inventory.md`)
- What is and isn't yet in Baserow
- Any open items listed at the bottom of this file

### Step 2 — Check Baserow (if MCP available)
If the Baserow MCP tool is active, call `list_table_rows` on table `911939` with no filter and count rows. Compare against the inventory in `references/card-inventory.md`. Flag any discrepancy.

If Baserow MCP is not available, note that and proceed from the embedded inventory.

### Step 3 — Flag Contradictions
If the user's request contradicts anything in this skill, name the contradiction explicitly before proceeding:
> *"This would change [X]. Current log says [Y]. Should I update the protocol?"*

Do not silently proceed with a contradicting design.

### Step 4 — Confirm Before Building
Before rendering HTML, pushing to Baserow, or writing card text, confirm:
- What is being created
- Whether it already exists
- Whether it aligns with the locked principles in this skill

**Never consume tokens producing work the user didn't need or that duplicates what exists.**

---

## REFERENCE FILE INDEX

Read the relevant file(s) before working in that domain. Do not guess — load the reference.

| File | When to read |
|---|---|
| `references/card-types.md` | Any card design, visual rendering, print work |
| `references/writing-conventions.md` | Writing any card text, flavor, stems, or effects |
| `references/design-principles.md` | Evaluating new designs, checking alignment |
| `references/class-identity.md` | Designing class ability cards, checking class ownership |
| `references/card-inventory.md` | Checking what exists; confirming before creating |

**For gameplay mechanics questions** (how checks work, what Toll is, how Resolve works, combat rules, scene rules, conditions): load the **at-core-rules** skill. This skill covers card anatomy and design systems; at-core-rules covers how the game plays at the table.

**For deprecated or future-scope design ideas**: load **at-design-archive**. Never use at-design-archive as a source of truth for current rules or card design.

---

## OPEN ITEMS (as of June 2025, post-Playtest #1)

These are unresolved design items. Surface them at session start if relevant.

**From before Playtest #1:**
- [ ] **Baserow push pending** — All 66 character creation cards exist in the JSX artifact and print file but have NOT been pushed to Baserow table 911939 yet
- [ ] **Bond cards in viewer** — Bonds converted to new visual shell in artifacts but Baserow data not updated
- [ ] **card-design-guide.md outdated** — Does not reflect new card type system, header layout, or ornament dictionary
- [ ] **Vault card (Fighter)** — Created as tutorial example; decision pending: add to Baserow or keep tutorial-only
- [ ] **Flaw Dismiss mechanic** — "Cleanse" referenced in all Dismiss conditions but not yet formally defined in rules
- [ ] **Aura of Resolve rework** — Should key off Oath held, not action volume
- [ ] **Wizard not yet designed** — Deferred; Sundered consumption hooks needed
- [ ] **Bard Rally Token identity** — Needs further design; distinction from Lead mechanic unclear

**From Playtest #1 (June 4, 2025 — Jimmy, Ben, Jordan):**
- [ ] **Paladin identity redesign** — Guard is eliminated. Paladin was the "Proactive Guard specialist." Identity must be rethought. Leading direction: Resolve manipulation specialist. Block new Paladin card design until resolved.
- [ ] **React cards need restoration** — Starter decks were stripped of React cards for the playtest; this undercut a core game feel. Restore 2–3 React cards per class before next playtest.
- [ ] **Empty hand rule** — No rule exists for when a player exhausts their full hand. Design needed: Desperation Draw, GM Toll gain, or scene-end trigger. See Playtest #1 report.
- [ ] **Ancestry stem rewrites** — Dragonborn and other ancestry stems are too lore-specific. Rewrite toward relationship/social framing or PbtA-style descriptor lists.
- [ ] **Barbarian deck distribution** — Only 3 of 11 cards had unconditional strike effects. Add 2–3 no-precondition strike cards.
- [ ] **Foldable character name card** — Players need a name-tent + appearance reference at the table. Design before next playtest.
- [ ] **Condition reference card** — GM cheat sheet for condition keywords (Sunder, Expose, Rattle, etc.) with fallback mechanical readings.
- [ ] **Context tags on cards** — Consider adding ⚔️/🗣️/🔍 icons to indicate primary scene context (non-restrictive, just legibility).
- [ ] **Boon vs. Act naming collision** — "Boon" and "active" overlap phonetically. Consider rename or extreme visual differentiation.

**Post-Playtest #1 decisions (already resolved):**
- [x] **Guard eliminated** — Replaced by Resolve (temporary hit die layer at combat start). See `references/class-identity.md`.
- [x] **Strong Roll → Crit** — Canonical terminology change. "Strong Roll" is retired. Use "Crit" and "Boost" throughout.
- [x] **Health maximization at level 1** — Players start with all hit dice at maximum value. No rolling for level 1 health.
- [x] **Simultaneous damage model** — Enemies show their damage threat upfront when combat begins. Players choose to engage knowing the cost.
- [x] **Combat + social unified under Resolve** — Both scene types use the same resolution engine. Social combat uses a temporary Resolve pool; physical combat uses hit dice. Guard is dead.
- [x] **Bane passive debuff cut** — "While held, [negative effect]" language removed from all Flaw/Bane cards. Hand slot cost IS the consequence.

---

## ★ SESSION WRAP-UP PROTOCOL

Run this at the end of ANY session where design decisions were made, cards were locked, or mechanics changed. Also run if Nathan says "we made a lot of progress" or "let's wrap up."

### Step 1 — Identify What Changed
List every decision made this session that affects a skill file:
- New/changed terminology → `writing-conventions.md`
- New/changed design principles → `design-principles.md`
- Class identity changed, mechanic locked/removed → `class-identity.md` + `at-class-quick-ref/SKILL.md`
- New cards designed and approved → `card-inventory.md`
- TAG_MAP needs a new tag or removal → `at-card-renderer/SKILL.md`
- Card schema or checklist changed → `at-design-session/SKILL.md`
- New open items or resolved items → `at-design-system/SKILL.md` (Open Items section)

### Step 2 — Generate Updated Files
For each affected file, generate the updated version with a changelog entry at the bottom. Use the naming convention:
- `at-design-system-SKILL.md`
- `at-design-system-writing-conventions.md`
- `at-design-system-design-principles.md`
- `at-design-system-class-identity.md`
- `at-class-quick-ref-SKILL.md`
- `at-card-renderer-SKILL.md`
- `at-design-session-SKILL.md`

Present all updated files for download in a single `present_files` call.

### Step 3 — Prompt Nathan to Run the Update Script
Always end the session with this reminder:

> **Skill update ready.** Download the files above, then run `update-skills.ps1` (right-click → Run with PowerShell) to push them to Claude Desktop. Takes about 30 seconds.

**The script location:** Nathan has `update-skills.ps1` saved locally. It copies files from `Downloads\` into:
`C:\Users\Natha\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\447c8b33-f38d-421b-ba9c-599fd090d3ae\39bfeaf3-1023-4688-b031-b30adfeb20ee\skills\`

After running, Nathan must **restart Claude Desktop** for changes to take effect.

---

## SELF-UPDATE PROTOCOL

When a design decision changes or a new principle is established:

1. **Identify the affected section** — which reference file and which heading
2. **Draft the updated text** — write it out explicitly, showing old vs new
3. **Present to user for confirmation** — never update silently
4. **On approval:** Generate updated file(s) using the naming convention above and present for download
5. **Remind Nathan** to run `update-skills.ps1` and restart Claude Desktop

**What triggers an update:**
- A new card type or sub-type is introduced
- A visual spec changes (color, ornament, layout)
- A writing convention is explicitly revised
- A class identity mechanic is locked or changed
- A new card is designed and approved (update `card-inventory.md`)
- Any "this supersedes X" statement from the user

**Format for update notes** — add to the bottom of the affected reference file:
```
---
## Changelog
- [Month Year] — [What changed and why]
```
