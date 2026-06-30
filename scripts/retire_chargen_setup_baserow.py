#!/usr/bin/env python3
"""Mark Loadout + Build Your Deck Core cards as legacy in Baserow (Status → legacy)."""
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

from scripts.strip_origin_stems import push_baserow, read_token  # noqa: E402

DATE = "2026-06-30"

# Loadout Core — primer v2 owns chargen setup (June 2026)
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

# Build Your Deck — replaced by primer chargen flow (June 2026)
BUILD_YOUR_DECK_ROWS = {
    "build-your-deck-fighter": 595,
    "build-your-deck-paladin": 596,
    "build-your-deck-ranger": 597,
    "build-your-deck-cleric": 598,
    "build-your-deck-bard": 599,
    "build-your-deck-warlock": 600,
    "build-your-deck-druid": 601,
    "build-your-deck-barbarian": 602,
    "build-your-deck-rogue": 603,
}

ALL_ROWS = {**LOADOUT_ROWS, **BUILD_YOUR_DECK_ROWS}


def main() -> None:
    if not read_token():
        raise SystemExit(
            "Baserow token required: set BASEROW_TOKEN or window.IRPG_TOKEN in config.js"
        )

    items = [
        {
            "id": row_id,
            "Status": "legacy",
            "Last_Rework_Date": DATE,
        }
        for row_id in ALL_ROWS.values()
    ]
    push_baserow(items)
    print(f"Set Status=legacy on {len(items)} Loadout + Build Your Deck rows ({DATE})")


if __name__ == "__main__":
    main()
