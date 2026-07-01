#!/usr/bin/env python3
"""Playtest 4 Phase 2B — Crit Flourish rework (Paladin + Barbarian model cards).

Rewrites the "pared Smite (Paladin) / Strike (Barbarian)" model cards named in
design/classes.md §4 to the locked Crit Flourish pattern (core-rules.md §5,
card-anatomy.md §4, writing-conventions.md §3): a bold Flourish keyword +
printed number, colored red (offensive — remove dice from the opposing pool),
blue (defensive — help allies), or green (resolve — heal/recover Resolve or
Hit Die). One keyword + effect per line; combined spends split into separate
lines. Also pares each base Effect down to one clear check + outcome (no
stacked forks), per the classes.md §4 Playtest 4 card audit.

Usage:
  python3 scripts/build_flourish_cards.py              # dry-run summary
  python3 scripts/build_flourish_cards.py --write      # patch card-data.js + write proof/batch
  python3 scripts/build_flourish_cards.py --push       # write + push to Baserow (needs token)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import CARD_DATA, load_cards, push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "flourish_cards_batch.json"
PROOF_OUT = ROOT / "flourish-cards-proof.html"
DATE = "2026-07-01"

C1 = '<span class="kw kw-crit">1</span>'
C_LOOP = '<span class="kw kw-crit kw-crit-repeat">1↻</span>'
B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'


def strip_plain(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", t).strip()


def fl(color: str, cost: str, word: str, tail: str) -> str:
    """One Crit Flourish line: cost pip + colored dot + bold colored keyword + effect."""
    return (
        f'<div class="ci fl-{color}">{cost}<span class="fl-dot"></span>'
        f'<strong class="fl-word">{word}</strong> — {tail}</div>'
    )


def crit_block(*rows: str) -> str:
    body = "".join(rows)
    return f'<div class="csec"><div class="clbl">Crit</div><div class="crow">{body}</div></div>'


def paladin_ability(name: str, flavor: str, effect: str, crit: str, *, act: bool = True) -> str:
    sub = '<span class="cap cap-neutral">Act</span>' if act else "<span></span>"
    return (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{sub}</div>'
        f'<div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div><div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>{crit}</div>'
        '<div class="idtag">Paladin</div><div class="tier-float"><span>t1</span></div></div>'
    )


def barbarian_ability(name: str, flavor: str, effect: str, crit: str, *, act: bool = True) -> str:
    badge = '<span class="cap cap-neutral">Act</span>' if act else ""
    return (
        '<div class="card acc-barbarian"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{badge}</div>'
        f'<div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div><div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>{crit}</div>'
        '<div class="idtag">Barbarian</div><div class="tier-float"><span>t1</span></div></div>'
    )


CARDS: list[dict] = [
    # ---- Paladin (Rattled — red/blue/green demonstrated) ----
    {
        "id": 370,
        "key": "smite-paladin",
        "name": "Smite",
        "class_id": "paladin",
        "build": lambda: paladin_ability(
            "Smite",
            "You make yourself the problem they can't ignore.",
            "Perform a <strong>Presence</strong> check. On success, draw an enemy's focus entirely "
            "onto you — they must answer your challenge before acting on anyone else this beat.",
            crit_block(
                fl(
                    "red",
                    C_LOOP,
                    "Rattled 1",
                    "remove 1 die from another enemy who heard you; they falter, fixing on you instead.",
                )
            ),
        ),
    },
    {
        "id": 373,
        "key": "divine-challenge-paladin",
        "name": "Divine Challenge",
        "class_id": "paladin",
        "build": lambda: paladin_ability(
            "Divine Challenge",
            "Conviction lands harder than steel.",
            f"Perform a <strong>Faith</strong> check. On success, <strong>Strike</strong> with divine "
            f"force — gain {B1} on the damage roll.",
            crit_block(
                fl(
                    "red",
                    C1,
                    "Rattled 2",
                    "remove 2 dice from their pool; they reel, shaken in front of their allies.",
                )
            ),
        ),
    },
    {
        "id": 378,
        "key": "sacred-ground-paladin",
        "name": "Condemn",
        "class_id": "paladin",
        "build": lambda: paladin_ability(
            "Condemn",
            "You don't curse them. You recognize what they are.",
            "Perform a <strong>Faith</strong> check. On success, speak what they have done aloud — "
            "the truth lands. They must choose: <strong>Stand down</strong> — abandon their course, "
            "visibly shaken; or <strong>Press on</strong> — everyone present sees them clearly now.",
            crit_block(
                fl("red", C1, "Rattled 2", "remove 2 dice from their pool."),
                fl(
                    "blue",
                    C1,
                    "Boost 1",
                    "each ally gains this on their next <strong>Strike</strong> against them.",
                ),
            ),
        ),
    },
    {
        "id": 369,
        "key": "lay-on-hands-paladin",
        "name": "Lay on Hands",
        "class_id": "paladin",
        "build": lambda: paladin_ability(
            "Lay on Hands",
            "Not this one. Not today.",
            f"Perform a <strong>Medicine</strong> check. On success, touch an ally — they shake off "
            f"the worst thing pressing on them and recover a lost {HD}.",
            crit_block(
                fl(
                    "green",
                    C1,
                    "Resolve 2",
                    "they also recover 2 Resolve, steadied enough to keep fighting.",
                )
            ),
        ),
    },
    # ---- Barbarian (Sundered — Barbarian's owned narrative term, classes.md §2) ----
    {
        "id": 342,
        "key": "reckless-strike-barbarian",
        "name": "Reckless Strike",
        "class_id": "barbarian",
        "build": lambda: barbarian_ability(
            "Reckless Strike",
            "You stop caring about what happens to you.",
            f"Perform an <strong>Athletics</strong> check with {B1}. On success, <strong>Strike</strong> "
            "with full force — you leave your guard wide open until your next turn.",
            crit_block(
                fl(
                    "red",
                    C1,
                    "Sundered 2",
                    "remove 2 dice from their pool; the blow cracks something structural.",
                )
            ),
        ),
    },
    {
        "id": 343,
        "key": "break-barbarian",
        "name": "Break",
        "class_id": "barbarian",
        "build": lambda: barbarian_ability(
            "Break",
            "There is no obstacle. There is only physics.",
            "Perform an <strong>Athletics</strong> check. On success, smash a piece of the "
            "<strong>Scene</strong> — an object, barrier, or structure is destroyed, opening a path "
            "or clearing an enemy's cover.",
            crit_block(
                fl(
                    "red",
                    C1,
                    "Sundered 2",
                    "remove 2 dice from an enemy caught in the wreckage.",
                )
            ),
        ),
    },
    {
        "id": 348,
        "key": "sundering-blow-barbarian",
        "name": "Sundering Blow",
        "class_id": "barbarian",
        "build": lambda: barbarian_ability(
            "Sundering Blow",
            "You don't just hit them. You compromise them.",
            "Perform an <strong>Athletics</strong> check. On success, <strong>Strike</strong> a target "
            "and open a structural weakness that follows them the rest of this <strong>Scene</strong>.",
            crit_block(
                fl("red", C1, "Sundered 2", "remove 2 dice from their pool immediately."),
                fl(
                    "blue",
                    C1,
                    "Boost 1",
                    "each ally who <strong>Strikes</strong> them this <strong>Scene</strong> gains this.",
                ),
            ),
        ),
    },
    {
        "id": 349,
        "key": "endure-barbarian",
        "name": "Endure",
        "class_id": "barbarian",
        "build": lambda: barbarian_ability(
            "Endure",
            "You have taken worse.",
            "Perform an <strong>Endurance</strong> check. On success, name what you're pushing "
            "through — pain, fear, exhaustion — and shrug it off; add a Rage die to your pool.",
            crit_block(
                fl(
                    "green",
                    C1,
                    "Resolve 2",
                    "you also recover 2 Resolve, steadied by what you just proved to yourself.",
                )
            ),
        ),
    },
]


def patch_cards(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c.get("Card_Key"): c for c in cards}
    missing = [spec["key"] for spec in CARDS if spec["key"] not in by_key]
    if missing:
        raise SystemExit(f"Card_Key(s) not found in card-data.js: {missing}")

    batch: list[dict] = []
    for spec in CARDS:
        html = spec["build"]()
        card = by_key[spec["key"]]
        plain = f"> {strip_plain(html)}"
        card["HTML"] = html
        card["EffectText_Plain"] = plain
        card["Last_Rework_Date"] = DATE
        batch.append(
            {
                "id": spec["id"],
                "Name": spec["name"],
                "Card_Key": spec["key"],
                "HTML": html,
                "EffectText_Plain": plain,
                "Last_Rework_Date": DATE,
            }
        )
    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        "// Generated by scripts/build_flourish_cards.py — do not edit manually. "
        f"Last updated: {DATE}\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof(cards: list[dict], keys: list[str]) -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_key = {c["Card_Key"]: c for c in cards}
    chunks = []
    for key in keys:
        c = by_key[key]
        cls_scope = f"scope-ability cls-{c.get('Class') or ''}"
        chunks.append(
            f'<div class="sample"><div class="stag">{c["Name"]}</div>'
            f'<div class="cardwrap {cls_scope}">{c["HTML"]}</div></div>'
        )
    legend = (
        '<div class="legend">'
        '<span class="lg-item"><span class="lg-dot" style="background:#991B1B"></span>'
        "Red — offensive: remove N dice from the opposing pool</span>"
        '<span class="lg-item"><span class="lg-dot" style="background:#2563EB"></span>'
        "Blue — defensive: help allies (Boost, etc.)</span>"
        '<span class="lg-item"><span class="lg-dot" style="background:#166534"></span>'
        "Green — resolve: heal / recover Resolve or Hit Die</span>"
        "</div>"
    )
    PROOF_OUT.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Crit Flourish proof — Playtest 4 Phase 2B</title><style>"
        f"{css}"
        "body{background:#14100a;padding:28px;color:#f0e6cf;font-family:system-ui,sans-serif;}"
        "h1{font-size:18px;letter-spacing:1px;color:#e7d6ac;margin-bottom:4px;}"
        "h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;"
        "margin:28px 0 12px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}"
        "p.sub{color:#a08a5c;font-size:13px;margin-bottom:18px;}"
        ".legend{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:22px;font-size:12px;color:#d8c8a0;}"
        ".lg-item{display:flex;align-items:center;gap:6px;}"
        ".lg-dot{display:inline-block;width:9px;height:9px;border-radius:50%;}"
        ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}"
        ".stag{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#c9b896;}"
        "</style></head><body>"
        "<h1>Crit Flourish rework — Playtest 4 Phase 2B</h1>"
        "<p class=\"sub\">Model cards: pared Smite (Paladin) / Strike (Barbarian) — "
        "design/classes.md §4. Bold Flourish keyword + printed number, colored by category.</p>"
        f"{legend}"
        "<h2>Paladin</h2>"
        f'<div class="grid">{"".join(chunks[:4])}</div>'
        "<h2>Barbarian</h2>"
        f'<div class="grid">{"".join(chunks[4:])}</div>'
        "</body></html>",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    cards = load_cards()
    cards, batch = patch_cards(cards)
    proof_keys = [s["key"] for s in CARDS]

    print(f"Patched {len(batch)} cards (Crit Flourish rework)")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']}")

    if args.write or args.push:
        write_card_data(cards)
        write_proof(cards, proof_keys)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name}, {PROOF_OUT.name}, {BATCH_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run — pass --write or --push")


if __name__ == "__main__":
    main()
