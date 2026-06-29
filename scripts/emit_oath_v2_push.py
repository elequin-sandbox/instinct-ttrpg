#!/usr/bin/env python3
"""Emit Baserow row payloads for Oath push (MCP or manual)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_oath_html import (  # noqa: E402
    OATHS,
    OATH_ROW_IDS,
    build,
    build_oath_template,
    build_patron_template,
)

DATE = "2026-06-29"

updates = []
for o in OATHS:
    row_id = OATH_ROW_IDS.get(o["key"])
    if not row_id:
        continue
    updates.append(
        {
            "id": row_id,
            "Name": o["name"],
            "Card_Key": o["key"],
            "HTML": build(o),
            "Ruleset": "base",
            "Status": "current",
            "Last_Rework_Date": DATE,
        }
    )

for name, key, html_fn in (
    ("Oath Template", "oath-template-paladin-core", build_oath_template),
    ("Patron Template", "patron-template-warlock-core", build_patron_template),
):
    row_id = OATH_ROW_IDS.get(key)
    if row_id:
        updates.append(
            {
                "id": row_id,
                "Name": name,
                "Card_Key": key,
                "HTML": html_fn(),
                "Ruleset": "base",
                "Status": "current",
                "Last_Rework_Date": DATE,
            }
        )

out = ROOT / "scripts" / "oath_v2_push.json"
out.write_text(json.dumps({"updates": updates, "creates": []}, indent=2), encoding="utf-8")
print(f"updates: {len(updates)} -> {out}")
