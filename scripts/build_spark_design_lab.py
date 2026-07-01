#!/usr/bin/env python3
"""Export Spark design-lab variants for Card Studio playtest voting.

Writes spark-design-lab-data.js — run via build_spark_flourish_proof.py --write
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "spark-design-lab-data.js"

# Import builders after path setup (called from build_spark_flourish_proof)
def collect_variants() -> list[dict]:
    from scripts.build_spark_flourish_proof import (  # noqa: WPS433
        HERITAGE_VARIANTS,
        LAYOUT_VARIANTS,
        PAY_ICON_VARIANTS,
        SAM_EFFECT,
        SAM_VARIANTS,
        SparkStyle,
        _variant_card,
        build_sam_variant,
        heritage_chip_sam,
        heritage_crit_sam,
        heritage_v2_question_sam,
        heritage_v3_sam,
        heritage_v5_die_sam,
        sam_spark,
        sam_spark_canonical,
        sam_spark_compact_xch,
        sam_spark_evocative,
        sam_spark_no_invites,
        sam_spark_pay,
        sam_spark_table_xch,
        sam_spark_yield_first,
    )

    def wrap(html: str) -> str:
        return f'<div class="spark-lab-cardwrap primer-cards">{html}</div>'

    def card_html(build_fn) -> str:
        return wrap(build_fn())

    entries: list[dict] = []

    def add(
        vid: str,
        category: str,
        cat_label: str,
        label: str,
        *,
        ships: bool = False,
        goals: list[dict],
        playtest: str,
        html: str,
        sort: int,
    ) -> None:
        entries.append(
            {
                "id": vid,
                "category": category,
                "categoryLabel": cat_label,
                "label": label,
                "ships": ships,
                "goals": goals,
                "playtestQuestion": playtest,
                "html": html,
                "sort": sort,
            }
        )

    pay_meta = [
        (
            "pay-spark-glyph",
            "Spark glyph",
            True,
            [
                {
                    "title": "Spark = currency",
                    "body": "Spend icon reads as Spark earned from 6s — not the die face itself.",
                },
                {
                    "title": "Name matches section",
                    "body": "Glyph ties to the Spark label on the card.",
                },
                {
                    "title": "Quick scan",
                    "body": "Count glyphs = how many Sparks this option costs.",
                },
            ],
            "Does the left side feel like spending Spark, or rolling a die?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("spark")})),
        ),
        (
            "pay-bonus-die",
            "Bonus die +",
            False,
            [
                {
                    "title": "Roll vs option",
                    "body": "Shows you're giving up the bonus die roll for this card effect.",
                },
                {
                    "title": "Mechanic clarity",
                    "body": "+ die = the extra roll you'd otherwise take.",
                },
            ],
            "Does + on a die make the spend-versus-roll tradeoff obvious?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bonus")})),
        ),
        (
            "pay-hollow-roll",
            "Hollow roll",
            False,
            [
                {
                    "title": "Uncommitted roll",
                    "body": "Dashed die = bonus roll you're cashing in without taking.",
                },
                {
                    "title": "Softer than +",
                    "body": "Less mechanical, more 'I'm spending a roll chance'.",
                },
            ],
            "Does the dashed die read as 'bonus roll' without feeling like a natural 6?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("hollow")})),
        ),
        (
            "pay-bolt",
            "Bolt slash",
            False,
            [
                {
                    "title": "Energy at a glance",
                    "body": "Lightning = spark energy, fast to spot.",
                },
                {
                    "title": "Less literal",
                    "body": "Doesn't say die or currency — pure flair.",
                },
            ],
            "Can you tell how much Spark this costs from the bolt icons alone?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bolt")})),
        ),
        (
            "pay-amber-bars",
            "Amber bars",
            False,
            [
                {
                    "title": "Familiar cost pips",
                    "body": "Recycles v3 vertical bars — count bars = cost.",
                },
                {
                    "title": "Separate from yield",
                    "body": "Bars only on spend side; triangles/squares stay on yield.",
                },
            ],
            "Do amber bars read as cost without confusing yield shapes?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bar")})),
        ),
        (
            "pay-die-six",
            "“6” die (retired)",
            False,
            [
                {
                    "title": "Anti-pattern",
                    "body": "Shows 6 on spend — implies you lose the natural 6 (wrong).",
                },
                {
                    "title": "Playtest control",
                    "body": "Rate low if this confuses you at the table.",
                },
            ],
            "Does showing 6 make you think you're spending the die that rolled 6?",
            lambda: card_html(
                lambda: build_sam_variant({"spark": lambda: sam_spark_pay("die-six")})
            ),
        ),
    ]
    for i, (vid, label, ships, goals, playtest, build) in enumerate(pay_meta):
        add(vid, "pay", "Spend icon", label, ships=ships, goals=goals, playtest=playtest, html=build(), sort=100 + i)

    layout_meta = [
        (
            "layout-canonical",
            "v5 Canonical layout",
            True,
            [
                {"title": "Exchange row", "body": "Spend ⇄ yield shapes above the verb line."},
                {"title": "One invite", "body": "Single italic line nudges the story after you read verbs."},
                {"title": "Flowing combo", "body": "Two-spark = one sentence: Feint…, while you Ghost…"},
            ],
            "Read both Spark lines aloud — can you play them chronologically?",
            lambda: card_html(sam_spark_canonical),
        ),
        (
            "layout-no-invites",
            "No invites",
            False,
            [
                {"title": "Verb only", "body": "No italic stems — action lines carry everything."},
                {"title": "Less clutter", "body": "More room on dense cards."},
            ],
            "Do you miss the italic line, or is the verb enough?",
            lambda: card_html(sam_spark_no_invites),
        ),
        (
            "layout-compact-xch",
            "Compact exchange",
            False,
            [
                {"title": "Tighter strip", "body": "Smaller pay⇄yield bar — phrase gets more space."},
            ],
            "Is the exchange still readable when compact?",
            lambda: card_html(sam_spark_compact_xch),
        ),
        (
            "layout-table-xch",
            "Spend / Yield table",
            False,
            [
                {"title": "Explicit labels", "body": "Mini grid names Spend and Yield columns."},
                {"title": "Teach once", "body": "Helps first-time players learn the exchange."},
            ],
            "Do labels help or feel like homework?",
            lambda: card_html(sam_spark_table_xch),
        ),
        (
            "layout-evocative",
            "Evocative chronology",
            False,
            [
                {
                    "title": "Read left-to-right",
                    "body": "Sell the wrong threat, and Pass your partner — say it, then describe.",
                },
                {"title": "Improv fuel", "body": "Verbs invite confident table narration."},
            ],
            "Can you say line 2 out loud and describe both beats in order?",
            lambda: card_html(
                lambda: build_sam_variant(
                    {
                        "flavor": "The lie lands first. The truth walks through second.",
                        "effect": SAM_EFFECT,
                        "spark": sam_spark_evocative,
                    }
                )
            ),
        ),
        (
            "layout-phrase-first",
            "Phrase-primary",
            False,
            [
                {"title": "Verb hero", "body": "Action line first; exchange chip trails inline."},
                {"title": "Fiction forward", "body": "Mechanics don't lead the read."},
            ],
            "Does putting verbs first speed up your pick at the table?",
            lambda: card_html(sam_spark_yield_first),
        ),
    ]
    for i, (vid, label, ships, goals, playtest, build) in enumerate(layout_meta):
        add(vid, "layout", "Layout & copy", label, ships=ships, goals=goals, playtest=playtest, html=build(), sort=200 + i)

    heritage_meta = [
        (
            "heritage-crit",
            "H0 · Crit (pre-Spark)",
            [
                {"title": "Legacy flourish", "body": "Crit-count options — no Spark section at all."},
                {"title": "Baseline", "body": "Compare: is Spark clearer than Crit for this card?"},
            ],
            "Is anything lost moving from Crit to Spark on this ability?",
            lambda: card_html(heritage_crit_sam),
        ),
        (
            "heritage-chips",
            "H1 · Chip pills",
            [
                {"title": "Keyword pills", "body": "Boost 1 / Stagger 1 chips — mechanical voice."},
                {"title": "Questions", "body": "Italic questions prompt improv ('what did they see?')."},
            ],
            "Do chips feel too rules-heavy compared to verbs?",
            lambda: card_html(heritage_chip_sam),
        ),
        (
            "heritage-glyph-questions",
            "H2 · Glyph + (n) questions",
            [
                {"title": "Star cost", "body": "Spark glyph cost with colored (1) magnitude."},
                {"title": "Question gloss", "body": "Full-sentence questions under each option."},
            ],
            "Are questions better or worse than story invites?",
            lambda: card_html(heritage_v2_question_sam),
        ),
        (
            "heritage-v3-arrows",
            "H3 · Arrows + bars",
            [
                {"title": "Split combos", "body": "→ between Feint and Ghost on separate lines."},
                {"title": "Bar cost", "body": "Amber bars left; (n) numbers for magnitude."},
            ],
            "Do arrows help combos or break the sentence flow?",
            lambda: card_html(heritage_v3_sam),
        ),
        (
            "heritage-v5-die-six",
            "H4 · Exchange with “6”",
            [
                {"title": "Misleading spend", "body": "v5 layout but 6 on spend column — retired."},
            ],
            "Compare to spark glyph — which spend icon is clearer?",
            lambda: card_html(
                lambda: build_sam_variant({"spark": lambda: sam_spark_pay("die-six")})
            ),
        ),
        (
            "heritage-v5-current",
            "H5 · v5 Spark glyph",
            True,
            [
                {"title": "Current ship", "body": "Spark token ⇄ shape yield · flowing sentence."},
            ],
            "Overall — would you ship this over heritage options?",
            lambda: card_html(lambda: build_sam_variant(SAM_VARIANTS[0])),
        ),
    ]
    for i, item in enumerate(heritage_meta):
        if len(item) == 6:
            vid, label, ships, goals, playtest, build = item
        else:
            vid, label, goals, playtest, build = item
            ships = False
        add(
            vid,
            "heritage",
            "Heritage timeline",
            label,
            ships=ships,
            goals=goals,
            playtest=playtest,
            html=build(),
            sort=300 + i,
        )

    entries.sort(key=lambda e: e["sort"])
    return entries


def write_lab_data() -> None:
    variants = collect_variants()
    payload = {
        "cardName": "Smoke and Mirrors",
        "cardClass": "Rogue",
        "updated": "2026-07-03",
        "intro": (
            "Same Rogue card, different Spark presentations. "
            "Tap ♥ I like something here or leave a comment on what works for you."
        ),
        "variants": variants,
    }
    OUT.write_text(
        "// Generated by scripts/build_spark_design_lab.py — do not edit.\n"
        f"window.SPARK_DESIGN_LAB = {json.dumps(payload, ensure_ascii=False, indent=2)};\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(variants)} variants)")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT))
    write_lab_data()
