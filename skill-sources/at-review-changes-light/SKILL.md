---
name: at-review-changes-light
description: Fast, minimal review of pending card change requests in Instinct RPG. Use this skill whenever the user wants to quickly process change requests flagged in the card viewer app. Triggers on phrases like "review pending changes," "light review," "quick change review," "apply flagged changes," "make card changes," "pending toggles," or "let's knock out the change requests." Always prefer this skill for speed-focused sessions where the user just wants to see and approve changes with minimal friction.
---

# At Review Changes — Light

Fast-mode review. No suggestions, no visualization, no extra commentary — just facts and action.

---

## Step 1: Fetch All Pending Comments

Call `list_table_rows` on the **comments table** (`table_id: 1014004`, `size: 200`).

Filter to rows where `Change_Request.value === 'pending'`. Discard any rows with an empty `Card_Key`.

Group the results by `Card_Key`. Each group = one card to review.

---

## Step 2: Fetch Current Card Text for Each Card

For each unique `Card_Key`, call `list_table_rows` on the **cards table** (`table_id: 911939`, `search: <Card_Name>`).

Match the result on `Card_Key` (exact). Grab the `HTML` field and extract the visible text — strip all tags, keep just enough context for the change to make sense (Effect, Crit/Strong Roll text, failure line). You don't need the full card, just the parts the comment is likely referring to.

---

## Step 3: Present a Review Table

Show a single numbered table with all pending changes at once:

| # | Card | Relevant Current Text | Requested Change(s) |
|---|------|-----------------------|---------------------|
| 1 | Card Name | ...current effect / crit text... | • Comment body |
| 2 | Card Name | ...current text... | • Comment 1<br>• Comment 2 |

- If a card has multiple pending comments, list them as bullets in the Requested Change(s) cell — do not split into separate rows.
- Keep all three text columns terse. No interpretation or design notes.

Then say exactly: **"Approve all, or let me know which rows to adjust."**

---

## Step 4: Apply Changes — No Further Confirmation Needed

When the user responds:

- **"Approve all"** (or equivalent) → apply every change as written, for all rows.
- **Specific row instructions** (e.g. "Row 2: do X instead") → apply their exact wording for that row; apply everything else as-is.

For each card being changed, **in one pass**:

1. Construct the updated HTML — apply the requested text change to the current HTML from Baserow. Preserve all existing structure, classes, and styling. Change only the specific text called out.
2. `update_row(table_id=911939, row_id=<card row id>, fields={HTML: <new full HTML>})`
3. For each comment that was applied: `update_row(table_id=1014004, row_id=<comment row id>, fields={Change_Request: null})`

Do steps 2 and 3 for all cards before reporting back. Then give a brief confirmation of what was changed (one line per card).
