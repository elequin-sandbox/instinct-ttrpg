#!/usr/bin/env python3
"""Push Paladin Oath HTML updates to Baserow table 911939."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
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

API = "https://api.baserow.io/api/database/rows/table/911939/batch/?user_field_names=true"
DATE = "2026-06-29"


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
        raise SystemExit("Set BASEROW_TOKEN env or window.IRPG_TOKEN in config.js")

    items = []
    for o in OATHS:
        row_id = OATH_ROW_IDS[o["key"]]
        items.append(
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
        row_id = OATH_ROW_IDS[key]
        items.append(
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

    body = json.dumps({"items": items}).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=body,
        method="PATCH",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Baserow PATCH failed ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e

    updated = result.get("items") or items
    keys = [i.get("Card_Key") or OATHS[i]["key"] if i.get("id") else "?" for i in items]
    print(f"Pushed {len(updated)} rows to Baserow:")
    for item in items:
        print(f"  row {item['id']}: {item['Card_Key']}")


if __name__ == "__main__":
    main()
