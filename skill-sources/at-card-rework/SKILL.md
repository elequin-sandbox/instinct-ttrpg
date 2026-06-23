---
name: at-card-rework
description: Major card rework workflow for Instinct RPG. Use when redesigning a card in a way that changes how it plays — cost, trigger, effect, card type, or tag changes. Triggers on phrases like "rework X card," "redesign this card," "mechanically change X," "overhaul the effect," "change the cost," "rewrite the trigger," or any session where the card's function is being meaningfully altered. Always archives the current version before touching the main card. Do NOT use for text-only tweaks — use at-card-edit instead.
---

# Instinct RPG — Card Rework

Use for **mechanical redesigns** — any change that alters how a card plays. Archives the current version before updating.

---

## Edit vs. Rework Decision

**Use Rework when:**
- Card cost changes (even by 1)
- Trigger condition changes
- Effect description changes in a way that alters what happens at the table
- Card type changes (Act → React, Condition, etc.)
- Tags added, removed, or changed in a way that affects gameplay
- Major structural change (adding/removing a Crit, Failure, Exchange, or Stack section)
- Any change you'd need to playtest

**Use `at-card-edit` instead when:**
- Fixing typos, grammar, or formatting
- Rewording for clarity without changing meaning
- Updating a tag name to match a rename
- Changing flavor text only

**Gray area:** If unsure, err toward rework — version history is cheap and easy to navigate.

---

## Table Reference

| Item | Value |
|---|---|
| Cards table ID | `911939` |
| Versions table ID | `1014012` |
| MCP: read rows | `list_table_rows` |
| MCP: create row | `create_rows` |
| MCP: update row | `update_rows` |

---

## Step-by-Step Workflow

### Step 1 — Read the current card

```
→ list_table_rows(table_id=911939, search="Card Display Name")
→ Capture ALL of the following from the response:
   - id          (row ID — needed for update_rows)
   - Name        (display name)
   - Card_Key    (slug, e.g. "ward-act")
   - HTML        (current full HTML — this is what you archive)
   - Ruleset     (note current value; update if it changes)
   - Status      (note current value; usually stays "current")
```

Do not proceed until you have the current HTML in hand.

### Step 2 — Agree on the Change_Note

Before archiving, confirm the reason for the rework in one concise line. This becomes the `Change_Note` in the version record. Examples:
- `"Cost reduced from 2 to 1, trigger tightened"`
- `"Effect redesigned — removed Exchange, added Stack 2"`
- `"Card type changed from Act to React"`

### Step 3 — Archive current version to Versions table

```
→ create_rows(
    table_id=1014012,
    fields={
      Card_Key:   "<card_key from step 1>",
      Card_Name:  "<Name from step 1>",
      HTML:       "<HTML from step 1 — exact, unmodified copy>",
      Change_Note: "<agreed reason from step 2>"
    }
  )

DO NOT pass Version_Date — it is auto-set by Baserow (created_on field).
```

**Verify the archive before proceeding:**
```
→ list_table_rows(table_id=1014012, search="<card_key>")
→ Confirm a new row exists with the correct Card_Key and Change_Note
→ Only continue to Step 4 after confirmation
```

### Step 4 — Design the new card

Apply the rework. Use `at-design-session` for the design process and `at-card-renderer` to produce the new HTML. Run the self-audit checklist before generating final HTML.

### Step 5 — Update the main card

```
→ update_rows(
    table_id=911939,
    row_id=<id from step 1>,
    fields={
      HTML: "<complete new rendered card HTML>",
      Last_Rework_Date: "<today's date in YYYY-MM-DD format>"
      // Also include any of these that changed:
      // Name: "<new name>"
      // Card_Key: "<new-card-key>"
      // Ruleset: "<base or magnitude>"
      // Status: "<current or legacy>"
    }
  )
```

HTML is always a **full replacement** — never partial. `Last_Rework_Date` is always set to today — include it in this same `update_rows` call, not a separate one.

### Step 6 — Verify both writes

```
→ list_table_rows(table_id=911939, search="Card Name")
  Confirm: HTML shows the new design

→ list_table_rows(table_id=1014012, search="<card_key>")
  Confirm: version row exists with old HTML + Change_Note + auto-set date
```

---

## Field Mapping Summary

### Versions table (1014012) — fields to write

| Field | Source | Notes |
|---|---|---|
| `Card_Key` | Copied from Cards v1 | Must match exactly — this is how the web app links versions |
| `Card_Name` | Copied from Cards v1 Name | Snapshot — OK if name later changes |
| `HTML` | Copied from Cards v1 HTML | The OLD HTML — exact copy before any changes |
| `Change_Note` | You write this | Short, descriptive reason (1 sentence) |
| `Version_Date` | **Auto-set by Baserow** | Never pass manually |

### Cards v1 (911939) — fields to update

| Field | Change when |
|---|---|
| `HTML` | Always — full re-render required |
| `Last_Rework_Date` | Always — set to today in `YYYY-MM-DD` format, in the same `update_rows` call as `HTML` |
| `Name` | Only if card is being renamed |
| `Card_Key` | Only if Name changes (keep slug in sync) |
| `Ruleset` | Only if ruleset scope changes |
| `Status` | Rarely — use `legacy` only to retire a card entirely |

---

## Rework Checklist

- [ ] Read current card via `list_table_rows` — captured `id`, `Card_Key`, `Name`, `HTML`
- [ ] Agreed on `Change_Note` (one sentence describing what changes)
- [ ] Called `create_rows` on table `1014012` with exact current `HTML` + `Change_Note`
- [ ] Verified version row exists in Versions table before touching main card
- [ ] Designed new card (at-design-session checklist passed)
- [ ] Rendered new full HTML via `renderCard()` (at-card-renderer)
- [ ] Called `update_rows` on table `911939` with full new `HTML` and `Last_Rework_Date` (today, `YYYY-MM-DD`)
- [ ] Updated `Name`, `Card_Key`, `Ruleset`, or `Status` if any of those changed
- [ ] Verified main card shows new HTML via `list_table_rows`
- [ ] Verified version history is navigable in card viewer (optional but recommended)
