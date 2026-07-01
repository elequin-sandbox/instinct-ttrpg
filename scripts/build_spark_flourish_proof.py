#!/usr/bin/env python3
"""Spark / Flourish overhaul — 8 model cards (2 per June 30 playtest class).

Spark lines: PbtA verb phrase (magnitude) + small italic prompt. No keyword pills.
Effects: [Skill] check to [intent], no On success.

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
DATE = "2026-07-02"

B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'

# clause: category (off|def|res), bold verb, tail text, optional magnitude
Clause = tuple[str, str, str, int | None]


def spark_pips(n: int) -> str:
    pips = "".join('<span class="spark-pip" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-pips" title="{n} Spark">{pips}</span>'


def verb_span(cat: str, verb: str) -> str:
    return f'<strong class="spark-v spark-v-{cat}">{verb}</strong>'


def mag_span(cat: str, n: int) -> str:
    return (
        f'<span class="spark-mag spark-mag-{cat}">'
        f'<span class="cat-icon cat-{cat}" aria-hidden="true"></span>'
        f'<span class="mag-n">({n})</span></span>'
    )


def clause_row(cat: str, verb: str, tail: str, mag: int | None = None) -> str:
    if mag is not None:
        suffix = f" {mag_span(cat, mag)}."
    elif tail.rstrip().endswith("then") or tail.rstrip().endswith(","):
        suffix = ""
    else:
        suffix = "."
    return f'<div class="spark-row">{verb_span(cat, verb)} {tail}{suffix}</div>'


def spark_line(cost: int, clauses: list[Clause], invite: str) -> str:
    rows = "".join(clause_row(c, v, t, m) for c, v, t, m in clauses)
    body = f'<div class="spark-body">{rows}<div class="spark-invite">{invite}</div></div>'
    return f'<div class="ci spark-entry">{spark_pips(cost)}{body}</div>'


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
                    [("off", "Jolt", "a second foe's attention onto you", 1)],
                    "Another enemy can't look at anyone but you.",
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
                    [("off", "Unmask", "them until the room goes quiet", 2)],
                    "The truth sits in their chest where swagger was.",
                ),
                spark_line(
                    1,
                    [("def", "Sound", "the charge for your allies", 1)],
                    "Your allies move on the conviction in your voice.",
                ),
                spark_line(
                    2,
                    [
                        ("off", "Shake", "their certainty, then", None),
                        ("res", "Plant", "your feet like stone", None),
                    ],
                    "They buckle; you don't.",
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
                    [("off", "Cleave", "through what they're holding", 2)],
                    "Their guard, footing, or nerve is broken.",
                ),
                spark_line(
                    2,
                    [
                        ("off", "Rupture", "their defenses as you pass, then", None),
                        ("def", "Hurl", "an ally above them", None),
                    ],
                    "Steel and surprise — your friend falls toward the opening.",
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
                    [("off", "Cascade", "wreckage onto whoever's hiding", 2)],
                    "Cover becomes rubble; someone wasn't fast enough.",
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
                    [("off", "Pierce", "from the blind side", 1)],
                    "They never saw which shadow moved.",
                ),
                spark_line(
                    2,
                    [("off", "Drop", "them hard", 2)],
                    "The floor meets them before their next thought.",
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
                    [("def", "Thread", "an ally through the hesitation", 1)],
                    "They lunge at the wrong shape.",
                ),
                spark_line(
                    2,
                    [
                        ("off", "Feint", "one way, then", None),
                        ("def", "Ghost", "a friend past them", None),
                    ],
                    "The wrong person moves; the right one is already gone.",
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
                    [("off", "Brand", "them with a crawling sigil", 1)],
                    "Everyone sees where the next blow belongs.",
                ),
                spark_line(
                    2,
                    [("off", "Unravel", "their guard across their body", 2)],
                    "Their stance comes apart like wet cloth.",
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
                    [("res", "Exhale", "the hunger for a breath", 1)],
                    "For a moment, you feel like a person again.",
                ),
                spark_line(
                    2,
                    [
                        ("res", "Ground", "yourself in the surge, then", None),
                        ("off", "Wither", "the nearest fool who stepped close", None),
                    ],
                    "Power leaves your hands; someone nearby pays for it.",
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
                f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
            )
        sections.append(f'<h2>{cls}</h2><div class="proof-grid">{"".join(chunks)}</div>')

    legend = """
<div class="legend">
  <span class="lg-item"><span class="cat-icon cat-off"></span> <strong class="spark-v-off">Verb</strong> — offensive</span>
  <span class="lg-item"><span class="cat-icon cat-def"></span> <strong class="spark-v-def">Verb</strong> — empower (Boost at table)</span>
  <span class="lg-item"><span class="cat-icon cat-res"></span> <strong class="spark-v-res">Verb</strong> — resolve</span>
  <span class="lg-item"><span class="spark-pip"></span> Spark cost (one pip per 6)</span>
</div>
<div class="proc box">
  Bold colored <strong>verb</strong> + ▲■● + <strong>(n)</strong> on single effects. Two-spark options split across
  lines — verb first. Italic line invites the story; global rules carry the math.
</div>
"""

    proof_css = """
body.proof-spark{background:#14100a;padding:28px 20px 48px;color:#f0e6cf;font-family:system-ui,sans-serif;}
body.proof-spark h1{font-size:20px;letter-spacing:1px;color:#e7d6ac;margin-bottom:6px;}
body.proof-spark h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;
  margin:32px 0 14px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}
body.proof-spark p.sub{color:#a08a5c;font-size:14px;margin-bottom:20px;max-width:52rem;line-height:1.5;}
body.proof-spark .legend{display:flex;flex-wrap:wrap;gap:14px 20px;margin-bottom:16px;font-size:13px;color:#d8c8a0;}
body.proof-spark .lg-item{display:flex;align-items:center;gap:6px;}
body.proof-spark .box{background:#1b130b;border:1px solid #3a2c19;border-radius:8px;padding:12px 14px;
  font-size:13px;line-height:1.55;color:#d8c8a0;margin-bottom:24px;max-width:52rem;}
body.proof-spark .proof-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:32px 24px;align-items:start;}
body.proof-spark .sample{display:flex;flex-direction:column;align-items:center;gap:10px;}
body.proof-spark .stag{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#c9b896;}
/* Screen-readable cards — full print frame, centered, no primer 0.58 shrink */
body.proof-spark .primer-cards{margin:0;display:flex;justify-content:center;width:100%;}
body.proof-spark .primer-cards .cardwrap{
  transform:none;
  margin-bottom:0;margin-right:0;
  width:auto;height:auto;
}
body.proof-spark .primer-cards .cardwrap .card{
  width:300px;height:420px;
  background:#f7f0e0;border:0.5px solid #c8a96e;box-shadow:6px 6px 0 #1a1a1a;
}
body.proof-spark .primer-cards .cbody{padding:7px 10px 5px;}
body.proof-spark .spark-sec .crow{gap:6px;}
body.proof-spark .spark-invite{font-size:8px;line-height:1.4;}
body.proof-spark .spark-row{font-size:9.5px;line-height:1.38;}
body.proof-spark .idtag{z-index:2;}
"""

    PROOF_OUT.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Spark / Flourish proof — 8 model cards</title><style>"
        f"{css}"
        f"{proof_css}"
        "</style></head><body class=\"proof-spark\">"
        "<h1>Spark / Flourish overhaul — model cards</h1>"
        '<p class="sub">Bold colored verbs, shape + (n) for magnitude, story invites instead of questions. '
        "Two-spark moves stack verbs on separate lines — Hurl implies Boost without saying it.</p>"
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
