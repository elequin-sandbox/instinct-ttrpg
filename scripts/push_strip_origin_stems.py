#!/usr/bin/env python3
"""Push stem-stripped Background/Ancestry/Bond HTML to Baserow table 911939."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import API, DATE, load_cards, push_baserow, read_token  # noqa: E402


def main() -> None:
    cards = load_cards()
    batch = []
    for card in cards:
        if card.get("Card_Type") not in {"Background", "Ancestry", "Bond"}:
            continue
        html = card.get("HTML", "")
        if "bf-stem" in html:
            raise SystemExit(f"Card still has stem: {card.get('Card_Key')}")
        batch.append(
            {
                "id": card["id"],
                "Name": card.get("Name"),
                "Card_Key": card.get("Card_Key"),
                "HTML": html,
                "Last_Rework_Date": card.get("Last_Rework_Date") or DATE,
            }
        )
    print(f"Prepared {len(batch)} rows for Baserow")
    push_baserow(batch)


if __name__ == "__main__":
    main()
