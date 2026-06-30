#!/usr/bin/env python3
"""Barbarian deck audit — narrative-term crit options + Endure/Frenzy/Battle Cry fixes.

Usage:
  python3 scripts/build_barbarian_pool.py --write
  python3 scripts/build_barbarian_pool.py --push
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_barbarian_core import (  # noqa: E402
    RETRIBUTION,
    RAGE,
    build_rage_html,
    build_retribution_html,
)
from scripts.strip_origin_stems import CARD_DATA, load_cards, push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "barbarian_pool_batch.json"
PROOF_OUT = ROOT / "barbarian-pool-proof.html"
DATE = "2026-06-30"

C1 = '<span class="kw kw-crit">1</span>'
C_LOOP = '<span class="kw kw-crit">1↻</span>'
B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'

CHUCK_LADDER = (
    '<div style="margin-top:4px;display:grid;grid-template-columns:1fr 68px;row-gap:1px;'
    "column-gap:3px;align-items:center;font-size:0.8em;\">"
    '<div></div><div style="background:#854F0B;color:#FAEEDA;border-radius:3px;padding:1px 0;'
    'font-weight:500;text-align:center;">★ Gone ★</div>'
    '<div></div><div style="border:0.5px solid #c8a96e;border-radius:3px;text-align:center;'
    'padding:1px 0;color:#4a3010;">120 ft</div>'
    '<div></div><div style="border:0.5px solid #c8a96e;border-radius:3px;text-align:center;'
    'padding:1px 0;color:#4a3010;">60 ft</div>'
    '<div style="text-align:right;font-weight:500;color:#5C1A1A;">One-Handed Object →</div>'
    '<div style="border:0.5px solid #5C1A1A;border-radius:3px;text-align:center;padding:1px 0;'
    'font-weight:500;color:#5C1A1A;">30 ft</div>'
    '<div style="text-align:right;font-weight:500;color:#5C1A1A;">Two-Handed Object →</div>'
    '<div style="border:0.5px solid #5C1A1A;border-radius:3px;text-align:center;padding:1px 0;'
    'font-weight:500;color:#5C1A1A;">15 ft</div>'
    '<div style="text-align:right;font-weight:500;color:#5C1A1A;">Willing Creature →</div>'
    '<div style="border:0.5px solid #5C1A1A;border-radius:3px;text-align:center;padding:1px 0;'
    'font-weight:500;color:#5C1A1A;">5 ft</div>'
    '<div style="text-align:right;font-weight:500;color:#5C1A1A;">Hostile Creature →</div>'
    '<div style="border:0.5px solid #5C1A1A;border-radius:3px;text-align:center;padding:1px 0;'
    'font-weight:500;color:#5C1A1A;">0 ft</div></div>'
)


def _crit(*rows: str) -> str:
    body = "".join(f'<div class="ci">{r}</div>' for r in rows)
    return f'<div class="csec"><div class="clbl">Crit</div><div class="crow">{body}</div></div>'


def _ability(
    name: str,
    flavor: str,
    effect: str,
    crit: str = "",
    *,
    act: bool = False,
    react: bool = False,
    extra_body: str = "",
) -> str:
    badges = '<span class="cap cap-neutral">Ability</span>'
    if act:
        badges += '<span class="cap cap-neutral">Act</span>'
    elif react:
        badges += '<span class="cap cap-neutral">React</span>'
    return (
        '<div class="card acc-barbarian">'
        f'<div class="hdr"><div class="hdr-top">{badges}</div>'
        f'<div class="hdr-name">{name}</div></div>'
        '<div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div>'
        '<div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>'
        f"{extra_body}{crit}"
        "</div>"
        '<div class="idtag">Barbarian</div>'
        '<div class="tier-float"><span>t1</span></div></div>'
    )


def strip_plain(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", t).strip()


CARDS: list[dict] = [
    {
        "id": 345,
        "key": "battle-cry-barbarian",
        "name": "Battle Cry",
        "card_type": "Act",
        "build": lambda: _ability(
            "Battle Cry",
            "The sound alone changes the calculus.",
            "Perform an <strong>Intimidation</strong> check. On success, every enemy in the "
            "<strong>Scene</strong> is <strong>Rattled</strong> — nerve breaks and they fight from "
            f"the back foot; all allies gain {B1} on their next <strong>Action</strong>.",
            _crit(f"{C_LOOP} Add a Rage die to your pool."),
            act=True,
        ),
    },
    {
        "id": 353,
        "key": "blood-for-blood-barbarian",
        "name": "Blood for Blood",
        "card_type": "Act",
        "build": lambda: _ability(
            "Blood for Blood",
            "The score isn't settled. Not yet.",
            f"Spend Rage dice equal to the number of <span class=\"kw kw-hd\">Hit Dice</span> you've lost this <strong>Scene</strong>. "
            "Perform an <strong>Athletics</strong> check. On success, <strong>Strike</strong> with "
            "force equal to what you've endured — the GM matches the narrative weight.",
            _crit(
                f"{C1} <strong>Exposed</strong> — they've overcommitted; your next blow finds the gap.",
                f"{C1} <strong>Rattled</strong> — the trade leaves them shaken and sloppy.",
            ),
            act=True,
        ),
    },
    {
        "id": 343,
        "key": "break-barbarian",
        "name": "Break",
        "card_type": "Act",
        "build": lambda: _ability(
            "Break",
            "There is no obstacle. There is only physics.",
            "Perform an <strong>Athletics</strong> check. On success, smash a piece of the "
            "<strong>Scene</strong> — an object, barrier, or structure is destroyed and the GM "
            "narrates one consequence on any enemy adjacent to it.",
            _crit(
                f"{C1} <strong>Exposed</strong> — splintered armor; the next clean hit lands."
            ),
            act=True,
        ),
    },
    {
        "id": 562,
        "key": "chuck-barbarian",
        "name": "Chuck",
        "card_type": "Act",
        "build": lambda: _ability(
            "Chuck",
            "You don't need a weapon when the room is already full of them.",
            'Choose a target. Perform an <strong>Athletics</strong> check — on success, it flies as '
            'far as the ladder shows. Each <span class="kw kw-crit">Crit</span> moves it one step higher.',
            _crit(
                f"{C1} <strong>Rattled</strong> — a thrown foe lands hard and scrambles to recover."
            ),
            act=True,
            extra_body=CHUCK_LADDER,
        ),
    },
    {
        "id": 349,
        "key": "endure-barbarian",
        "name": "Endure",
        "card_type": "Act",
        "build": lambda: _ability(
            "Endure",
            "You have taken worse.",
            "Perform an <strong>Endurance</strong> check. On success, name what you're pushing "
            "through — pain, fear, exhaustion — and shrug it off; add a Rage die to your pool.",
            _crit(
                f"{C1} Name two things you refuse to show; add two Rage dice."
            ),
            act=True,
        ),
    },
    {
        "id": 347,
        "key": "frenzy-barbarian",
        "name": "Frenzy",
        "card_type": "",
        "build": lambda: _ability(
            "Frenzy",
            "While in hand: the anger is running the show now.",
            f"While this card is in hand, every time you lose a {HD}, add a Rage die to your pool. "
            f"Every <strong>Strike</strong> gains {B1}. Your instinct has one gear — set aside any "
            "<strong>React</strong> cards in hand until you discard this card.",
            _crit(f"{C1} Add two Rage dice instead of one on the next hit you take."),
        ),
    },
    {
        "id": 340,
        "key": "into-the-fray-barbarian",
        "name": "Into the Fray",
        "card_type": "Act",
        "build": lambda: _ability(
            "Into the Fray",
            "You don't approach. You arrive.",
            "Perform an <strong>Athletics</strong> check. On success, close any distance and "
            "<strong>Strike</strong> before anyone can react.",
            _crit(
                f"{C1} An ally gains {B1} against this target.",
                f"{C1} <strong>Rattled</strong> — the charge came from nowhere; they can't set their feet.",
            ),
            act=True,
        ),
    },
    {
        "id": 342,
        "key": "reckless-strike-barbarian",
        "name": "Reckless Strike",
        "card_type": "Act",
        "build": lambda: _ability(
            "Reckless Strike",
            "You stop caring about what happens to you.",
            f"Perform an <strong>Athletics</strong> check with {B1}. On success, <strong>Strike</strong> "
            "with full force — you are <strong>Exposed</strong> — you left your guard wide; the GM "
            "has an honest opening until your next turn.",
            _crit(
                f"{C1} <strong>Rattled</strong> — the ferocity staggers them.",
                f"{C1} Add a Rage die to your pool.",
            ),
            act=True,
        ),
    },
    {
        "id": 346,
        "key": "retaliate-barbarian",
        "name": "Retaliate",
        "card_type": "React",
        "build": lambda: _ability(
            "Retaliate",
            "Pain is information. Your response is immediate.",
            f"When you lose a {HD}, perform an <strong>Athletics</strong> check — add a Rage die to "
            f"your pool, then roll it. On success, <strong>Strike</strong> whatever hit you using that "
            f"die as {B1}.",
            _crit(
                f"{C1} <strong>Rattled</strong> — they didn't expect you to answer back this fast."
            ),
            react=True,
        ),
    },
    {
        "id": 350,
        "key": "shockwave-barbarian",
        "name": "Shockwave",
        "card_type": "Act",
        "build": lambda: _ability(
            "Shockwave",
            "The ground disagrees with them.",
            "Perform an <strong>Athletics</strong> check. On success, slam the ground or a surface — "
            "every enemy nearby is knocked off balance; each is <strong>Rattled</strong>, fighting on "
            "unsteady footing this beat.",
            _crit(
                f"{C1} <strong>Rooted</strong> — one enemy's feet leave the ground wrong; they can't reposition."
            ),
            act=True,
        ),
    },
    {
        "id": 348,
        "key": "sundering-blow-barbarian",
        "name": "Sundering Blow",
        "card_type": "Act",
        "build": lambda: _ability(
            "Sundering Blow",
            "You don't just hit them. You compromise them.",
            "Perform an <strong>Athletics</strong> check. On success, <strong>Strike</strong> a target "
            "and open a weakness — they are <strong>Exposed</strong>, a flaw showing; allies who "
            f"<strong>Strike</strong> them this <strong>Scene</strong> gain {B1} on that Strike.",
            _crit(
                f"{C1} <strong>Exposed</strong> — the weakness you opened follows them into the next "
                "<strong>Scene</strong>.",
                f"{C1} You gain {B1} on your next <strong>Strike</strong> against this target.",
            ),
            act=True,
        ),
    },
]

CORE_PATCH = [
    (RAGE, build_rage_html),
    (RETRIBUTION, build_retribution_html),
]


def patch_cards(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c.get("Card_Key"): c for c in cards}
    batch: list[dict] = []

    for spec in CARDS:
        html = spec["build"]()
        card = by_key[spec["key"]]
        plain = f"> {strip_plain(html)}"
        card["HTML"] = html
        card["EffectText_Plain"] = plain
        card["Last_Rework_Date"] = DATE
        if spec["card_type"]:
            card["Card_Type"] = spec["card_type"]
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

    for meta, builder in CORE_PATCH:
        card = by_key[meta["key"]]
        html = builder()
        card["HTML"] = html
        card["EffectText_Plain"] = meta["effect_plain"]
        card["Card_Type"] = meta["card_type"]
        card["Last_Rework_Date"] = DATE
        batch.append(
            {
                "id": meta["id"],
                "Name": meta["name"],
                "Card_Key": meta["key"],
                "Card_Type": meta["card_type"],
                "HTML": html,
                "EffectText_Plain": meta["effect_plain"],
                "Last_Rework_Date": DATE,
            }
        )

    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Generated by scripts/build_barbarian_pool.py — do not edit manually. "
        f"Last updated: {DATE}\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof(cards: list[dict], keys: list[str]) -> None:
    css = open(ROOT / "primer-card-scope.css").read()
    chunks = []
    for key in keys:
        c = next(x for x in cards if x["Card_Key"] == key)
        chunks.append(
            f'<div class="sample"><div class="stag">{c["Name"]}</div>'
            f'<div class="cardwrap scope-ability cls-barbarian">{c["HTML"]}</div></div>'
        )
    PROOF_OUT.write_text(
        f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>Barbarian pool proof</title><style>{css}"
        "body{{background:#16110a;padding:24px;color:#f0e6cf;font-family:system-ui,sans-serif;}}"
        ".grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}}"
        ".stag{{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#e7d6ac;}}</style></head><body>"
        "<h1>Barbarian pool — narrative crit audit</h1>"
        f'<div class="grid">{"".join(chunks)}</div></body></html>',
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    cards = load_cards()
    cards, batch = patch_cards(cards)
    proof_keys = [s["key"] for s in CARDS] + [RAGE["key"], RETRIBUTION["key"]]

    print(f"Patched {len(batch)} Barbarian cards")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']}")

    if args.write or args.push:
        write_card_data(cards)
        write_proof(cards, proof_keys)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name}, {PROOF_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run — pass --write or --push")


if __name__ == "__main__":
    main()
