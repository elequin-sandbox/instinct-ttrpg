---
name: at-baserow-push
description: Act Tactics Baserow database workflow. Use this skill any time a session needs to add cards to Baserow, save cards to the database, push cards to the viewer, update an existing card in Baserow, query what cards exist, or sync card data. Triggers on phrases like "add to Baserow," "save to Baserow," "push to the viewer," "update the card in the database," "check what's in Baserow," or "sync these cards." Contains table ID, MCP tool names, HTML field rules, create and update workflows, batch add pattern, and viewer regeneration script.
---

# Act Tactics — Baserow Push

Complete workflow for the Act Tactics card data layer. Use whenever a session adds, updates, queries, or syncs cards in Baserow.

---

## Core Facts

| Item | Value |
|---|---|
| **Table ID** | `911939` |
| **Live viewer** | `Nathan-Elequin.github.io/act-tactics` |
| **GitHub repo** | `Nathan-Elequin/act-tactics` |
| **index.html** | Single source of truth — all edits happen here |

---

## MCP Tool Reference

| Tool | Use for |
|---|---|
| `list_table_rows` | Browse existing cards; confirm before updating |
| `create_row` | Add a brand-new card |
| `update_row` | Edit an existing card (requires row ID from `list_table_rows`) |
| `delete_table_row` | Remove a card — confirm with Annie first |

**Search pattern:** `list_table_rows` with a name filter returns rows reliably by display name. Always call this before `update_row` to get the correct row ID.

---

## HTML Field — Key Rule

The Baserow table stores **complete rendered card HTML markup** in the HTML field. **Full replacement required on every edit** — never partial updates.

**Card key format:** `card-name-type` — hyphenated lowercase + type suffix.
- `lucky-break-boon`, `ward-act`, `lay-hands-act`, `rage-condition`

---

## Workflow: Add a New Card

```
1. Design card object (see at-design-session for schema)
2. Render via renderCard() to get HTML string (see at-card-renderer)
3. Confirm card doesn't already exist:
   → list_table_rows(table_id=911939, search="Card Name")
4. If not found:
   → create_row(table_id=911939, fields={
       Name: "Card Display Name",
       HTML: "<complete rendered card HTML>",
       ... [confirm other field names from list_table_rows response on first use]
     })
5. Verify by calling list_table_rows and confirming new row appears
```

---

## Workflow: Update an Existing Card

```
1. Get the row ID:
   → list_table_rows(table_id=911939, search="Card Display Name")
   → Note the `id` field from the matching row
2. Prepare the complete new HTML (never partial)
3. Update:
   → update_row(table_id=911939, row_id=<id>, fields={
       HTML: "<complete new rendered card HTML>"
     })
4. Verify by calling list_table_rows again
```

---

## Workflow: Batch Add (Multiple Cards)

```
1. Render all cards to HTML strings first (one pass)
2. Confirm none already exist (one list_table_rows call with class filter)
3. Add cards sequentially with create_row — one row per call
4. Final list_table_rows to confirm the full set
```

---

## Field Schema Note

Exact field names beyond `Name` and `HTML` are not fully documented here. On first use in a session, call `list_table_rows` with `table_id=911939` and read the field keys from the response. Do not guess field names.

---

## Viewer Regeneration Script

After updating Baserow, regenerate and push `index.html` to GitHub:

```python
import re
with open('act-tactics-cards.js') as f: src = f.read()
src = src.replace('export const TAG_MAP', 'const TAG_MAP')
src = src.replace('export const CARDS', 'const CARDS')
src = src.replace('export function parseMarkup', 'function parseMarkup')
src = src.replace('export function resolveTagBase', 'function resolveTagBase')
start = src.index('const TAG_MAP')
end = src.rindex('];') + 2
embedded = src[start:end]
with open('act-tactics-viewer.html') as f: html = f.read()
with open('act-tactics-viewer.html', 'w') as f:
    f.write(re.sub(r'const TAG_MAP.*?\];', embedded, html, flags=re.DOTALL))
print("Done.")
```
