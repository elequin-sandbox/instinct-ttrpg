#!/usr/bin/env python3
"""Export Spark design-lab variants for Card Studio playtest voting.

Writes spark-design-lab-data.js — run via build_spark_flourish_proof.py --write
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "spark-design-lab-data.js"


def collect_variants() -> list[dict]:
    from scripts.build_spark_flourish_proof import (  # noqa: WPS433
        SAM_EFFECT,
        build_sam_variant,
        heritage_chip_sam,
        heritage_v2_question_sam,
        sam_spark_canonical,
        sam_spark_column_flow_card,
        sam_spark_compact_xch,
        sam_spark_evocative,
        sam_spark_inverted_card,
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

    # ── Layout — structure only (how rows stack / exchange reads) ───────────
    layout_meta = [
        (
            "layout-exchange",
            "Exchange row (v5)",
            False,
            [
                {"title": "Spend ⇄ yield", "body": "Amber exchange strip above the verb line."},
                {"title": "Ships today", "body": "Current production layout on Spark cards."},
            ],
            "Can you read cost, category, and verb in one glance?",
            lambda: card_html(sam_spark_canonical),
        ),
        (
            "layout-inverted",
            "Verb-first + invite box",
            True,
            [
                {
                    "title": "Cost → shapes → verb",
                    "body": "Open row: die cost, yield shapes, bold Obscure / Pass + Distract.",
                },
                {
                    "title": "Serif invite below",
                    "body": "Bordered box holds the table description — fiction under the pick.",
                },
            ],
            "Does putting verbs first speed your pick? Is the invite box clearer than italic under?",
            lambda: card_html(sam_spark_inverted_card),
        ),
        (
            "layout-column-flow",
            "Column flow (book read)",
            False,
            [
                {
                    "title": "Key column left",
                    "body": "Cost die, shape, and impact verb stack in a narrow left column.",
                },
                {
                    "title": "Sentence continues right",
                    "body": "Same-size prose flows right — Deflect attention… / Sell the wrong threat.",
                },
                {
                    "title": "Combo = two rows",
                    "body": "Second row: Pass (red) + your ally through the opening — read top to bottom.",
                },
            ],
            "Read down the left column for the trade, then left-to-right across each row — does it feel like a book?",
            lambda: card_html(sam_spark_column_flow_card),
        ),
        (
            "layout-compact",
            "Compact exchange",
            False,
            [
                {"title": "Tighter strip", "body": "Smaller pay⇄yield bar — more room for copy."},
            ],
            "Is the exchange still readable when compact?",
            lambda: card_html(sam_spark_compact_xch),
        ),
        (
            "layout-table",
            "Spend / Yield labels",
            False,
            [
                {"title": "Mini grid", "body": "Explicit Spend and Yield column headers."},
            ],
            "Do labels help first-timers or feel like homework?",
            lambda: card_html(sam_spark_table_xch),
        ),
        (
            "layout-phrase-first",
            "Phrase before exchange",
            False,
            [
                {"title": "Verb hero", "body": "Action line leads; exchange chip trails inline."},
            ],
            "Does trailing the exchange after the verb change how you read the line?",
            lambda: card_html(sam_spark_yield_first),
        ),
    ]
    for i, (vid, label, ships, goals, playtest, build) in enumerate(layout_meta):
        add(
            vid, "layout", "Layout", label,
            ships=ships, goals=goals, playtest=playtest, html=build(), sort=100 + i,
        )

    # ── Language — copy voice (same v5 structure unless noted) ─────────────
    language_meta = [
        (
            "lang-invites",
            "Verbs + story invites",
            True,
            [
                {"title": "Bold verbs", "body": "Thread / Feint / Ghost — category-colored."},
                {"title": "Italic invite", "body": "One line nudges how you describe it at the table."},
            ],
            "Read both lines aloud — can you play them chronologically?",
            lambda: card_html(sam_spark_canonical),
        ),
        (
            "lang-no-invites",
            "Verbs only",
            False,
            [
                {"title": "Less clutter", "body": "No italic stems — action lines carry everything."},
            ],
            "Do you miss the invite line, or is the verb enough?",
            lambda: card_html(sam_spark_no_invites),
        ),
        (
            "lang-evocative",
            "Evocative chronology",
            False,
            [
                {
                    "title": "Read left-to-right",
                    "body": "Sell the wrong threat, and Pass your partner — say it, then describe.",
                },
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
            "lang-questions",
            "Question prompts",
            False,
            [
                {"title": "Improv fuel", "body": "Full-sentence questions instead of story invites."},
                {"title": "Heritage H2", "body": "“What did they think they saw?” under each option."},
            ],
            "Are questions better or worse than story invites?",
            lambda: card_html(heritage_v2_question_sam),
        ),
        (
            "lang-chips",
            "Keyword chips",
            False,
            [
                {"title": "Mechanical voice", "body": "Boost / Stagger pills — rules-forward read."},
                {"title": "Heritage H1", "body": "Compare to verb-first Spark copy."},
            ],
            "Do chips feel too rules-heavy compared to verbs?",
            lambda: card_html(heritage_chip_sam),
        ),
    ]
    for i, (vid, label, ships, goals, playtest, build) in enumerate(language_meta):
        add(
            vid, "language", "Language", label,
            ships=ships, goals=goals, playtest=playtest, html=build(), sort=200 + i,
        )

    # ── Spend icon — what the cost column looks like ───────────────────────
    pay_meta = [
        (
            "pay-spark-glyph",
            "Spark glyph",
            True,
            [
                {"title": "Spark = currency", "body": "Earned from 6s — not the die face itself."},
                {"title": "Quick scan", "body": "Count glyphs = Sparks spent."},
            ],
            "Does the left side feel like spending Spark, or rolling a die?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("spark")})),
        ),
        (
            "pay-bonus-die",
            "Bonus die +",
            False,
            [
                {"title": "Roll vs option", "body": "Giving up the bonus die roll for this effect."},
            ],
            "Does + on a die make the spend-versus-roll tradeoff obvious?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bonus")})),
        ),
        (
            "pay-hollow-roll",
            "Hollow roll",
            False,
            [
                {"title": "Uncommitted roll", "body": "Dashed outline — bonus roll you're cashing in."},
            ],
            "Does the dashed die read as bonus roll without feeling like a natural 6?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("hollow")})),
        ),
        (
            "pay-bolt",
            "Bolt slash",
            False,
            [
                {"title": "Energy at a glance", "body": "Lightning tick — spark energy, not a die."},
            ],
            "Can you tell cost from the bolt icons alone?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bolt")})),
        ),
        (
            "pay-amber-bars",
            "Amber bars",
            False,
            [
                {"title": "Cost pips", "body": "Vertical bars — count bars = cost."},
            ],
            "Do amber bars read as cost without confusing yield shapes?",
            lambda: card_html(lambda: build_sam_variant({"spark": lambda: sam_spark_pay("bar")})),
        ),
        (
            "pay-die-six",
            "“6” die (retired)",
            False,
            [
                {"title": "Anti-pattern", "body": "Implies you lose the natural 6 — wrong."},
            ],
            "Does showing 6 make you think you're spending the die that rolled 6?",
            lambda: card_html(
                lambda: build_sam_variant({"spark": lambda: sam_spark_pay("die-six")})
            ),
        ),
        (
            "pay-cost-die-blue",
            "Blue “6” cost die",
            False,
            [
                {
                    "title": "Inverted layout",
                    "body": "Periwinkle 6 before shapes — cost reads first on the verb row.",
                },
                {
                    "title": "Not the natural 6",
                    "body": "Still a spend marker; pairs with verb-first + invite box layout.",
                },
            ],
            "Does a blue 6 before Defend read as cost without implying you lose the crit die?",
            lambda: card_html(sam_spark_inverted_card),
        ),
    ]
    for i, (vid, label, ships, goals, playtest, build) in enumerate(pay_meta):
        add(
            vid, "pay", "Spend icon", label,
            ships=ships, goals=goals, playtest=playtest, html=build(), sort=300 + i,
        )

    entries.sort(key=lambda e: e["sort"])
    return entries


def write_lab_data() -> None:
    variants = collect_variants()
    payload = {
        "cardName": "Smoke and Mirrors",
        "cardClass": "Rogue",
        "updated": "2026-07-01",
        "intro": (
            "Same Rogue card — compare Layout, Language, and Spend icon in separate tabs. "
            "Hover to peek closer, or click a card to open full size. "
            "Tap ♥ or leave a comment on what works for you."
        ),
        "categories": {
            "layout": {
                "label": "Layout",
                "intro": (
                    "How the Spark block is structured: exchange row vs verb-first, compact vs "
                    "labeled grid. Copy stays similar so you can judge structure alone."
                ),
            },
            "language": {
                "label": "Language",
                "intro": (
                    "How the lines read at the table: bold verbs, invites, questions, or keyword "
                    "chips. Structure is mostly v5 exchange unless noted."
                ),
            },
            "pay": {
                "label": "Spend icon",
                "intro": (
                    "What marks cost on the left: Spark glyph, bonus-roll icons, amber bars, or "
                    "the retired misleading “6”. Natural 6s earn Spark — you spend Spark, not the die."
                ),
            },
        },
        "defaultCategory": "layout",
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
