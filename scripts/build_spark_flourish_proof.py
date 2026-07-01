#!/usr/bin/env python3
"""Spark / Flourish overhaul — 8 model cards (2 per June 30 playtest class).

Spark lines: chip — action — describe how. Effects: [Skill] check to [intent], no On success.

Usage:
  python3 scripts/build_spark_flourish_proof.py              # proof HTML only
  python3 scripts/build_spark_flourish_proof.py --write      # + patch card-data.js
  python3 scripts/build_spark_flourish_proof.py --push       # + Baserow table 911939
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

PROOF_OUT = ROOT / "spark-flourish-proof.html"
BATCH_OUT = ROOT / "scripts" / "spark_flourish_batch.json"
DATE = "2026-07-01"

B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'


def spark_cost(n: int) -> str:
    glyphs = "".join('<span class="spark-glyph" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-glyphs" title="{n} Spark">{glyphs}</span>'


def fl_icon(color: str) -> str:
    kind = {"red": "off", "blue": "def", "green": "res"}[color]
    return f'<span class="fl-icon fl-icon-{kind}" aria-hidden="true"></span>'


def fl_chip(color: str, label: str) -> str:
    term, _, mag = label.rpartition(" ")
    if not mag.isdigit():
        term, mag = label, ""
    mag_html = f'<span class="fl-mag">{mag}</span>' if mag else ""
    return (
        f'<span class="fl-chip fl-chip-{color}">{fl_icon(color)}'
        f'<span class="fl-term">{term}</span>{mag_html}</span>'
    )


def spark_line(
    cost: int,
    keywords: list[tuple[str, str]],
    action: str,
    how: str = "",
) -> str:
    chips = []
    for i, (color, word) in enumerate(keywords):
        if i:
            chips.append('<span class="fl-plus">+</span>')
        chips.append(fl_chip(color, word))
    keys = f'<span class="spark-keys">{"".join(chips)}</span>'
    how_html = f' <span class="spark-how">— {how}</span>' if how else ""
    multi = " spark-multi" if len(keywords) > 1 else ""
    return (
        f'<div class="ci spark-line fl-{keywords[0][0]}{multi}">'
        f'{spark_cost(cost)}{keys}'
        f'<span class="ci-txt">— {action}{how_html}</span></div>'
    )


def spark_block(*rows: str) -> str:
    return (
        '<div class="csec spark-sec"><div class="clbl">Spark</div>'
        f'<div class="crow">{"".join(rows)}</div></div>'
    )


def ability_card(
    accent: str,
    idtag: str,
    name: str,
    flavor: str,
    effect: str,
    spark: str,
    *,
    act: bool = True,
) -> str:
    badge = '<span class="cap cap-neutral">Act</span>' if act else ""
    return (
        f'<div class="card acc-{accent}"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{badge}</div>'
        f'<div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div><div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>{spark}</div>'
        f'<div class="idtag">{idtag}</div><div class="tier-float"><span>t1</span></div></div>'
    )


CARDS: list[dict] = [
    {
        "id": 370,
        "key": "smite-paladin",
        "class": "Paladin",
        "name": "Smite",
        "build": lambda: ability_card(
            "paladin",
            "Paladin",
            "Smite",
            "You make yourself the problem they can't ignore.",
            "Perform a <strong>Presence</strong> check to draw an enemy's focus onto you — "
            "make them answer your challenge before they go for your allies.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Rattled 1")],
                    "Force a second foe to answer you",
                    "how do you wrench their eyes off your allies?",
                ),
            ),
        ),
    },
    {
        "id": 378,
        "key": "sacred-ground-paladin",
        "class": "Paladin",
        "name": "Condemn",
        "build": lambda: ability_card(
            "paladin",
            "Paladin",
            "Condemn",
            "You don't curse them. You recognize what they are.",
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Rattled 2")],
                    "Name what they did until the room stops",
                    "what word lands, and how do they show it?",
                ),
                spark_line(
                    1,
                    [("blue", "Boost 1")],
                    "Point an ally at the opening",
                    "how do you signal them in?",
                ),
                spark_line(
                    2,
                    [("red", "Rattled 1"), ("green", "Resolve 1")],
                    "Watch them buckle; stand taller",
                    "what cracks in them — what hardens in you?",
                ),
            ),
        ),
    },
    {
        "id": 342,
        "key": "reckless-strike-barbarian",
        "class": "Barbarian",
        "name": "Reckless Strike",
        "build": lambda: ability_card(
            "barbarian",
            "Barbarian",
            "Reckless Strike",
            "You stop caring about what happens to you.",
            f"Perform an <strong>Athletics</strong> check with {B1} to <strong>Strike</strong> with "
            "full force — leave your guard wide open until your next turn.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Sundered 2")],
                    "Break something they were counting on",
                    "what gives — guard, footing, or nerve?",
                ),
                spark_line(
                    2,
                    [("red", "Sundered 1"), ("blue", "Boost 1")],
                    "Clip them and shout the opening",
                    "what cracks; who answers your voice?",
                ),
            ),
        ),
    },
    {
        "id": 343,
        "key": "break-barbarian",
        "class": "Barbarian",
        "name": "Break",
        "build": lambda: ability_card(
            "barbarian",
            "Barbarian",
            "Break",
            "There is no obstacle. There is only physics.",
            "Perform an <strong>Athletics</strong> check to smash part of the <strong>Scene</strong> — "
            "destroy a barrier or structure and open a path.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Sundered 2")],
                    "Drop the wreckage on whoever's behind it",
                    "what collapses — and who gets caught?",
                ),
            ),
        ),
    },
    {
        "id": 300,
        "key": "sneak-attack-rogue",
        "class": "Rogue",
        "name": "Sneak Attack",
        "build": lambda: ability_card(
            "rogue",
            "Rogue",
            "Sneak Attack",
            "You weren't watching the right shadow.",
            "Perform a <strong>Stealth</strong> check to <strong>Strike</strong> a target "
            "unaware of you or occupied with an ally.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Stagger 1")],
                    "Strike while they're turned the wrong way",
                    "where were you a moment ago?",
                ),
                spark_line(
                    2,
                    [("red", "Stagger 2")],
                    "Take their legs out from under them",
                    "how do they hit the ground?",
                ),
            ),
        ),
    },
    {
        "id": 310,
        "key": "smoke-and-mirrors-rogue",
        "class": "Rogue",
        "name": "Smoke and Mirrors",
        "build": lambda: ability_card(
            "rogue",
            "Rogue",
            "Smoke and Mirrors",
            "Let them argue about what they saw.",
            "Perform a <strong>Deception</strong> check to plant a false impression — "
            "a sound, silhouette, or dropped object.",
            spark_block(
                spark_line(
                    1,
                    [("blue", "Boost 1")],
                    "Slip an ally through the hesitation",
                    "what did they think they saw?",
                ),
                spark_line(
                    2,
                    [("red", "Stagger 1"), ("blue", "Boost 1")],
                    "Feint one way; send a friend the other",
                    "what do they lunge at — who slips past?",
                ),
            ),
        ),
    },
    {
        "id": 312,
        "key": "eldritch-strike-warlock",
        "class": "Warlock",
        "name": "Eldritch Strike",
        "build": lambda: ability_card(
            "warlock",
            "Warlock",
            "Eldritch Strike",
            "The power is yours. So is the price.",
            f"Remove a {HD} from your pool and <strong>Strike</strong> at any range — add that die "
            "to your strike. Dark magic marks where to hit them next.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Hexed 1")],
                    "Burn a sigil where the next blow lands",
                    "what does it look like — how do they react?",
                ),
                spark_line(
                    2,
                    [("red", "Hexed 2")],
                    "Spread the mark across them",
                    "what does their guard look like when it fails?",
                ),
            ),
        ),
    },
    {
        "id": 316,
        "key": "feed-the-fire-warlock",
        "class": "Warlock",
        "name": "Feed the Fire",
        "build": lambda: ability_card(
            "warlock",
            "Warlock",
            "Feed the Fire",
            "More. Always more.",
            f"Remove a {HD} from your pool. Perform a <strong>Spellcast</strong> check — add that die "
            "to the roll — to pour more power into your next Act this <strong>Scene</strong>.",
            spark_block(
                spark_line(
                    1,
                    [("green", "Resolve 1")],
                    "Let the hunger pass through you",
                    "what steadiness returns — and where?",
                ),
                spark_line(
                    2,
                    [("green", "Resolve 1"), ("red", "Hexed 1")],
                    "Steady your breath; buckle the nearest foe",
                    "what floods out of you — how do they break?",
                ),
            ),
        ),
    },
]


def strip_plain(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", t).strip()


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
        "// Generated by scripts/build_spark_flourish_proof.py — do not edit manually. "
        f"Last updated: {DATE}\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof() -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_class: dict[str, list[dict]] = {}
    for spec in CARDS:
        by_class.setdefault(spec["class"], []).append(spec)

    sections = []
    for cls in ("Paladin", "Barbarian", "Rogue", "Warlock"):
        chunks = []
        for spec in by_class[cls]:
            html = spec["build"]()
            chunks.append(
                f'<div class="sample"><div class="stag">{spec["name"]}</div>'
                f'<div class="cardwrap scope-ability">{html}</div></div>'
            )
        sections.append(f'<h2>{cls}</h2><div class="grid">{"".join(chunks)}</div>')

    legend = """
<div class="legend">
  <span class="lg-item"><span class="lg-shape lg-off"></span> ▲ Offensive flourish</span>
  <span class="lg-item"><span class="lg-shape lg-def"></span> ■ Boost — extra die (any player, incl. you)</span>
  <span class="lg-item"><span class="lg-shape lg-res"></span> ● Resolve flourish</span>
  <span class="lg-item"><span class="spark-glyphs"><span class="spark-glyph"></span></span> Spark cost</span>
</div>
<div class="proc box">
  Each Spark line: <strong>chip — action — describe how</strong>. Bold clause = what you do; lighter
  clause = what to show the table (look, reaction, what gives way). GM judges keyword fit only.
</div>
"""

    PROOF_OUT.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Spark / Flourish proof — 8 model cards</title><style>"
        f"{css}"
        ".primer-cards .card{width:2.5in;height:3.5in;}"
        "body{background:#14100a;padding:28px;color:#f0e6cf;font-family:system-ui,sans-serif;}"
        "h1{font-size:18px;letter-spacing:1px;color:#e7d6ac;margin-bottom:4px;}"
        "h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;"
        "margin:28px 0 12px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}"
        "p.sub{color:#a08a5c;font-size:13px;margin-bottom:18px;max-width:52rem;line-height:1.45;}"
        ".legend{display:flex;flex-wrap:wrap;gap:14px 20px;margin-bottom:16px;font-size:12px;color:#d8c8a0;}"
        ".lg-item{display:flex;align-items:center;gap:6px;}"
        ".lg-shape{display:inline-block;width:9px;height:9px;}"
        ".lg-off{clip-path:polygon(50% 0%,0% 100%,100% 100%);background:#991B1B;}"
        ".lg-def{background:#2563EB;border-radius:1px;}"
        ".lg-res{border-radius:50%;background:#166534;}"
        ".box{background:#1b130b;border:1px solid #3a2c19;border-radius:8px;padding:12px 14px;"
        "font-size:12px;line-height:1.5;color:#d8c8a0;margin-bottom:22px;max-width:52rem;}"
        ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}"
        ".stag{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#c9b896;}"
        ".cardwrap{display:flex;justify-content:center;}"
        "</style></head><body>"
        "<h1>Spark / Flourish overhaul — live model cards</h1>"
        '<p class="sub">Eight abilities shipped to Card Studio — Effect + Spark on every card. '
        "Effect = check to intent; Spark = chip — action — describe how.</p>"
        f"{legend}"
        + "".join(sections)
        + "</body></html>",
        encoding="utf-8",
    )
    print(f"Wrote {PROOF_OUT} ({len(CARDS)} cards)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Patch card-data.js + proof HTML")
    parser.add_argument("--push", action="store_true", help="Also push to Baserow")
    args = parser.parse_args()

    write_proof()

    if args.write or args.push:
        cards = load_cards()
        cards, batch = patch_cards(cards)
        write_card_data(cards)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Patched {len(batch)} cards → {CARD_DATA.name}, {BATCH_OUT.name}")
        for item in batch:
            print(f"  row {item['id']}: {item['Card_Key']}")

    if args.push:
        batch = json.loads(BATCH_OUT.read_text(encoding="utf-8"))
        push_baserow(batch)


if __name__ == "__main__":
    main()
