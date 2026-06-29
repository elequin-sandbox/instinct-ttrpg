#!/usr/bin/env python3
"""Emit Baserow row payloads for Oath v2 push (MCP or manual)."""
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

DATE = "2026-06-28"

updates = []
for o in OATHS:
    row_id = OATH_ROW_IDS.get(o["key"])
    payload = {
        "Name": o["name"],
        "Card_Key": o["key"],
        "HTML": build(o),
        "Ruleset": "base",
        "Status": "current",
        "Last_Rework_Date": DATE,
    }
    if row_id:
        payload["id"] = row_id
        updates.append(payload)

creates = []
for o in OATHS:
    if o["key"] in OATH_ROW_IDS:
        continue
    creates.append(
        {
            "Name": o["name"],
            "Card_Key": o["key"],
            "HTML": build(o),
            "Ruleset": "base",
            "Status": "current",
            "Last_Rework_Date": DATE,
        }
    )

creates.extend(
    [
        {
            "Name": "Oath Template",
            "Card_Key": "oath-template-paladin-core",
            "HTML": build_oath_template(),
            "Ruleset": "base",
            "Status": "current",
            "Last_Rework_Date": DATE,
        },
        {
            "Name": "Patron Template",
            "Card_Key": "patron-template-warlock-core",
            "HTML": build_patron_template(),
            "Ruleset": "base",
            "Status": "current",
            "Last_Rework_Date": DATE,
        },
    ]
)

out = ROOT / "scripts" / "oath_v2_push.json"
out.write_text(json.dumps({"updates": updates, "creates": creates}, indent=2), encoding="utf-8")
print(f"updates: {len(updates)} creates: {len(creates)} -> {out}")
