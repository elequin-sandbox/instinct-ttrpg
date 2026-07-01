#!/usr/bin/env python3
"""Spark / Flourish — 8 model cards + Rogue variant lab (Smoke and Mirrors).

Spark v5: exchange table (spend icon ⇄ yield shapes), magnitude as shape pips,
flowing combo sentences (no arrows), max 2 entries, optional invites.
Proof: pay-icon lab + heritage timeline on Smoke and Mirrors.

Usage:
  python3 scripts/build_spark_flourish_proof.py --write
  python3 scripts/build_spark_flourish_proof.py --push
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
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
XchLayout = Literal["row", "compact", "table"]
PayIcon = Literal["spark", "bonus", "hollow", "bolt", "bar", "die-six"]


@dataclass
class SparkStyle:
    xch_layout: XchLayout = "row"
    show_invites: bool = True
    phrase_first: bool = False
    pay_icon: PayIcon = "spark"


@dataclass
class SparkLineSpec:
    cost: int
    clauses: list[Clause]
    invite: str | None = None
    combo_join: str = "while you"


def verb_span(cat: Cat, verb: str) -> str:
    return f'<strong class="spark-v spark-v-{cat}">{verb}</strong>'


def shape_pip(cat: Cat) -> str:
    return f'<span class="pip-shape cat-{cat}" aria-hidden="true"></span>'


def mag_pips(cat: Cat, n: int) -> str:
    shapes = "".join(shape_pip(cat) for _ in range(n))
    return f'<span class="mag-pips mag-pips-{cat}" aria-label="magnitude {n}">{shapes}</span>'


def yield_icons(clauses: list[Clause]) -> str:
    parts: list[str] = []
    for cat, _verb, _tail, mag in clauses:
        if mag is not None and mag > 0:
            parts.append(mag_pips(cat, mag))
        else:
            parts.append(shape_pip(cat))
    return "".join(parts)


def pay_icons(cost: int, icon: PayIcon) -> str:
    pieces: list[str] = []
    for _ in range(cost):
        if icon == "spark":
            pieces.append('<span class="pay-spark" aria-hidden="true"></span>')
        elif icon == "bonus":
            pieces.append(
                '<span class="pay-bonus" aria-hidden="true" title="bonus die">'
                '<span class="pay-plus">+</span></span>'
            )
        elif icon == "hollow":
            pieces.append('<span class="pay-hollow" aria-hidden="true" title="roll bonus die"></span>')
        elif icon == "bolt":
            pieces.append('<span class="pay-bolt" aria-hidden="true"></span>')
        elif icon == "bar":
            pieces.append('<span class="pay-bar" aria-hidden="true"></span>')
        else:
            pieces.append('<span class="spark-die" aria-hidden="true">6</span>')
    titles = {
        "spark": "Spark",
        "bonus": "bonus die",
        "hollow": "bonus roll",
        "bolt": "Spark",
        "bar": "Spark",
        "die-six": "6 (misleading)",
    }
    return f'<span class="xch-pay" title="{cost} {titles[icon]}">{"".join(pieces)}</span>'


def exchange_row(cost: int, clauses: list[Clause], layout: XchLayout, pay_icon: PayIcon) -> str:
    pay = pay_icons(cost, pay_icon)
    yld = f'<span class="xch-yield">{yield_icons(clauses)}</span>'
    mid = '<span class="xch-mid" aria-hidden="true">⇄</span>'
    if layout == "compact":
        return f'<div class="spark-xch spark-xch-compact">{pay}{mid}{yld}</div>'
    if layout == "table":
        spend_lbl = "Roll" if pay_icon in ("bonus", "hollow") else "Spark"
        return (
            '<div class="spark-xch spark-xch-table">'
            f'<div class="xch-th">{spend_lbl}</div><div class="xch-th">Yield</div>'
            f'<div class="xch-td">{pay}</div><div class="xch-td">{yld}</div>'
            "</div>"
        )
    return f'<div class="spark-xch spark-xch-row">{pay}{mid}{yld}</div>'


def flowing_phrase(clauses: list[Clause], combo_join: str) -> str:
    if len(clauses) == 1:
        cat, verb, tail, _mag = clauses[0]
        end = "" if tail.rstrip().endswith((".", "!", "?")) else "."
        return f"{verb_span(cat, verb)} {tail}{end}"

    c0, v0, t0, _ = clauses[0]
    t0 = re.sub(r",?\s*then\s*$", "", t0, flags=re.I).rstrip("., ")
    c1, v1, t1, _ = clauses[1]
    end = "" if t1.rstrip().endswith((".", "!", "?")) else "."
    return (
        f"{verb_span(c0, v0)} {t0}, {combo_join} "
        f"{verb_span(c1, v1)} {t1}{end}"
    )


def entry_border_class(clauses: list[Clause]) -> str:
    if len(clauses) > 1:
        cats = {c[0] for c in clauses}
        return "spark-entry-mix" if len(cats) > 1 else f"spark-entry-{clauses[0][0]}"
    return f"spark-entry-{clauses[0][0]}"


def invite_html(text: str | None) -> str:
    if not text:
        return ""
    return f'<div class="spark-invite">{text}</div>'


def spark_line(spec: SparkLineSpec, style: SparkStyle) -> str:
    xch = exchange_row(spec.cost, spec.clauses, style.xch_layout, style.pay_icon)
    phrase = flowing_phrase(spec.clauses, spec.combo_join)
    invite = invite_html(spec.invite) if style.show_invites else ""
    if style.phrase_first:
        inner = f'<div class="spark-phrase">{phrase}</div>{xch}{invite}'
    else:
        inner = f'{xch}<div class="spark-phrase">{phrase}</div>{invite}'
    body = f'<div class="spark-body">{inner}</div>'
    border = entry_border_class(spec.clauses)
    pf = " spark-entry-phrase-first" if style.phrase_first else ""
    return f'<div class="ci spark-entry {border}{pf}">{body}</div>'


def spark_block(style: SparkStyle, *lines: SparkLineSpec) -> str:
    rendered = "".join(spark_line(line, style) for line in lines)
    return (
        '<div class="csec spark-sec"><div class="clbl">Spark</div>'
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


SPARK_V5 = SparkStyle()


# ── Smoke and Mirrors — Rogue variant lab (proof only) ─────────────────────

SAM_EFFECT = (
    "Perform a <strong>Deception</strong> check to plant a false impression — "
    "a sound, silhouette, or dropped object."
)

SAM_LINES = (
    SparkLineSpec(
        1,
        [("def", "Thread", "an ally through the hesitation", 1)],
        "They lunge at the wrong shape while your friend slips through.",
    ),
    SparkLineSpec(
        2,
        [("off", "Feint", "one way", None), ("def", "Ghost", "a friend past them", None)],
        "The decoy takes the hit; the real one is already behind them.",
    ),
)


def sam_spark(style: SparkStyle | None = None, *extra: SparkLineSpec) -> str:
    lines = SAM_LINES if not extra else extra
    return spark_block(style or SPARK_V5, *lines)


def sam_spark_pay(icon: PayIcon) -> str:
    return sam_spark(SparkStyle(pay_icon=icon))


def sam_spark_canonical() -> str:
    return sam_spark(SPARK_V5)


def sam_spark_no_invites() -> str:
    return sam_spark(SparkStyle(show_invites=False))


def sam_spark_compact_xch() -> str:
    return sam_spark(SparkStyle(xch_layout="compact"))


def sam_spark_table_xch() -> str:
    return sam_spark(SparkStyle(xch_layout="table"))


def sam_spark_evocative() -> str:
    """Read-aloud chronology: player says the line, then describes beat by beat."""
    return spark_block(
        SPARK_V5,
        SparkLineSpec(
            1,
            [("def", "Slip", "your ally through the gap you opened", 1)],
            "You point; they move; the enemy still swats at your echo.",
        ),
        SparkLineSpec(
            2,
            [("off", "Sell", "the wrong threat", None), ("def", "Pass", "your partner through the opening", None)],
            "You throw your voice left — they commit — your friend is already past.",
            combo_join="and",
        ),
    )


def sam_spark_yield_first() -> str:
    return sam_spark(SparkStyle(phrase_first=True))


PAY_ICON_VARIANTS: list[dict] = [
    {
        "label": "Pay · Spark glyph (ships)",
        "note": "Amber spark token — currency earned from 6s, spent as bonus-roll choice.",
        "spark": lambda: sam_spark_pay("spark"),
    },
    {
        "label": "Pay · Bonus die +",
        "note": "Hollow die with + — you spend the bonus roll, not the natural 6.",
        "spark": lambda: sam_spark_pay("bonus"),
    },
    {
        "label": "Pay · Hollow roll",
        "note": "Dashed outline — unrolled bonus die you're committing.",
        "spark": lambda: sam_spark_pay("hollow"),
    },
    {
        "label": "Pay · Bolt slash",
        "note": "Lightning tick — quick spark-energy read at arm's length.",
        "spark": lambda: sam_spark_pay("bolt"),
    },
    {
        "label": "Pay · Amber bars",
        "note": "v3 cost pips recycled as spend column only.",
        "spark": lambda: sam_spark_pay("bar"),
    },
    {
        "label": "Pay · “6” die (retired)",
        "note": "Misleading — implies you spend the 6 itself. Do not ship.",
        "spark": lambda: sam_spark_pay("die-six"),
    },
]

LAYOUT_VARIANTS: list[dict] = [
    {
        "label": "Layout · No invites",
        "note": "Verb lines only.",
        "spark": sam_spark_no_invites,
    },
    {
        "label": "Layout · Compact exchange",
        "note": "Tighter pay⇄yield strip.",
        "spark": sam_spark_compact_xch,
    },
    {
        "label": "Layout · Spend/Yield table",
        "note": "Labeled mini-grid.",
        "spark": sam_spark_table_xch,
    },
    {
        "label": "Layout · Evocative chronology",
        "note": "Sell… and Pass… — read left-to-right at table.",
        "spark": sam_spark_evocative,
    },
    {
        "label": "Layout · Phrase-primary",
        "note": "Verb line first; exchange trails inline.",
        "spark": sam_spark_yield_first,
    },
]

SAM_VARIANTS: list[dict] = [
    {
        "slug": "canonical",
        "label": "A · v5 Canonical (ships)",
        "note": "Spark glyph pay ⇄ yield shapes · flowing combo · one invite.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_canonical,
    },
]


def build_sam_variant(spec: dict) -> str:
    return ability_card(
        "rogue",
        "Rogue",
        "Smoke and Mirrors",
        spec.get("flavor", "Let them argue about what they saw."),
        spec.get("effect", SAM_EFFECT),
        spec["spark"](),
    )


# ── Heritage reconstructions (proof timeline) ─────────────────────────────

C1 = '<span class="kw kw-crit">1</span>'


def _fl_icon(color: str) -> str:
    kind = {"red": "off", "blue": "def", "green": "res"}[color]
    return f'<span class="fl-icon fl-icon-{kind}" aria-hidden="true"></span>'


def _fl_chip(color: str, label: str) -> str:
    term, _, mag = label.rpartition(" ")
    if not mag.isdigit():
        term, mag = label, ""
    mag_html = f'<span class="fl-mag">{mag}</span>' if mag else ""
    return (
        f'<span class="fl-chip fl-chip-{color}">{_fl_icon(color)}'
        f'<span class="fl-term">{term}</span>{mag_html}</span>'
    )


def _heritage_glyph_cost(n: int) -> str:
    glyphs = "".join('<span class="spark-glyph" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-glyphs" title="{n} Spark">{glyphs}</span>'


def _heritage_bar_cost(n: int) -> str:
    pips = "".join('<span class="spark-pip-heritage" aria-hidden="true"></span>' for _ in range(n))
    return f'<span class="spark-pips-heritage" title="{n} Spark">{pips}</span>'


def heritage_crit_sam() -> str:
    crit = (
        '<div class="csec"><div class="clbl">Crit</div><div class="crow">'
        f'<div class="ci">{C1} Two enemies investigate, not one.</div></div></div>'
    )
    return ability_card(
        "rogue",
        "Rogue",
        "Smoke and Mirrors",
        "Let them argue about what they saw.",
        "Perform a <strong>Deception</strong> check. On success, create a false impression — "
        "a sound, a silhouette, a dropped object. Every enemy in the <strong>Scene</strong> is "
        "<strong>Rattled</strong>, wrong-footed by what they think they saw, until one spends an "
        "<strong>Action</strong> investigating.",
        crit,
    )


def heritage_chip_sam() -> str:
    def chip_line(cost: int, chips: list[tuple[str, str]], action: str, how: str) -> str:
        parts = []
        for i, (color, word) in enumerate(chips):
            if i:
                parts.append('<span class="fl-plus">+</span>')
            parts.append(_fl_chip(color, word))
        keys = f'<span class="spark-keys">{"".join(parts)}</span>'
        return (
            f'<div class="ci spark-line fl-{chips[0][0]}">'
            f"{_heritage_glyph_cost(cost)}{keys}"
            f'<span class="ci-txt">— {action} <span class="spark-how">— {how}</span></span></div>'
        )

    spark = (
        '<div class="csec spark-sec"><div class="clbl">Spark</div><div class="crow">'
        + chip_line(1, [("blue", "Boost 1")], "Slip an ally through the hesitation", "what did they think they saw?")
        + chip_line(
            2,
            [("red", "Stagger 1"), ("blue", "Boost 1")],
            "Feint one way; send a friend the other",
            "what do they lunge at — who slips past?",
        )
        + "</div></div>"
    )
    return ability_card(
        "rogue", "Rogue", "Smoke and Mirrors",
        "Let them argue about what they saw.", SAM_EFFECT, spark,
    )


def heritage_v2_question_sam() -> str:
    def v2_line(cost: int, cat: str, text: str, mag: int, prompt: str) -> str:
        mag_html = f'<span class="spark-n spark-n-{cat}">({mag})</span>'
        return (
            f'<div class="ci spark-entry-heritage">'
            f"{_heritage_glyph_cost(cost)}"
            '<div class="spark-body">'
            f'<div class="spark-verb">{text} {mag_html}.</div>'
            f'<div class="spark-prompt">{prompt}</div></div></div>'
        )

    spark = (
        '<div class="csec spark-sec"><div class="clbl">Spark</div><div class="crow">'
        + v2_line(1, "def", "Thread an ally through the hesitation", 1, "What did they think they saw?")
        + v2_line(
            2,
            "off",
            "Feint one way · Ghost a friend past them",
            2,
            "What do they lunge at — who slips past?",
        )
        + "</div></div>"
    )
    return ability_card(
        "rogue", "Rogue", "Smoke and Mirrors",
        "Let them argue about what they saw.", SAM_EFFECT, spark,
    )


def _heritage_v3_line(cost: int, clauses: list[Clause], invite: str, *, split_combo: bool) -> str:
    rows: list[str] = []
    multi = len(clauses) > 1
    for i, (cat, verb, tail, mag) in enumerate(clauses):
        if i > 0 and multi and split_combo:
            rows.append('<div class="spark-chain"><span class="spark-link">→</span></div>')
        icon = f'<span class="cat-icon cat-{cat}" aria-hidden="true"></span>'
        v = verb_span(cat, verb)
        clean = re.sub(r",?\s*then\s*$", "", tail, flags=re.I) if multi and i == 0 else tail
        if mag is not None:
            mag_html = (
                f'<span class="spark-mag spark-mag-{cat}">'
                f'<span class="cat-icon cat-{cat}" aria-hidden="true"></span>'
                f'<span class="mag-n">({mag})</span></span>'
            )
            rows.append(f'<div class="spark-row">{icon}{v} {clean} {mag_html}.</div>')
        else:
            end = "" if clean.rstrip().endswith(".") else "."
            rows.append(f'<div class="spark-row">{icon}{v} {clean}{end}</div>')
    rows.append(f'<div class="spark-invite-heritage"><span class="invite-lead">—</span> {invite}</div>')
    border = entry_border_class(clauses)
    return (
        f'<div class="ci spark-entry-heritage {border}">'
        f"{_heritage_bar_cost(cost)}"
        f'<div class="spark-body">{"".join(rows)}</div></div>'
    )


def heritage_v3_sam() -> str:
    spark = (
        '<div class="csec spark-sec"><div class="clbl">Spark</div><div class="crow">'
        + _heritage_v3_line(
            1, [("def", "Thread", "an ally through the hesitation", 1)],
            "They lunge at the wrong shape.", split_combo=False,
        )
        + _heritage_v3_line(
            2,
            [("off", "Feint", "one way, then", None), ("def", "Ghost", "a friend past them", None)],
            "The wrong person moves; the right one is already gone.", split_combo=True,
        )
        + "</div></div>"
    )
    return ability_card(
        "rogue", "Rogue", "Smoke and Mirrors",
        "Let them argue about what they saw.", SAM_EFFECT, spark,
    )


def heritage_v5_die_sam() -> str:
    return build_sam_variant({"spark": lambda: sam_spark(SparkStyle(pay_icon="die-six"))})


HERITAGE_VARIANTS: list[dict] = [
    {
        "label": "H0 · Crit (pre-Spark)",
        "note": "Crit-count flourish — keyword outcomes, no Spark section.",
        "build": heritage_crit_sam,
    },
    {
        "label": "H1 · Chip pills",
        "note": "Boost/Stagger keyword chips + question gloss.",
        "build": heritage_chip_sam,
    },
    {
        "label": "H2 · Glyph + (n) questions",
        "note": "Star cost glyphs, colored parentheses, italic questions.",
        "build": heritage_v2_question_sam,
    },
    {
        "label": "H3 · v3 arrows + bars",
        "note": "Amber bar cost, → split combos, em-dash invites, (n) magnitude.",
        "build": heritage_v3_sam,
    },
    {
        "label": "H4 · v5 misleading “6”",
        "note": "Exchange table but spend column shows 6 — retired.",
        "build": heritage_v5_die_sam,
    },
    {
        "label": "H5 · v5 Spark glyph (current)",
        "note": "Spend spark token ⇄ yield shapes · flowing sentence.",
        "build": lambda: build_sam_variant(SAM_VARIANTS[0]),
    },
]


def _variant_card(spec: dict, *, legacy: bool = False) -> str:
    if legacy:
        return spec["build"]()
    return build_sam_variant(spec)


# ── Production cards (8) ─────────────────────────────────────────────────

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
                SPARK_V5,
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
        "build": lambda: ability_card(
            "paladin",
            "Paladin",
            "Condemn",
            "You don't curse them. You recognize what they are.",
            "Perform a <strong>Faith</strong> check to speak what they have done aloud — "
            "the truth lands while everyone watches.",
            spark_block(
                SPARK_V5,
                SparkLineSpec(
                    1,
                    [("off", "Unmask", "them until the room goes quiet", 2)],
                    "Swagger drains away; everyone sees what remains.",
                ),
                SparkLineSpec(
                    2,
                    [("off", "Shake", "their certainty", None), ("res", "Plant", "your feet like stone", None)],
                    "They buckle in the telling; you do not move.",
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
                SPARK_V5,
                SparkLineSpec(
                    1,
                    [("off", "Cleave", "through what they're holding", 2)],
                    "Their guard, footing, or nerve is broken.",
                ),
                SparkLineSpec(
                    2,
                    [
                        ("off", "Rupture", "their defenses as you pass", None),
                        ("def", "Hurl", "an ally above them", None),
                    ],
                    "Steel opens the lane; your friend falls through it.",
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
                SPARK_V5,
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
                SPARK_V5,
                SparkLineSpec(
                    1,
                    [("off", "Pierce", "from the blind side", 1)],
                    "They never saw which shadow moved.",
                ),
                SparkLineSpec(
                    2,
                    [("off", "Drop", "them before they finish turning", 2)],
                    "The floor meets them mid-thought.",
                ),
            ),
        ),
    },
    {
        "id": 310,
        "key": "smoke-and-mirrors-rogue",
        "class": "Rogue",
        "name": "Smoke and Mirrors",
        "build": lambda: build_sam_variant(SAM_VARIANTS[0]),
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
                SPARK_V5,
                SparkLineSpec(
                    1,
                    [("off", "Brand", "them with a crawling sigil", 1)],
                    "Everyone sees where the next blow belongs.",
                ),
                SparkLineSpec(
                    2,
                    [("off", "Unravel", "their guard from throat to heel", 2)],
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
                SPARK_V5,
                SparkLineSpec(
                    1,
                    [("res", "Exhale", "the hunger for a breath", 1)],
                    "For a moment, you feel like a person again.",
                ),
                SparkLineSpec(
                    2,
                    [
                        ("res", "Ground", "yourself in the surge", None),
                        ("off", "Wither", "whoever stood too close", None),
                    ],
                    "You steady; the heat finds the nearest fool.",
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

    sam_chunks = []
    for var in PAY_ICON_VARIANTS:
        html = build_sam_variant({"spark": var["spark"]})
        sam_chunks.append(
            f'<div class="sample variant-sample"><div class="stag">{var["label"]}</div>'
            f'<div class="vnote">{var["note"]}</div>'
            f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
        )
    pay_section = (
        '<h2 id="pay-lab">Smoke and Mirrors — pay icon lab</h2>'
        '<p class="lab-intro">Same card, six spend-column icons. Natural <strong>6</strong>s earn Spark; '
        "you <em>spend Spark</em> to roll the bonus die or take the card option — the spend icon should "
        "not look like a 6.</p>"
        f'<div class="proof-grid variant-grid">{"".join(sam_chunks)}</div>'
    )

    layout_chunks = []
    for var in LAYOUT_VARIANTS:
        html = build_sam_variant({"spark": var["spark"]})
        layout_chunks.append(
            f'<div class="sample variant-sample"><div class="stag">{var["label"]}</div>'
            f'<div class="vnote">{var["note"]}</div>'
            f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
        )
    layout_section = (
        '<h2 id="layout-lab">Smoke and Mirrors — layout lab</h2>'
        f'<div class="proof-grid variant-grid">{"".join(layout_chunks)}</div>'
    )

    heritage_chunks = []
    for var in HERITAGE_VARIANTS:
        html = _variant_card(var, legacy=True)
        heritage_chunks.append(
            f'<div class="sample variant-sample"><div class="stag">{var["label"]}</div>'
            f'<div class="vnote">{var["note"]}</div>'
            f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
        )
    heritage_section = (
        '<h2 id="heritage">Smoke and Mirrors — heritage timeline</h2>'
        "<p class=\"lab-intro\">Oldest → newest on the same card. "
        "<strong>H5</strong> is what ships today.</p>"
        f'<div class="proof-grid variant-grid heritage-grid">{"".join(heritage_chunks)}</div>'
    )

    legend = """
<div class="legend">
  <span class="lg-item"><span class="pay-spark"></span> Spark token (spend)</span>
  <span class="lg-item"><span class="pay-bonus"><span class="pay-plus">+</span></span> bonus die</span>
  <span class="lg-item"><span class="xch-mid">⇄</span> exchange</span>
  <span class="lg-item"><span class="mag-pips mag-pips-off"><span class="pip-shape cat-off"></span><span class="pip-shape cat-off"></span></span> yield</span>
</div>
<div class="proc box">
  <strong>Spend icon ideation:</strong> A natural <strong>6</strong> earns Spark but stays in your pool.
  Spending Spark means <em>not</em> rolling the bonus die — so the left column should read as
  <strong>Spark currency</strong> or <strong>bonus-roll choice</strong>, not a die showing 6.
  Candidates: spark glyph · <strong>+</strong> die · hollow roll · bolt · amber bars.
</div>
<div class="proc box">
  <strong>v5 (ships):</strong> spark glyph ⇄ yield shape-pips · read verb line aloud ·
  combos one sentence (<em>Feint…, while you Ghost…</em>) · max <strong>2</strong> entries.
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
body.proof-spark .heritage-grid .stag{font-size:10px;}
/* Heritage-only styles (retired passes) */
.spark-glyphs{display:inline-flex;gap:1px;flex-shrink:0;padding-top:2px;}
.spark-glyph{
  display:inline-block;width:8px;height:10px;flex-shrink:0;
  background:linear-gradient(160deg,#ffe566 0%,#d4a017 55%,#9a7209 100%);
  clip-path:polygon(50% 0%,68% 36%,100% 38%,74% 60%,82% 100%,50% 78%,18% 100%,26% 60%,0% 38%,32% 36%);
}
.spark-pips-heritage{display:flex;flex-direction:column;gap:3px;flex-shrink:0;padding-top:2px;}
.spark-pip-heritage{
  display:block;width:4px;height:11px;border-radius:1px;
  background:linear-gradient(180deg,#e0a820,#8a6508);
}
.ci.spark-entry-heritage{display:flex;align-items:flex-start;gap:5px;padding:4px 5px;margin:0;
  border-radius:4px;border:1px solid rgba(90,74,50,.12);background:rgba(0,0,0,.02);}
.spark-verb{font-size:9.5px;line-height:1.38;font-weight:600;color:#1a1008;}
.spark-n{font-weight:800;font-size:9px;}
.spark-n-off{color:#991B1B;}
.spark-n-def{color:#2563EB;}
.spark-n-res{color:#166534;}
.spark-prompt{font-size:8px;line-height:1.38;font-style:italic;color:#5a4a32;margin-top:2px;}
.spark-entry-heritage .spark-row{font-size:9.5px;line-height:1.38;}
.spark-entry-heritage .spark-mag{font-size:9px;}
.spark-chain{padding-left:10px;line-height:1;margin:2px 0;}
.spark-link{color:#9a7209;font-size:9px;font-weight:800;}
.spark-invite-heritage{font-size:7.75px;font-style:italic;color:#5a4a32;margin-top:2px;padding-left:6px;}
.spark-invite-heritage .invite-lead{color:#a08a5c;font-style:normal;margin-right:2px;}
"""

    PROOF_OUT.write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        "<title>Spark v5 proof — pay icons + heritage</title><style>"
        f"{css}"
        f"{proof_css}"
        "</style></head><body class=\"proof-spark\">"
        "<h1>Spark v5 — pay icons + heritage timeline</h1>"
        '<p class="sub">Eight model cards use the <strong>spark glyph</strong> spend icon. '
        '<a href="#pay-lab" style="color:#e7d6ac">Pay icon lab</a> · '
        '<a href="#layout-lab" style="color:#e7d6ac">Layout lab</a> · '
        '<a href="#heritage" style="color:#e7d6ac">Heritage timeline</a> on Smoke and Mirrors.</p>'
        f"{legend}"
        + "".join(sections)
        + pay_section
        + layout_section
        + heritage_section
        + "</body></html>",
        encoding="utf-8",
    )
    n_lab = len(PAY_ICON_VARIANTS) + len(LAYOUT_VARIANTS) + len(HERITAGE_VARIANTS)
    print(f"Wrote {PROOF_OUT} ({len(CARDS)} cards + {n_lab} SAM lab/heritage)")


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
