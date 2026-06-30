#!/usr/bin/env python3
"""Retire all Loadout Core cards in Baserow (Status → retired)."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.baserow.io/api/database/rows/table/911939/batch/?user_field_names=true"
DATE = "2026-06-30"

LOADOUT_ROWS = {
    "loadout-fighter-core": 412,
    "loadout-paladin-core": 415,
    "loadout-ranger-core": 418,
    "loadout-cleric-core": 421,
    "loadout-bard-core": 424,
    "loadout-warlock-core": 427,
    "loadout-druid-core": 430,
    "loadout-barbarian-core": 433,
    "loadout-rogue-core": 436,
}


def read_token() -> str:
    token = os.environ.get("BASEROW_TOKEN", "").strip()
    if token:
        return token
    text = (ROOT / "config.js").read_text(encoding="utf-8")
    m = re.search(r'IRPG_TOKEN\s*=\s*"([^"]*)"', text)
    token = (m.group(1) if m else "").strip()
    if token and token != "PASTE_YOUR_SCOPED_BASEROW_TOKEN_HERE":
        return token
    return ""


def main() -> None:
    token = read_token()
    if not token:
        print("SKIP: no Baserow token — retire Loadout rows manually or set BASEROW_TOKEN")
        return

    items = [
        {
            "id": row_id,
            "Status": "retired",
            "Last_Rework_Date": DATE,
        }
        for row_id in LOADOUT_ROWS.values()
    ]
    req = urllib.request.Request(
        API,
        data=json.dumps({"items": items}).encode(),
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        },
        method="PATCH",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = json.loads(resp.read().decode())
        print(f"Retired {len(items)} Loadout rows in Baserow")
        for item in body.get("items", []):
            print(f"  row {item.get('id')} → Status={item.get('Status')}")
    except urllib.error.HTTPError as e:
        print(f"ERROR {e.code}: {e.read().decode()[:500]}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
