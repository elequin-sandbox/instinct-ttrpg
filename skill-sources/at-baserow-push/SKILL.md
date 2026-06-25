---
name: at-baserow-push
description: Act Tactics Baserow database workflow. Use this skill any time a session needs to add cards to Baserow, save cards to the database, push cards to the viewer, update an existing card in Baserow, query what cards exist, or sync card data. Triggers on phrases like "add to Baserow," "save to Baserow," "push to the viewer," "update the card in the database," "check what's in Baserow," "sync these cards," "sync my edits," "push my edits," or "update Baserow." Contains table ID, MCP tool names, HTML field rules, create and update workflows, batch add pattern, card-editor sync procedure, and viewer regeneration script.
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

## Workflow: Sync Card Editor Edits ("sync my edits" / "push my edits" / "update Baserow")

This is the Card Editor sync flow. Trigger whenever Annie says anything like "sync my edits," "push my edits," or "update Baserow."

```
1. FIND the edits file
   → Look in the repo root for card-edits*.json files
   → Use the most recently modified one (may be card-edits(1).json, card-edits(2).json, etc.)
   → Read it — if edits[] is empty, tell Annie and stop

2. FOR EACH edit in edits[]:

   If action == "update":
   a. Fetch current Baserow row by Card_Key:
      → list_table_rows(table_id=911939, search=Card_Key)
      → Note the row id
   b. Archive old version to Versions table (1014012):
      → create_row(table_id=1014012, fields={
          Card_Key, Card_Name: Name, HTML: <old HTML>, Change_Note, Date: today
        })
   c. Translate EffectText_Plain → card HTML body
      → Read design/card-anatomy.md for pill/chip/bold rules
      → Wrap in correct .cbody structure with .bf-body divs
      → Build full card HTML (hdr + cbody + flv + idtag)
   d. Push update:
      → update_row(table_id=911939, row_id=<id>, fields={
          Name, HTML: <new full HTML>, Last_Rework_Date: today,
          Class, Card_Type, Ruleset, Status
        })

   If action == "create":
   a. Confirm Card_Key doesn't already exist:
      → list_table_rows(table_id=911939, search=Card_Key)
   b. Generate full card HTML from plain fields
   c. create_row(table_id=911939, fields={...})

3. REGENERATE card-data.js
   → Fetch all Status=current rows from table 911939 (paginate if needed)
   → Write updated card-data.js to repo root
   → See at-session-close step 3b for extraction details

4. CLEAN UP the edits file graveyard
   → Delete ALL files matching card-edits*.json in the repo root
     (card-edits.json, card-edits(1).json, card-edits(2).json, etc.)
   → Write a fresh empty card-edits.json:
     {"timestamp": "", "edits": []}
   → This resets the queue — next Firefox download becomes card-edits(1).json again

5. CONFIRM
   → Tell Annie: how many cards updated/created, that card-data.js is refreshed,
     and that the edit queue is cleared
```

**Why the cleanup matters:** Firefox creates numbered duplicates on every download because it never overwrites. Without step 4, the repo fills with stale files and future syncs could read the wrong file. Always clean up after syncing.

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
