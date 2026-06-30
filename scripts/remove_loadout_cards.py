#!/usr/bin/env python3
"""Remove Loadout cards from card-data.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD_DATA = ROOT / "card-data.js"
LOADOUT_KEYS = {
    "loadout-barbarian-core",
    "loadout-bard-core",
    "loadout-cleric-core",
    "loadout-druid-core",
    "loadout-fighter-core",
    "loadout-paladin-core",
    "loadout-ranger-core",
    "loadout-rogue-core",
    "loadout-warlock-core",
}


def main() -> None:
    text = CARD_DATA.read_text(encoding="utf-8")
    m = re.search(r"(window\.CARD_DATA\s*=\s*)(\[.*\])", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse card-data.js")
    cards = json.loads(m.group(2))
    before = len(cards)
    kept = [c for c in cards if c.get("Card_Key") not in LOADOUT_KEYS]
    removed = before - len(kept)
    if removed != 9:
        found = {c.get("Card_Key") for c in cards if c.get("Card_Key") in LOADOUT_KEYS}
        raise SystemExit(f"Expected 9 Loadout cards, removed {removed}: {found}")
    new_json = json.dumps(kept, separators=(",", ":"))
    CARD_DATA.write_text(f"window.CARD_DATA = {new_json};\n", encoding="utf-8")
    print(f"Removed {removed} Loadout cards ({before} → {len(kept)})")


if __name__ == "__main__":
    main()
