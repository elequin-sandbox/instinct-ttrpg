#!/usr/bin/env python3
"""Build Ancestry Snap Check HTML for all 10 deck cards.

Usage:
  python3 scripts/build_ancestry_snap.py              # dry-run
  python3 scripts/build_ancestry_snap.py --write    # patch card-data.js + batch JSON
  python3 scripts/build_ancestry_snap.py --push     # write + push to Baserow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import CARD_DATA, push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "ancestry_snap_batch.json"
DATE = "2026-06-29"

# (verb, description) — CRPG syntax; Boost 1 max; niche fiction only
Option = tuple[str, str]

ANCESTRIES: list[dict] = [
    {
        "id": 505,
        "name": "Human",
        "key": "human-ancestry",
        "timing": "Act",
        "flavor": "You were not born with magic or ancient lineage. You were born with will.",
        "trigger": (
            "Once per <strong>Scene</strong>, when sheer determination could tip a stuck moment, "
            "try to push through with human grit and make a <strong>Snap Check</strong>."
        ),
        "fail": "The moment slips — you overreach or misread the room.",
        "options": [
            ("Press On", "name what you're reaching for; take <span class=\"kw kw-boost\">Boost 1</span> on your next check toward it"),
            ("Find a Way", "improvise an angle nobody else thought of; the GM names what opens"),
            ("Rally", "steady an ally beside you; they take <span class=\"kw kw-boost\">Boost 1</span> on their next check"),
        ],
    },
    {
        "id": 506,
        "name": "Elf",
        "key": "elf-ancestry",
        "timing": "Act",
        "flavor": "Something in you is older than this world, and it always notices.",
        "trigger": (
            "Once per <strong>Scene</strong>, when old memory or a hidden detail might matter, "
            "try to attune to what others overlook and make a <strong>Snap Check</strong>."
        ),
        "fail": "The thread fades — what you sensed stays out of reach for now.",
        "options": [
            ("Listen", "ask the GM one honest question about this <strong>Scene</strong>; they answer truthfully"),
            ("Trace", "name one detail others missed; the GM confirms if it's there"),
            ("Stillness", "read the room's weight; take <span class=\"kw kw-boost\">Boost 1</span> on your next social check"),
        ],
    },
    {
        "id": 507,
        "name": "Dwarf",
        "key": "dwarf-ancestry",
        "timing": "React",
        "flavor": "You were carved from stone and stubbornness — and it shows.",
        "trigger": (
            "Once per <strong>Scene</strong>, when a blow — physical, social, or emotional — would stagger you, "
            "try to hold your ground and make a <strong>Snap Check</strong>."
        ),
        "fail": "The hit lands clean — you show the cost, and the <strong>Scene</strong> keeps pushing.",
        "options": [
            ("Absorb It", "take the hit without losing your footing; narrate what you refuse to show"),
            ("Brace", "plant your weight; take <span class=\"kw kw-boost\">Boost 1</span> on your next check to stay in the fight"),
            ("Answer Back", "meet pressure with a short, grounded reply that shifts the tone"),
        ],
    },
    {
        "id": 508,
        "name": "Halfling",
        "key": "halfling-ancestry",
        "timing": "React",
        "flavor": "You've gotten away with things that should have ended you more times than you can count.",
        "trigger": (
            "Once per <strong>Scene</strong>, when a check doesn't go your way, "
            "try to wriggle out with halfling luck and make a <strong>Snap Check</strong>."
        ),
        "fail": "No reprieve — you own the bad beat and the <strong>Scene</strong> moves on.",
        "options": [
            ("Slip Away", "narrate how you get clear of the worst of it"),
            ("Look Harmless", "shrink the target; an enemy hesitates or looks elsewhere"),
            ("Small Fortune", "name one absurd small thing that softens the blow; the GM plays it fairly"),
        ],
    },
    {
        "id": 509,
        "name": "Half-Orc",
        "key": "half-orc-ancestry",
        "timing": "React",
        "flavor": "You have been underestimated your whole life. You have learned to use that.",
        "trigger": (
            "Once per <strong>Scene</strong>, when the <strong>Scene</strong> pushes you to yield or fall, "
            "try to refuse and make a <strong>Snap Check</strong>."
        ),
        "fail": "You buckle — the pressure wins this beat.",
        "options": [
            ("Stand", "stay on your feet; narrate what keeps you there"),
            ("Snarl", "let your heritage show; one foe hesitates"),
            ("Survive", "draw on scars; take <span class=\"kw kw-boost\">Boost 1</span> on your very next check"),
        ],
    },
    {
        "id": 510,
        "name": "Tiefling",
        "key": "tiefling-ancestry",
        "timing": "Act",
        "flavor": "You carry something ancient and unholy in your blood. It is not a curse. It is yours.",
        "trigger": (
            "Once per <strong>Scene</strong>, when your unsettling heritage could bend a social beat, "
            "try to lean on what you carry and make a <strong>Snap Check</strong>."
        ),
        "fail": "The wrong kind of attention — folk pull back or misread you.",
        "options": [
            ("Shadow", "your presence shifts the mood; name what changes"),
            ("Bargain", "offer a small infernal favor; the GM names the price"),
            ("Whisper", "speak one truth that shouldn't be known; one listener reacts honestly"),
        ],
    },
    {
        "id": 511,
        "name": "Dragonborn",
        "key": "dragonborn-ancestry",
        "timing": "Act",
        "flavor": "Every choice you make is an answer to what your bloodline means.",
        "trigger": (
            "Once per <strong>Scene</strong>, when your draconic nature could unsettle or awe, "
            "try to let it surface and make a <strong>Snap Check</strong>."
        ),
        "fail": "The tell backfires — others read it wrong or resist.",
        "options": [
            ("Bearing", "your stillness or voice changes the room's temperature"),
            ("Ember", "a small elemental tell; name it; the GM plays it fairly"),
            ("Lineage", "name what your blood remembers; ask one honest GM question"),
        ],
    },
    {
        "id": 512,
        "name": "Gnome",
        "key": "gnome-ancestry",
        "timing": "Act",
        "flavor": "Your mind moves in directions that simply do not occur to anyone else.",
        "trigger": (
            "Once per <strong>Scene</strong>, when an odd angle or trick could help, "
            "try to see what others miss and make a <strong>Snap Check</strong>."
        ),
        "fail": "The bit falls flat — cleverness without payoff.",
        "options": [
            ("Tinker", "use something here in an unintended way; name how"),
            ("Misdirect", "draw eyes elsewhere; take <span class=\"kw kw-boost\">Boost 1</span> on your next sneaky check"),
            ("Spark", "name the overlooked solution; the GM confirms if it could work"),
        ],
    },
    {
        "id": 513,
        "name": "Half-Elf",
        "key": "half-elf-ancestry",
        "timing": "Act",
        "flavor": "You belong to neither world completely. You have learned to make that a strength.",
        "trigger": (
            "Once per <strong>Scene</strong>, when you could bridge two peoples or ways of seeing, "
            "try to read both sides and make a <strong>Snap Check</strong>."
        ),
        "fail": "You miss the thread — neither side quite lands.",
        "options": [
            ("Translate", "name the thread between two opposed parties; they hear you"),
            ("Soften", "ease tension with the right tone; one NPC shifts their stance"),
            ("Switch", "lean elven grace or human drive; take <span class=\"kw kw-boost\">Boost 1</span> on your next check"),
        ],
    },
    {
        "id": 514,
        "name": "Orc",
        "key": "orc-ancestry",
        "timing": "Act",
        "flavor": "You are built for things that require more than most people have.",
        "trigger": (
            "Once per <strong>Scene</strong>, when raw force or presence could shift the moment, "
            "try to bring orcish weight to bear and make a <strong>Snap Check</strong>."
        ),
        "fail": "You overcommit — momentum turns against you.",
        "options": [
            ("Rush", "close distance; name what gives way before you"),
            ("Hold", "plant yourself; the <strong>Scene</strong> works around your mass"),
            ("Roar", "your voice carries; one ally takes <span class=\"kw kw-boost\">Boost 1</span> on their next <strong>Action</strong>"),
        ],
    },
]


def _options_html(options: list[Option]) -> str:
    parts = []
    for verb, desc in options:
        parts.append(f"<strong>{verb}</strong> — {desc}")
    return " · ".join(parts)


def _snap_row(band: str, text: str) -> str:
    return (
        f'<div class="snap-row">'
        f'<span class="snap-band"><span class="kw kw-snap">{band}</span></span>'
        f'<span class="snap-txt">{text}</span>'
        f"</div>"
    )


def render_ancestry_snap(card: dict) -> str:
    timing = card["timing"]
    opts = _options_html(card["options"])
    choose1 = f"Choose <strong>1</strong>: {opts}"
    choose2 = f"Choose <strong>2</strong> from the above."
    snap = (
        '<div class="snap-sec">'
        '<div class="snap-lbl">Snap Check</div>'
        + _snap_row("1–3", card["fail"])
        + _snap_row("4–8", choose1)
        + _snap_row("9+", choose2)
        + "</div>"
    )
    return (
        f'<div class="card bf-ancestry acc-ancestry">'
        f'<div class="hdr">'
        f'<div class="hdr-top">'
        f'<span class="cap cap-accent">Ancestry</span>'
        f'<span class="cap cap-neutral">{timing}</span>'
        f"</div>"
        f'<div class="hdr-name">{card["name"]}</div>'
        f"</div>"
        f'<div class="bf-body">'
        f'<div class="bf-flv">{card["flavor"]}</div>'
        f'<div class="bf-trig">{card["trigger"]}</div>'
        f"{snap}"
        f"</div>"
        f"</div>"
    )


def load_cards() -> list[dict]:
    text = CARD_DATA.read_text(encoding="utf-8")
    m = re.search(r"window\.CARD_DATA\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse card-data.js")
    return json.loads(m.group(1))


def patch_card_data(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c["key"]: c for c in ANCESTRIES}
    batch: list[dict] = []
    for card in cards:
        key = card.get("Card_Key", "")
        if key not in by_key:
            continue
        spec = by_key[key]
        html = render_ancestry_snap(spec)
        card["HTML"] = html
        card["Last_Rework_Date"] = DATE
        batch.append(
            {
                "id": spec["id"],
                "Name": spec["name"],
                "Card_Key": key,
                "HTML": html,
                "Last_Rework_Date": DATE,
            }
        )
    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Auto-generated card data — do not hand-edit; regenerate from Baserow.\n"
        f"// Source: build_ancestry_snap.py ({DATE})\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    for spec in ANCESTRIES:
        html = render_ancestry_snap(spec)
        print(f"{spec['key']} ({spec['timing']}) — {len(html)} chars")

    if args.write or args.push:
        cards = load_cards()
        cards, batch = patch_card_data(cards)
        if len(batch) != len(ANCESTRIES):
            raise SystemExit(f"Expected {len(ANCESTRIES)} ancestry rows, got {len(batch)}")
        write_card_data(cards)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name} and {BATCH_OUT.name}")
        if args.push:
            push_baserow(batch)
    elif not args.write:
        print("Dry run only. Pass --write or --push to apply.")


if __name__ == "__main__":
    main()
