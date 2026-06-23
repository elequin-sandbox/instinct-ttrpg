---
name: at-card-edit
description: Lightweight card edit workflow for Instinct RPG. Use when making minor text or language changes to an existing card that do NOT change how the card functions mechanically. Triggers on phrases like "fix the wording on X," "tweak the flavor text," "update the tag reference," "clean up the text," "minor edit to," or any session where the change is presentational rather than mechanical. Do NOT use when cost, trigger, effect, or card type changes — use at-card-rework instead.
---

# Instinct RPG — Card Edit

Use for **lightweight text changes** that don't alter how a card plays. No version archiving required.

---

## Edit vs. Rework Decision

**Use Edit when the change is:**
- Fixing a typo or grammatical error
- Rewording flavor text (no mechanical change)
- Clarifying phrasing without changing meaning
- Updating a tag name to match a renamed mechanic
- Renaming the card with no function change
- Adjusting formatting or layout within the HTML

**Use `at-card-rework` instead when:**
- Card cost changes
- Trigger condition changes
- Effect text changes in a way that alters what the card does
- Card type changes (Act → React, etc.)
- Tags added or removed that affect gameplay
- Any change you'd need to playtest

**When in doubt:** ask "Would a player at the table notice a difference?" If yes → rework.

---

## Fields That Can Change in an Edit

| Field | Notes |
|---|---|
| `HTML` | Almost always changes — full re-render required |
| `Name` | Only if correcting spelling/formatting; update `Card_Key` too if slug changes |
| `Card_Key` | Only if Name changes; use hyphenated-lowercase-type format |

`Ruleset` and `Status` should almost never change in an edit.

---

## Workflow

```
1. Identify the card:
   → list_table_rows(table_id=911939, search="Card Display Name")
   → Confirm you have the right row — check Name and Card_Key
   → Note the row `id`

2. Make the text change:
   → Apply the edit to the card object
   → Re-render the full HTML via renderCard() (see at-card-renderer)
   → HTML field ALWAYS gets a full replacement — never partial

3. Update Baserow:
   → update_rows(
       table_id=911939,
       row_id=<id>,
       fields={
         HTML: "<complete new rendered HTML>"
         // add Name and/or Card_Key here ONLY if those changed
       }
     )

4. Verify:
   → list_table_rows(table_id=911939, search="Card Display Name")
   → Confirm the HTML field reflects the change
   → Render a quick preview if the session has a renderer available
```

---

## Table Reference

| Item | Value |
|---|---|
| Cards table ID | `911939` |
| Versions table ID | `1014012` (NOT used in edits) |
| MCP tool: read | `list_table_rows` |
| MCP tool: write | `update_rows` |

---

## Edit Checklist

- [ ] Confirmed this is an edit, not a rework (no mechanical change)
- [ ] Located the correct row via `list_table_rows` and noted row `id`
- [ ] Re-rendered complete card HTML (no partial HTML)
- [ ] Called `update_rows` with full `HTML` value
- [ ] Verified updated row via `list_table_rows`
- [ ] Did NOT touch the Versions table
- [ ] Did NOT change `Status` or `Ruleset` unless explicitly asked
