#!/usr/bin/env python3
"""Prepare Baserow payloads: archive + V1 update (20) + create (10 new instincts)."""
from __future__ import annotations

import json
from pathlib import Path

from render_instinct_dual import render_instinct_dual

EXISTING = [
    {"id": 449, "word": "Bold", "key": "bold-instinct"},
    {"id": 450, "word": "Perceptive", "key": "perceptive-instinct"},
    {"id": 451, "word": "Tenacious", "key": "tenacious-instinct"},
    {"id": 452, "word": "Resourceful", "key": "resourceful-instinct"},
    {"id": 453, "word": "Charismatic", "key": "charismatic-instinct"},
    {"id": 454, "word": "Cunning", "key": "cunning-instinct"},
    {"id": 455, "word": "Nimble", "key": "nimble-instinct"},
    {"id": 456, "word": "Steadfast", "key": "steadfast-instinct"},
    {"id": 457, "word": "Intuitive", "key": "intuitive-instinct"},
    {"id": 458, "word": "Fierce", "key": "fierce-instinct"},
    {"id": 459, "word": "Learned", "key": "learned-instinct"},
    {"id": 460, "word": "Empathic", "key": "empathic-instinct"},
    {"id": 461, "word": "Vigilant", "key": "vigilant-instinct"},
    {"id": 462, "word": "Resilient", "key": "resilient-instinct"},
    {"id": 463, "word": "Subtle", "key": "subtle-instinct"},
    {"id": 464, "word": "Diplomatic", "key": "diplomatic-instinct"},
    {"id": 465, "word": "Commanding", "key": "commanding-instinct"},
    {"id": 466, "word": "Daring", "key": "daring-instinct"},
    {"id": 467, "word": "Resolute", "key": "resolute-instinct"},
    {"id": 468, "word": "Primal", "key": "primal-instinct"},
]

# VN archetype tag pool expansion (kuudere, genki, dandere, rival, etc.)
NEW_WORDS = [
    "Stoic", "Impulsive", "Wistful", "Sardonic", "Devoted",
    "Impish", "Brooding", "Earnest", "Guarded", "Gregarious",
]

ALL_WORDS = [row["word"] for row in EXISTING] + NEW_WORDS

CHANGE_NOTE = (
    "V1 Band Wash fork stack — Strength/Flaw halves, teal/crimson washes, OR medallion"
)
TODAY = "2026-06-28"


def slug(word: str) -> str:
    return word.lower().replace(" ", "-") + "-instinct"


def main() -> None:
    # Old HTML captured from Baserow (June 28 minimal dual-purpose layout)
    baserow_dump = Path(__file__).resolve().parents[1] / "scripts" / "instinct_old_html.json"
    if baserow_dump.exists():
        old_by_key = json.loads(baserow_dump.read_text(encoding="utf-8"))
    else:
        old_by_key = {}

    archives = []
    updates = []
    for row in EXISTING:
        word = row["word"]
        key = row["key"]
        new_html = render_instinct_dual(word, "v1")
        old_html = old_by_key.get(key)
        if old_html:
            archives.append({
                "Card_Key": key,
                "Card_Name": word,
                "HTML": old_html,
                "Change_Note": CHANGE_NOTE,
            })
        updates.append({
            "id": row["id"],
            "HTML": new_html,
            "Last_Rework_Date": TODAY,
        })

    creates = []
    for word in NEW_WORDS:
        key = slug(word)
        creates.append({
            "Name": word,
            "Card_Key": key,
            "HTML": render_instinct_dual(word, "v1"),
            "Ruleset": "base",
            "Status": "current",
            "Last_Rework_Date": TODAY,
        })

    out = Path(__file__).resolve().parents[1] / "scripts" / "instinct_v1_push.json"
    out.write_text(
        json.dumps({"archives": archives, "updates": updates, "creates": creates}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {out}")
    print(f"archives={len(archives)} updates={len(updates)} creates={len(creates)}")


if __name__ == "__main__":
    main()
