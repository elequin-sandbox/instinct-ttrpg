# Card Parallelism Pass — Handoff (resume point)

**Goal:** Normalize all 245 `Status:current` cards in Baserow to one unified look.
Full spec is in `design/card-anatomy.md` **§7** (already written this session).

## What is ALREADY done — do NOT redo
- **Normalization complete for all 245 cards.** Final HTML is pre-generated in
  `parallelism-pass/normalized.json` and split into push-ready batches `upd_00.json`…`upd_06.json`.
  Each batch row is the exact Baserow payload: `{ "id", "HTML", "Last_Rework_Date":"2026-06-24" }`.
- **Pushed to Baserow (table 911939):** `upd_00.json` (ids 298–332) and `upd_01.json` (ids 333–367).
  = **70 cards live.**
- **Viewer:** `index.html` already has the canonical CSS (`canon_keywords/accents/header.css`) +
  EB Garamond font injected. New cards use `.kw`/`.acc-*`/`.hdr`/`.idtag`/`.tier-float` classes that
  the viewer styles directly (they bypass the old `restyle()` `.tp` path — no JS change needed).
- **Doctrine:** `design/card-anatomy.md` §7 + `card-inventory.md` updated.
- **Backup:** full pre-pass snapshot of all 245 originals at `cards-backup-2026-06-24.json`
  (re-pushable for rollback). NOTE: Annie chose Versions-table archival originally, but the volume
  made per-row archiving impractical; the snapshot file is the rollback path.

## What REMAINS — push these 5 batches (175 cards, ids 368–636)
`upd_02.json` (368–402) · `upd_03.json` (403–451) · `upd_04.json` (452–486) ·
`upd_05.json` (487–596) · `upd_06.json` (597–636)

### Exact procedure (per batch, cheapest path)
For each remaining `upd_0X.json`:
1. Read the file (it is already the payload — do not regenerate or reformat).
2. Call Baserow `update_rows` with `table_id = 911939` and `rows =` the entire file array.
3. Confirm the returned count, then move to the next file.

Do them one batch per message to keep context small. Do NOT re-run `normalize.py` unless Annie
asks for a content change — the HTML is final.

## Key facts
- Cards table: **911939**. Versions table: 1014012. Status field values: `current` / `legacy`.
- Only `Status:current` rows are in scope (245). Legacy rows untouched.
- Annie pushes `index.html` herself via Sourcetree (never run git).

## If a content change is needed later
Edit `parallelism-pass/normalize.py`, re-run `python3 normalize.py` from a dir containing
`current_cards.json` (regenerate that via Baserow list_table_rows if missing), then re-split into
`upd_*.json` and re-push.
