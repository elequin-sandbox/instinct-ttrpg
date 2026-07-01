#!/usr/bin/env python3
"""Spark / Flourish overhaul — 8 model cards + Condemn variant lab on proof page.

Spark v4: discrete choice blocks, shape-before-verb, heavier pips, → combo chain,
invite em-dash, cooler Spark label. Condemn gets multiple language/visual variants on proof only.

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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import CARD_DATA, load_cards, push_baserow  # noqa: E402

PROOF_OUT = ROOT / "spark-flourish-proof.html"
BATCH_OUT = ROOT / "scripts" / "spark_flourish_batch.json"
DATE = "2026-07-03"

B1 = '<span class="kw kw-boost">Boost 1</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'

Cat = Literal["off", "def", "res"]
Clause = tuple[Cat, str, str, int | None]
PipStyle = Literal["bar", "dot"]


@dataclass
class SparkStyle:
    pip_style: PipStyle = "bar"
    cool_label: bool = False


@dataclass
class SparkLineSpec:
    cost: int
    clauses: list[Clause]
    invite: str
    invite2: str | None = None


def cat_icon(cat: Cat) -> str:
    return f'<span class="cat-icon cat-{cat}" aria-hidden="true"></span>'


def verb_span(cat: Cat, verb: str) -> str:
    return f'<strong class="spark-v spark-v-{cat}">{verb}</strong>'


def mag_span(cat: Cat, n: int) -> str:
    return f'<span class="spark-mag spark-mag-{cat}"><span class="mag-n">({n})</span></span>'


def entry_border_class(clauses: list[Clause]) -> str:
    if len(clauses) > 1:
        cats = {c[0] for c in clauses}
        return "spark-entry-mix" if len(cats) > 1 else f"spark-entry-{clauses[0][0]}"
    return f"spark-entry-{clauses[0][0]}"


def spark_pips(n: int, style: PipStyle) -> str:
    dot_cls = " spark-pips-dots" if style == "dot" else ""
    pips = "".join('<span class="spark-pip" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-pips{dot_cls}" title="{n} Spark">{pips}</span>'


def invite_html(text: str, *, second: bool = False) -> str:
    cls = "spark-invite spark-invite-2" if second else "spark-invite"
    return (
        f'<div class="{cls}">'
        f'<span class="invite-lead" aria-hidden="true">—</span> {text}</div>'
    )


def clause_row(
    cat: Cat,
    verb: str,
    tail: str,
    mag: int | None = None,
    *,
    combo_first: bool = False,
) -> str:
    icon = cat_icon(cat)
    v = verb_span(cat, verb)
    clean = re.sub(r",?\s*then\s*$", "", tail, flags=re.I) if combo_first else tail
    if mag is not None:
        return f'<div class="spark-row">{icon}{v} {clean} {mag_span(cat, mag)}.</div>'
    end = "" if clean.rstrip().endswith(".") else "."
    return f'<div class="spark-row">{icon}{v} {clean}{end}</div>'


def combo_connector() -> str:
    return '<div class="spark-chain" aria-hidden="true"><span class="spark-link">→</span></div>'


def spark_line(spec: SparkLineSpec, style: SparkStyle) -> str:
    rows: list[str] = []
    multi = len(spec.clauses) > 1
    for i, (cat, verb, tail, mag) in enumerate(spec.clauses):
        if i > 0 and multi:
            rows.append(combo_connector())
        rows.append(
            clause_row(
                cat,
                verb,
                tail,
                mag,
                combo_first=multi and i == 0,
            )
        )
    if spec.invite2:
        rows.append(invite_html(spec.invite))
        rows.append(invite_html(spec.invite2, second=True))
    else:
        rows.append(invite_html(spec.invite))
    body = f'<div class="spark-body">{"".join(rows)}</div>'
    border = entry_border_class(spec.clauses)
    return (
        f'<div class="ci spark-entry {border}">'
        f'{spark_pips(spec.cost, style.pip_style)}{body}</div>'
    )


def spark_block(style: SparkStyle, *lines: SparkLineSpec) -> str:
    lbl_cls = " spark-lbl-cool" if style.cool_label else ""
    rendered = "".join(spark_line(line, style) for line in lines)
    return (
        f'<div class="csec spark-sec{lbl_cls}"><div class="clbl">Spark</div>'
        f'<div class="crow">{rendered}</div></div>'
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


SPARK_V4 = SparkStyle()


def condemn_spark_canonical() -> str:
    return spark_block(
        SPARK_V4,
        SparkLineSpec(
            1,
            [("off", "Unmask", "them until the room goes quiet", 2)],
            "The truth sits in their chest where swagger was.",
        ),
        SparkLineSpec(
            1,
            [("def", "Sound", "the charge for your allies", 1)],
            "Your allies move on the conviction in your voice.",
        ),
        SparkLineSpec(
            2,
            [("off", "Shake", "their certainty, then", None), ("res", "Plant", "your feet like stone", None)],
            "They buckle; you don't.",
        ),
    )


def condemn_spark_terse() -> str:
    return spark_block(
        SPARK_V4,
        SparkLineSpec(
            1,
            [("off", "Bare", "them before the room", 2)],
            "Swagger drains out of them.",
        ),
        SparkLineSpec(
            1,
            [("def", "Rally", "your allies with one sentence", 1)],
            "They answer your voice, not their fear.",
        ),
        SparkLineSpec(
            2,
            [("off", "Unseat", "their certainty", None), ("res", "Anchor", "yourself in place", None)],
            "They fold. You hold.",
        ),
    )


def condemn_spark_two_door() -> str:
    """Density cap: two spark entries only."""
    return spark_block(
        SPARK_V4,
        SparkLineSpec(
            1,
            [("off", "Unmask", "them until the room goes quiet", 2)],
            "Swagger gives way to what they really are.",
        ),
        SparkLineSpec(
            2,
            [("off", "Shake", "their certainty", None), ("res", "Plant", "your feet like stone", None)],
            "They buckle; you don't.",
        ),
    )


def condemn_spark_split_invites() -> str:
    return spark_block(
        SPARK_V4,
        SparkLineSpec(
            1,
            [("off", "Unmask", "them until the room goes quiet", 2)],
            "The truth sits in their chest where swagger was.",
        ),
        SparkLineSpec(
            1,
            [("def", "Sound", "the charge for your allies", 1)],
            "Your allies move on the conviction in your voice.",
        ),
        SparkLineSpec(
            2,
            [("off", "Shake", "their certainty, then", None), ("res", "Plant", "your feet like stone", None)],
            "Their certainty cracks.",
            invite2="You stand unmoved.",
        ),
    )


def condemn_spark_poetic() -> str:
    return spark_block(
        SPARK_V4,
        SparkLineSpec(
            1,
            [("off", "Lay bare", "what they have done", 2)],
            "The room holds its breath on your words.",
        ),
        SparkLineSpec(
            1,
            [("def", "Proclaim", "who stands with you", 1)],
            "Steel answers when your voice does.",
        ),
        SparkLineSpec(
            2,
            [("off", "Unseat", "their bravado", None), ("res", "Root", "yourself in the oath", None)],
            "Their knees remember gravity; yours remember stone.",
        ),
    )


def condemn_spark_dot_pips() -> str:
    return spark_block(
        SparkStyle(pip_style="dot"),
        SparkLineSpec(
            1,
            [("off", "Unmask", "them until the room goes quiet", 2)],
            "The truth sits in their chest where swagger was.",
        ),
        SparkLineSpec(
            1,
            [("def", "Sound", "the charge for your allies", 1)],
            "Your allies move on the conviction in your voice.",
        ),
        SparkLineSpec(
            2,
            [("off", "Shake", "their certainty, then", None), ("res", "Plant", "your feet like stone", None)],
            "They buckle; you don't.",
        ),
    )


def condemn_spark_cool_label() -> str:
    return spark_block(
        SparkStyle(cool_label=True),
        SparkLineSpec(
            1,
            [("off", "Unmask", "them until the room goes quiet", 2)],
            "The truth sits in their chest where swagger was.",
        ),
        SparkLineSpec(
            1,
            [("def", "Sound", "the charge for your allies", 1)],
            "Your allies move on the conviction in your voice.",
        ),
        SparkLineSpec(
            2,
            [("off", "Shake", "their certainty, then", None), ("res", "Plant", "your feet like stone", None)],
            "They buckle; you don't.",
        ),
    )


def condemn_spark_kitchen_sink() -> str:
    """Terse copy + dot pips + cool label + split combo invites."""
    return spark_block(
        SparkStyle(pip_style="dot", cool_label=True),
        SparkLineSpec(
            1,
            [("off", "Bare", "them before the room", 2)],
            "Swagger drains out of them.",
        ),
        SparkLineSpec(
            1,
            [("def", "Rally", "your allies with one sentence", 1)],
            "They answer your voice, not their fear.",
        ),
        SparkLineSpec(
            2,
            [("off", "Unseat", "their certainty", None), ("res", "Anchor", "yourself in place", None)],
            "They fold.",
            invite2="You hold.",
        ),
    )


CONDEMN_VARIANTS: list[dict] = [
    {
        "slug": "canonical",
        "label": "A · v4 Canonical (ships)",
        "note": "Production — all v4 visual fixes, current copy.",
        "flavor": "You don't curse them. You recognize what they are.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches."
        ),
        "spark": condemn_spark_canonical,
    },
    {
        "slug": "terse",
        "label": "B · Terse language",
        "note": "Shorter effect + punchier verbs (Bare, Rally, Unseat/Anchor).",
        "flavor": "You name what they are, not what you wish.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak their crime aloud — "
            "the room goes still."
        ),
        "spark": condemn_spark_terse,
    },
    {
        "slug": "two-door",
        "label": "C · Two-door (density cap)",
        "note": "Only two Spark entries — drops the 1-spark Rally line.",
        "flavor": "You don't curse them. You recognize what they are.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches."
        ),
        "spark": condemn_spark_two_door,
    },
    {
        "slug": "split-invites",
        "label": "D · Split combo invites",
        "note": "Same copy; combo row gets two em-dash invites.",
        "flavor": "You don't curse them. You recognize what they are.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches."
        ),
        "spark": condemn_spark_split_invites,
    },
    {
        "slug": "poetic",
        "label": "E · Poetic language",
        "note": "More literary verbs + longer invites.",
        "flavor": "Judgment is not a spell. It is a mirror held steady.",
        "effect": (
            "Perform a <strong>Faith</strong> check to name their sin where witnesses stand — "
            "let the <strong>Scene</strong> remember it."
        ),
        "spark": condemn_spark_poetic,
    },
    {
        "slug": "dot-pips",
        "label": "F · Dot pips (visual)",
        "note": "Mana-style circular cost pips instead of bars.",
        "flavor": "You don't curse them. You recognize what they are.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches."
        ),
        "spark": condemn_spark_dot_pips,
    },
    {
        "slug": "cool-label",
        "label": "G · Cool Spark label",
        "note": "Slate section label — less gold competition with header.",
        "flavor": "You don't curse them. You recognize what they are.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches."
        ),
        "spark": condemn_spark_cool_label,
    },
    {
        "slug": "kitchen-sink",
        "label": "H · Kitchen sink alt",
        "note": "Terse + dot pips + cool label + split combo invites.",
        "flavor": "You name what they are, not what you wish.",
        "effect": (
            "Perform a <strong>Faith</strong> check to speak their crime aloud — "
            "the room goes still."
        ),
        "spark": condemn_spark_kitchen_sink,
    },
]


def build_condemn_variant(spec: dict) -> str:
    return ability_card(
        "paladin",
        "Paladin",
        "Condemn",
        spec["flavor"],
        spec["effect"],
        spec["spark"](),
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
                SPARK_V4,
                SparkLineSpec(
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
        "build": lambda: build_condemn_variant(CONDEMN_VARIANTS[0]),
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
                SPARK_V4,
                SparkLineSpec(
                    1,
                    [("off", "Cleave", "through what they're holding", 2)],
                    "Their guard, footing, or nerve is broken.",
                ),
                SparkLineSpec(
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
                SPARK_V4,
                SparkLineSpec(
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
                SPARK_V4,
                SparkLineSpec(
                    1,
                    [("off", "Pierce", "from the blind side", 1)],
                    "They never saw which shadow moved.",
                ),
                SparkLineSpec(
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
                SPARK_V4,
                SparkLineSpec(
                    1,
                    [("def", "Thread", "an ally through the hesitation", 1)],
                    "They lunge at the wrong shape.",
                ),
                SparkLineSpec(
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
                SPARK_V4,
                SparkLineSpec(
                    1,
                    [("off", "Brand", "them with a crawling sigil", 1)],
                    "Everyone sees where the next blow belongs.",
                ),
                SparkLineSpec(
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
                SPARK_V4,
                SparkLineSpec(
                    1,
                    [("res", "Exhale", "the hunger for a breath", 1)],
                    "For a moment, you feel like a person again.",
                ),
                SparkLineSpec(
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

    condemn_chunks = []
    for var in CONDEMN_VARIANTS:
        html = build_condemn_variant(var)
        condemn_chunks.append(
            f'<div class="sample variant-sample">'
            f'<div class="stag">{var["label"]}</div>'
            f'<div class="vnote">{var["note"]}</div>'
            f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
        )
    condemn_section = (
        '<h2 id="condemn-lab">Condemn — language &amp; visual lab</h2>'
        '<p class="lab-intro">Eight Condemn variants side-by-side. <strong>A</strong> ships to '
        "card-data / Baserow; B–H are proof-only experiments.</p>"
        f'<div class="proof-grid variant-grid">{"".join(condemn_chunks)}</div>'
    )

    legend = """
<div class="legend">
  <span class="lg-item"><span class="cat-icon cat-off"></span> <strong class="spark-v-off">Verb</strong> — offensive</span>
  <span class="lg-item"><span class="cat-icon cat-def"></span> <strong class="spark-v-def">Verb</strong> — empower</span>
  <span class="lg-item"><span class="cat-icon cat-res"></span> <strong class="spark-v-res">Verb</strong> — resolve</span>
  <span class="lg-item"><span class="spark-pip"></span> Spark cost (bar pips)</span>
  <span class="lg-item"><span class="spark-pips spark-pips-dots"><span class="spark-pip"></span></span> dot pips (variant)</span>
</div>
<div class="proc box">
  <strong>v4:</strong> shape-before-verb + <strong>(n)</strong> · tinted choice blocks · heavier bar pips ·
  <strong>→</strong> combo chain · em-dash story invites · cooler Spark label. Combos omit <strong>(n)</strong>.
</div>
"""

    proof_css = """
body.proof-spark{background:#14100a;padding:28px 20px 48px;color:#f0e6cf;font-family:system-ui,sans-serif;}
body.proof-spark h1{font-size:20px;letter-spacing:1px;color:#e7d6ac;margin-bottom:6px;}
body.proof-spark h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;
  margin:32px 0 14px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}
body.proof-spark p.sub,body.proof-spark p.lab-intro{color:#a08a5c;font-size:14px;margin-bottom:20px;max-width:52rem;line-height:1.5;}
body.proof-spark .legend{display:flex;flex-wrap:wrap;gap:14px 20px;margin-bottom:16px;font-size:13px;color:#d8c8a0;}
body.proof-spark .lg-item{display:flex;align-items:center;gap:6px;}
body.proof-spark .box{background:#1b130b;border:1px solid #3a2c19;border-radius:8px;padding:12px 14px;
  font-size:13px;line-height:1.55;color:#d8c8a0;margin-bottom:24px;max-width:52rem;}
body.proof-spark .proof-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:32px 24px;align-items:start;}
body.proof-spark .variant-grid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr));}
body.proof-spark .sample{display:flex;flex-direction:column;align-items:center;gap:10px;}
body.proof-spark .variant-sample .vnote{font-size:11px;color:#8a7a5c;text-align:center;max-width:280px;line-height:1.45;}
body.proof-spark .stag{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#c9b896;text-align:center;}
body.proof-spark .primer-cards{margin:0;display:flex;justify-content:center;width:100%;}
body.proof-spark .primer-cards .cardwrap{transform:none;margin-bottom:0;margin-right:0;width:auto;height:auto;}
body.proof-spark .primer-cards .cardwrap .card{
  width:300px;height:420px;
  background:#f7f0e0;border:0.5px solid #c8a96e;box-shadow:6px 6px 0 #1a1a1a;
}
body.proof-spark .primer-cards .cbody{padding:7px 10px 5px;}
body.proof-spark .idtag{z-index:2;}
"""

    PROOF_OUT.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Spark v4 proof — 8 model cards + Condemn lab</title><style>"
        f"{css}"
        f"{proof_css}"
        "</style></head><body class=\"proof-spark\">"
        "<h1>Spark v4 — model cards + Condemn lab</h1>"
        '<p class="sub">Discrete Spark choice blocks, shape-before-verb, combo <strong>→</strong> chains, '
        "and em-dash story invites. Scroll to <a href=\"#condemn-lab\" style=\"color:#e7d6ac\">Condemn lab</a> "
        "for eight language/visual variants.</p>"
        f"{legend}"
        + "".join(sections)
        + condemn_section
        + "</body></html>",
        encoding="utf-8",
    )
    print(f"Wrote {PROOF_OUT} ({len(CARDS)} cards + {len(CONDEMN_VARIANTS)} Condemn variants)")


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
