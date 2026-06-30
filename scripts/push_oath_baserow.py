#!/usr/bin/env python3
"""Push Paladin Oath HTML updates to Baserow table 911939."""
from __future__ import annotations

import sys
from datetime import date
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
from scripts.strip_origin_stems import push_baserow  # noqa: E402


def main() -> None:
    today = date.today().isoformat()
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
                "Last_Rework_Date": today,
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
                "Last_Rework_Date": today,
            }
        )

    push_baserow(items)


if __name__ == "__main__":
    main()
