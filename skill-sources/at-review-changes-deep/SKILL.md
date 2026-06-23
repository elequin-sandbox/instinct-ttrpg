---
name: at-review-changes-deep
description: Deep, collaborative review of pending card change requests in Instinct RPG. Use this skill when the user wants to work through change requests one-by-one with full card visualization and game design iteration. Triggers on phrases like "deep review," "let's work through the changes," "design review," "go through each change together," "review changes with me," or any time the user wants to see the card rendered and iterate on wording before committing. Always prefer this skill when the user wants to think through changes rather than just approve them.
---

# At Review Changes — Deep

Collaborative, card-by-card design review with full visualization. One card at a time, iterate until approved, then commit and move on.

---

## Step 1: Fetch All Pending Comments

Call `list_table_rows` on the **comments table** (`table_id: 1014004`, `size: 200`).

Filter to rows where `Change_Request.value === 'pending'`. Discard any rows with an empty `Card_Key`.

Group by `Card_Key`. Each group = one card to review.

---

## Step 2: Announce the Queue

Before starting, tell the user:

- How many **cards** have pending changes (e.g. "3 cards to review")
- Show a simple text progress bar: `Progress: [░░░░░░░░░░] 0 / 3`

Use block characters: filled = `█`, empty = `░`. 10 segments total, proportional to progress.

---

## Step 3: For Each Card (Loop)

Work through each card in order. For each one:

### 3a. Render the Card

Fetch the current card HTML from the cards table:
`list_table_rows(table_id=911939, search=<Card_Name>)` — match on `Card_Key`.

Use `show_widget` to render the card HTML inline. The HTML stored in Baserow is a complete, self-contained card element — wrap it in a minimal shell if needed:

```html
<style>
  body { background: #1a1a1a; display: flex; justify-content: center; padding: 24px; }
</style>
<div id="card-mount">
  <!-- paste the card's HTML here -->
</div>
```

### 3b. Show the Pending Comments

Directly below the rendered card (not inside the widget), show all pending comments for this card as a quoted block:

> **Requested change(s):**
> • [Commenter name, date]: "comment body"
> • [Commenter name, date]: "comment body"

### 3c. Iterate as a Game Designer

Work with the user to refine the change. You are a collaborator, not an approver — discuss phrasing, mechanical implications, connotation. Re-render the card with proposed new text using `show_widget` as many times as needed during iteration.

Stay in this loop until the user explicitly approves (words like "approve," "looks good," "ship it," "yes," "that's it").

### 3d. Apply and Clear

When the user approves, in one pass:

1. Construct the final updated HTML — apply all agreed-upon changes to the full current card HTML. Preserve all structure, classes, and styling.
2. `update_row(table_id=911939, row_id=<card row id>, fields={HTML: <new full HTML>})`
3. For every pending comment on this card: `update_row(table_id=1014004, row_id=<comment row id>, fields={Change_Request: null})`

Confirm with one line: e.g. "✓ Sneak Attack updated and change request cleared."

---

## Step 4: Update Progress Bar and Continue

After each card is committed, update the progress bar:

`Progress: [███░░░░░░░] 1 / 3`

Then immediately move to the next card (Step 3). No extra prompting needed — just start the next one.

When all cards are done:

`Progress: [██████████] 3 / 3 — all changes applied! 🎉`
