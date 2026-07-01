#!/usr/bin/env python3
"""Spark / Flourish — 8 model cards + Rogue variant lab (Smoke and Mirrors).

Spark v5: exchange table (spend 6s ⇄ yield shapes), magnitude as shape pips,
flowing combo sentences (no arrows), max 2 entries, optional invites.

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


@dataclass
class SparkStyle:
    xch_layout: XchLayout = "row"
    show_invites: bool = True
    phrase_first: bool = False


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


def pay_dice(cost: int) -> str:
    dice = "".join('<span class="spark-die" aria-hidden="true">6</span>' for _ in range(cost))
    return f'<span class="xch-pay" title="{cost} Spark">{dice}</span>'


def exchange_row(cost: int, clauses: list[Clause], layout: XchLayout) -> str:
    pay = pay_dice(cost)
    yld = f'<span class="xch-yield">{yield_icons(clauses)}</span>'
    mid = '<span class="xch-mid" aria-hidden="true">⇄</span>'
    if layout == "compact":
        return f'<div class="spark-xch spark-xch-compact">{pay}{mid}{yld}</div>'
    if layout == "table":
        return (
            '<div class="spark-xch spark-xch-table">'
            f'<div class="xch-th">Spend</div><div class="xch-th">Yield</div>'
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
    xch = exchange_row(spec.cost, spec.clauses, style.xch_layout)
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


def sam_spark_canonical() -> str:
    return spark_block(
        SPARK_V5,
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


def sam_spark_no_invites() -> str:
    return spark_block(
        SparkStyle(show_invites=False),
        SparkLineSpec(
            1,
            [("def", "Thread", "an ally through the hesitation", 1)],
        ),
        SparkLineSpec(
            2,
            [("off", "Feint", "one way", None), ("def", "Ghost", "a friend past them", None)],
        ),
    )


def sam_spark_compact_xch() -> str:
    return spark_block(
        SparkStyle(xch_layout="compact"),
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


def sam_spark_table_xch() -> str:
    return spark_block(
        SparkStyle(xch_layout="table"),
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
    return spark_block(
        SparkStyle(phrase_first=True),
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


SAM_VARIANTS: list[dict] = [
    {
        "slug": "canonical",
        "label": "A · v5 Canonical (ships)",
        "note": "Exchange row: spend 6s ⇄ yield shapes · flowing combo · one invite.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_canonical,
    },
    {
        "slug": "no-invites",
        "label": "B · No invites",
        "note": "Action lines only — no italic stems.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_no_invites,
    },
    {
        "slug": "compact-xch",
        "label": "C · Compact exchange",
        "note": "Tighter pay⇄yield strip above the phrase.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_compact_xch,
    },
    {
        "slug": "table-xch",
        "label": "D · Spend / Yield table",
        "note": "Mini grid labels the exchange explicitly.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_table_xch,
    },
    {
        "slug": "evocative",
        "label": "E · Evocative chronology",
        "note": "Verbs you say aloud, then play out left-to-right (Sell… and Pass…).",
        "flavor": "The lie lands first. The truth walks through second.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_evocative,
    },
    {
        "slug": "yield-first",
        "label": "F · Phrase-primary",
        "note": "Same as A — exchange stays compact; phrase is the hero line.",
        "flavor": "Let them argue about what they saw.",
        "effect": SAM_EFFECT,
        "spark": sam_spark_yield_first,
    },
]


def build_sam_variant(spec: dict) -> str:
    return ability_card(
        "rogue",
        "Rogue",
        "Smoke and Mirrors",
        spec["flavor"],
        spec["effect"],
        spec["spark"](),
    )


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
    for var in SAM_VARIANTS:
        html = build_sam_variant(var)
        sam_chunks.append(
            f'<div class="sample variant-sample">'
            f'<div class="stag">{var["label"]}</div>'
            f'<div class="vnote">{var["note"]}</div>'
            f'<div class="primer-cards"><div class="cardwrap">{html}</div></div></div>'
        )
    sam_section = (
        '<h2 id="rogue-lab">Smoke and Mirrors — Rogue lab</h2>'
        '<p class="lab-intro">Six variants on one Rogue card. <strong>A</strong> ships to card-data / '
        "Baserow. Rejected v4 experiments (arrows, split invites, dot pips, 3+ entries) removed.</p>"
        f'<div class="proof-grid variant-grid">{"".join(sam_chunks)}</div>'
    )

    legend = """
<div class="legend">
  <span class="lg-item"><span class="spark-die">6</span> Spark spent (natural 6)</span>
  <span class="lg-item"><span class="xch-mid">⇄</span> exchange</span>
  <span class="lg-item"><span class="mag-pips mag-pips-off"><span class="pip-shape cat-off"></span><span class="pip-shape cat-off"></span></span> yield (▲▲ = mag 2)</span>
  <span class="lg-item"><strong class="spark-v-def">Verb</strong> read aloud, then describe</span>
</div>
<div class="proc box">
  <strong>v5:</strong> spend <strong>6</strong>s ⇄ yield shape-pips · magnitude = repeated ▲/■/● (not numbers) ·
  combos are one sentence (<em>Feint…, while you Ghost…</em>) · max <strong>2</strong> Spark entries ·
  invites optional (lab variant B drops them).
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
        "<title>Spark v5 proof — 8 cards + Rogue lab</title><style>"
        f"{css}"
        f"{proof_css}"
        "</style></head><body class=\"proof-spark\">"
        "<h1>Spark v5 — exchange table + Rogue lab</h1>"
        '<p class="sub">Spend natural <strong>6</strong>s on the left, yield shape-pips on the right, '
        'then read the <strong>verb line</strong> aloud. See '
        '<a href="#rogue-lab" style="color:#e7d6ac">Smoke and Mirrors lab</a>.</p>'
        f"{legend}"
        + "".join(sections)
        + sam_section
        + "</body></html>",
        encoding="utf-8",
    )
    print(f"Wrote {PROOF_OUT} ({len(CARDS)} cards + {len(SAM_VARIANTS)} SAM variants)")


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
