#!/usr/bin/env python3
"""Spark / Flourish overhaul — proof-page builder (8 model cards, 2 per class).

Locked design (Annie, July 2026):
- Each natural 6 on the *initial* roll earns 1 Spark.
- The 6 stays in the pool. Per Spark: roll the bonus die OR spend on a Flourish.
- Spend timing: right after the first handful, simultaneous with pulling 1s.
- Fiction-fit gate is global (GM agrees keyword fits) — not repeated on cards.
- Spark cost = glyph icon(s), not numbers. Keyword chips carry magnitude; gloss is narrative only.
- Color-blind: shape icon (▲ offensive, ■ Boost/defensive, ● resolve) + hue.

Usage:
  python3 scripts/build_spark_flourish_proof.py --write
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROOF_OUT = ROOT / "spark-flourish-proof.html"

B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'


def spark_cost(n: int) -> str:
    glyphs = "".join('<span class="spark-glyph" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-glyphs" title="{n} Spark">{glyphs}</span>'


def fl_icon(color: str) -> str:
    kind = {"red": "off", "blue": "def", "green": "res"}[color]
    return f'<span class="fl-icon fl-icon-{kind}" aria-hidden="true"></span>'


def fl_chip(color: str, label: str) -> str:
    """Keyword chip: 'Rattled 2' → shape + term + magnitude badge."""
    term, _, mag = label.rpartition(" ")
    if not mag.isdigit():
        term, mag = label, ""
    mag_html = f'<span class="fl-mag">{mag}</span>' if mag else ""
    return (
        f'<span class="fl-chip fl-chip-{color}">{fl_icon(color)}'
        f'<span class="fl-term">{term}</span>{mag_html}</span>'
    )


def spark_line(cost: int, keywords: list[tuple[str, str]], gloss: str) -> str:
    chips = []
    for i, (color, word) in enumerate(keywords):
        if i:
            chips.append('<span class="fl-plus">+</span>')
        chips.append(fl_chip(color, word))
    keys = f'<span class="spark-keys">{"".join(chips)}</span>'
    multi = " spark-multi" if len(keywords) > 1 else ""
    return (
        f'<div class="ci spark-line fl-{keywords[0][0]}{multi}">'
        f'{spark_cost(cost)}{keys}<span class="ci-txt">{gloss}</span></div>'
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
        "class": "Paladin",
        "name": "Smite",
        "html": ability_card(
            "paladin",
            "Paladin",
            "Smite",
            "You make yourself the problem they can't ignore.",
            "Perform a <strong>Presence</strong> check. On success, draw an enemy's focus onto you — "
            "they must answer your challenge before acting on anyone else this beat.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Rattled 1")],
                    "Your challenge echoes off a second foe — they falter, fixing on you instead.",
                ),
            ),
        ),
    },
    {
        "class": "Paladin",
        "name": "Condemn",
        "html": ability_card(
            "paladin",
            "Paladin",
            "Condemn",
            "You don't curse them. You recognize what they are.",
            "Perform a <strong>Faith</strong> check. On success, speak what they have done aloud — "
            "the truth lands. They must choose: <strong>Stand down</strong> or <strong>Press on</strong> "
            "while everyone watches.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Rattled 2")],
                    "The word hangs in the air; their certainty splinters in front of the room.",
                ),
                spark_line(
                    1,
                    [("blue", "Boost 1")],
                    "Allies hear the steel in your voice and surge into the opening.",
                ),
                spark_line(
                    2,
                    [("red", "Rattled 1"), ("green", "Resolve 1")],
                    "They stagger under the weight of it — and you feel your own spine straighten.",
                ),
            ),
        ),
    },
    {
        "class": "Barbarian",
        "name": "Reckless Strike",
        "html": ability_card(
            "barbarian",
            "Barbarian",
            "Reckless Strike",
            "You stop caring about what happens to you.",
            f"Perform an <strong>Athletics</strong> check with {B1}. On success, "
            "<strong>Strike</strong> with full force — your guard stays wide open until your next turn.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Sundered 2")],
                    "Something gives — bone, bark, or bravado — and they won't hold together the same.",
                ),
                spark_line(
                    2,
                    [("red", "Sundered 1"), ("blue", "Boost 1")],
                    "You clip them on the way through and roar the opening for whoever follows.",
                ),
            ),
        ),
    },
    {
        "class": "Barbarian",
        "name": "Break",
        "html": ability_card(
            "barbarian",
            "Barbarian",
            "Break",
            "There is no obstacle. There is only physics.",
            "Perform an <strong>Athletics</strong> check. On success, smash part of the "
            "<strong>Scene</strong> — a barrier or structure is destroyed, opening a path or "
            "clearing cover.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Sundered 2")],
                    "The wreckage finds a body; cover becomes rubble and someone screams.",
                ),
            ),
        ),
    },
    {
        "class": "Rogue",
        "name": "Sneak Attack",
        "html": ability_card(
            "rogue",
            "Rogue",
            "Sneak Attack",
            "You weren't watching the right shadow.",
            "Perform a <strong>Stealth</strong> check. On success, <strong>Strike</strong> a target "
            "that is unaware of you or occupied with an ally.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Stagger 1")],
                    "They're still turning toward the wrong threat when you land.",
                ),
                spark_line(
                    2,
                    [("red", "Stagger 2")],
                    "Both feet leave the floor — when they find them again, the fight moved on.",
                ),
            ),
        ),
    },
    {
        "class": "Rogue",
        "name": "Smoke and Mirrors",
        "html": ability_card(
            "rogue",
            "Rogue",
            "Smoke and Mirrors",
            "Let them argue about what they saw.",
            "Perform a <strong>Deception</strong> check. On success, plant a false impression — "
            "a sound, silhouette, or dropped object. Enemies in the area hesitate.",
            spark_block(
                spark_line(
                    1,
                    [("blue", "Boost 1")],
                    "Your ally moves on the hesitation you planted — a half-step ahead of the lie.",
                ),
                spark_line(
                    2,
                    [("red", "Stagger 1"), ("blue", "Boost 1")],
                    "They lunge at the wrong shadow; your friend is already through the gap.",
                ),
            ),
        ),
    },
    {
        "class": "Warlock",
        "name": "Eldritch Strike",
        "html": ability_card(
            "warlock",
            "Warlock",
            "Eldritch Strike",
            "The power is yours. So is the price.",
            f"Remove a {HD} from your pool and <strong>Strike</strong> at any range — add that die "
            "to your strike. On success, dark magic marks exactly where to hit them again.",
            spark_block(
                spark_line(
                    1,
                    [("red", "Hexed 1")],
                    "The sigil crawls under their skin — everyone sees where to strike next.",
                ),
                spark_line(
                    2,
                    [("red", "Hexed 2")],
                    "The brand spreads; their guard looks like tissue paper from here.",
                ),
            ),
        ),
    },
    {
        "class": "Warlock",
        "name": "Feed the Fire",
        "html": ability_card(
            "warlock",
            "Warlock",
            "Feed the Fire",
            "More. Always more.",
            f"Remove a {HD} from your pool. Perform a <strong>Spellcast</strong> check — add that die "
            "to the roll. On success, your next Act this <strong>Scene</strong> meets no resistance.",
            spark_block(
                spark_line(
                    1,
                    [("green", "Resolve 1")],
                    "The hunger clears for a breath — you remember you still have a body.",
                ),
                spark_line(
                    2,
                    [("green", "Resolve 1"), ("red", "Hexed 1")],
                    "Power ripples outward; a nearby foe buckles as the spell eats their footing.",
                ),
            ),
        ),
    },
]


def write_proof() -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_class: dict[str, list[dict]] = {}
    for card in CARDS:
        by_class.setdefault(card["class"], []).append(card)

    sections = []
    for cls in ("Paladin", "Barbarian", "Rogue", "Warlock"):
        chunks = []
        for card in by_class[cls]:
            chunks.append(
                f'<div class="sample"><div class="stag">{card["name"]}</div>'
                f'<div class="cardwrap scope-ability">{card["html"]}</div></div>'
            )
        sections.append(f'<h2>{cls}</h2><div class="grid">{"".join(chunks)}</div>')

    legend = """
<div class="legend">
  <span class="lg-item"><span class="lg-shape lg-off"></span> ▲ Offensive — Sunder, Rattle, Stagger…</span>
  <span class="lg-item"><span class="lg-shape lg-def"></span> ■ Boost — extra die to any player (self included)</span>
  <span class="lg-item"><span class="lg-shape lg-res"></span> ● Resolve — recover Resolve / steadiness</span>
  <span class="lg-item"><span class="spark-glyphs"><span class="spark-glyph"></span></span> Spark — spend instead of rolling that bonus die</span>
</div>
<div class="proc box">
  <strong>On-card rule:</strong> chips name the flourish; italic gloss is how <em>you</em> describe it landing.
  Magnitude is global — <strong>Rattled 2</strong> means what Rattling means at the table. GM only judges
  whether the keyword fits the objective (not repeated per card).
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
        "<h1>Spark / Flourish overhaul — model cards</h1>"
        '<p class="sub">Eight abilities for the June 30 playtest classes. Spark glyphs = cost; '
        "colored chips = guaranteed flourish; italic line = your narration hook.</p>"
        f"{legend}"
        + "".join(sections)
        + "</body></html>",
        encoding="utf-8",
    )
    print(f"Wrote {PROOF_OUT} ({len(CARDS)} cards)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write proof HTML")
    args = parser.parse_args()
    write_proof()


if __name__ == "__main__":
    main()
