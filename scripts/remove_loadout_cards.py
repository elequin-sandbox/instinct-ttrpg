#!/usr/bin/env python3
"""Remove retired chargen-setup cards (Loadout, Build Your Deck) from card-data.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD_DATA = ROOT / "card-data.js"

RETIRED_KEYS = {
    # Loadout Core (already absent after first pass — kept for idempotent reruns)
    "loadout-barbarian-core",
    "loadout-bard-core",
    "loadout-cleric-core",
    "loadout-druid-core",
    "loadout-fighter-core",
    "loadout-paladin-core",
    "loadout-ranger-core",
    "loadout-rogue-core",
    "loadout-warlock-core",
    # Build Your Deck Core
    "build-your-deck-barbarian",
    "build-your-deck-bard",
    "build-your-deck-cleric",
    "build-your-deck-druid",
    "build-your-deck-fighter",
    "build-your-deck-paladin",
    "build-your-deck-ranger",
    "build-your-deck-rogue",
    "build-your-deck-warlock",
}


def main() -> None:
    text = CARD_DATA.read_text(encoding="utf-8")
    m = re.search(r"(window\.CARD_DATA\s*=\s*)(\[.*\])", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse card-data.js")
    cards = json.loads(m.group(2))
    before = len(cards)
    kept = [c for c in cards if c.get("Card_Key") not in RETIRED_KEYS]
    removed = before - len(kept)
    if removed == 0:
        print("No chargen-setup cards to remove")
        return
    new_json = json.dumps(kept, separators=(",", ":"))
    CARD_DATA.write_text(f"window.CARD_DATA = {new_json};\n", encoding="utf-8")
    print(f"Removed {removed} chargen-setup cards ({before} → {len(kept)})")


if __name__ == "__main__":
    main()
