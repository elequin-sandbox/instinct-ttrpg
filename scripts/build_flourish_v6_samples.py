#!/usr/bin/env python3
"""Flourish v6 sample pass — RIGHT-card layout (flavor · Effect · Spark + narrative).

Four yield categories: Advance (red) · Defend (blue) · Boost (teal) · Restore (green).
Attempt-only Effect body; Spark lines pair mechanical keywords with evocative table beats.

Proof: flourish-v6-sample-proof.html (12 cards: 4 Rogue, 4 Fighter, 4 Bard)

Usage:
  python3 scripts/build_flourish_v6_samples.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_spark_flourish_proof import cost_die_icons  # noqa: E402

PROOF_OUT = ROOT / "flourish-v6-sample-proof.html"
DATE = "2026-07-01"

Cat = Literal["off", "def", "boost", "res"]
SparkLine = tuple[int, list[tuple[Cat, str]], str]


def cat_shape(cat: Cat) -> str:
    if cat == "def":
        return '<span class="yield-sq cat-def" aria-hidden="true"></span>'
    if cat == "off":
        return '<span class="yield-tri cat-off" aria-hidden="true"></span>'
    if cat == "boost":
        return '<span class="yield-sq cat-boost" aria-hidden="true"></span>'
    return '<span class="yield-dot cat-res" aria-hidden="true"></span>'


def kw_label(cat: Cat, word: str) -> str:
    return f'<span class="spark-kw spark-kw-{cat}">{word}</span>'


def spark_verb_row(clauses: list[tuple[Cat, str]]) -> str:
    parts: list[str] = []
    for i, (cat, kw) in enumerate(clauses):
        if i:
            parts.append('<span class="spark-combo-plus" aria-hidden="true">+</span>')
        parts.append(cat_shape(cat))
        parts.append(kw_label(cat, kw))
    return "".join(parts)


def spark_entry(cost: int, clauses: list[tuple[Cat, str]], invite: str) -> str:
    return (
        '<div class="ci spark-entry spark-entry-inverted">'
        f'<div class="spark-verb-row">{cost_die_icons(cost)}{spark_verb_row(clauses)}</div>'
        f'<div class="spark-invite-box">{invite}</div>'
        "</div>"
    )


def spark_block(*lines: SparkLine) -> str:
    rendered = "".join(spark_entry(cost, clauses, invite) for cost, clauses, invite in lines)
    return (
        '<div class="csec spark-sec"><div class="clbl">Spark</div>'
        f'<div class="crow">{rendered}</div></div>'
    )


def right_card(
    accent: str,
    idtag: str,
    name: str,
    flavor: str,
    attempt: str,
    sparks: list[SparkLine],
    *,
    act: bool = True,
) -> str:
    badge = '<span class="cap cap-neutral">Act</span>' if act else '<span class="cap cap-neutral">React</span>'
    return (
        f'<div class="card acc-{accent}"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{badge}</div>'
        f'<div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div>'
        f'<div class="elbl">Effect</div><div class="etxt">{attempt}</div>'
        f"{spark_block(*sparks)}</div>"
        f'<div class="idtag">{idtag}</div><div class="tier-float"><span>t1</span></div></div>'
    )


# ── 12 sample cards — thoughtful Spark beats (July 2026) ────────────────────

SAMPLE_CARDS: list[dict] = [
    # Rogue
    {
        "class": "Rogue",
        "name": "Smoke and Mirrors",
        "build": lambda: right_card(
            "rogue",
            "Rogue",
            "Smoke and Mirrors",
            "Let them argue about what they saw.",
            "Perform a <strong>Deception</strong> check to plant a false impression — "
            "a sound, silhouette, or dropped object.",
            [
                (1, [("def", "Defend")], "Pull every eye toward the wrong shape."),
                (
                    2,
                    [("def", "Defend"), ("off", "Advance")],
                    "Sell the wrong threat — your ally is already through the opening.",
                ),
            ],
        ),
    },
    {
        "class": "Rogue",
        "name": "Sneak Attack",
        "build": lambda: right_card(
            "rogue",
            "Rogue",
            "Sneak Attack",
            "You weren't watching the right shadow.",
            "Perform a <strong>Stealth</strong> check to <strong>Strike</strong> from somewhere "
            "they aren't looking.",
            [
                (1, [("off", "Advance")], "Land the blow they never saw coming."),
                (2, [("off", "Advance")], "Drop them before they finish turning around."),
            ],
        ),
    },
    {
        "class": "Rogue",
        "name": "Quick Hands",
        "build": lambda: right_card(
            "rogue",
            "Rogue",
            "Quick Hands",
            "Their pocket was never the interesting part.",
            "Perform a <strong>Sleight of Hand</strong> check to lift, switch, or plant something "
            "on someone who isn't watching closely.",
            [
                (1, [("off", "Advance")], "The thing you needed changes hands — they never felt it."),
                (
                    2,
                    [("off", "Advance"), ("def", "Defend")],
                    "Plant the decoy; when they react, you're already gone.",
                ),
            ],
        ),
    },
    {
        "class": "Rogue",
        "name": "Misdirection",
        "build": lambda: right_card(
            "rogue",
            "Rogue",
            "Misdirection",
            "That's not what they think they saw.",
            "When an ally would be targeted, perform a <strong>Deception</strong> check to redirect "
            "attention elsewhere.",
            [
                (1, [("def", "Defend")], "Their attack bends toward the wrong person."),
                (
                    2,
                    [("def", "Defend"), ("off", "Advance")],
                    "They commit to the decoy — your ally is already moving.",
                ),
            ],
            act=False,
        ),
    },
    # Fighter
    {
        "class": "Fighter",
        "name": "Rallying Cry",
        "build": lambda: right_card(
            "fighter",
            "Fighter",
            "Rallying Cry",
            "One voice cuts through everything else.",
            "Perform a <strong>Presence</strong> check to shout what needs doing — cut through the noise.",
            [
                (1, [("def", "Defend")], "Your words find them — they hold where they were breaking."),
                (2, [("boost", "Boost")], "Name the opening — the next ally to act hits where you pointed."),
            ],
        ),
    },
    {
        "class": "Fighter",
        "name": "Disarm",
        "build": lambda: right_card(
            "fighter",
            "Fighter",
            "Disarm",
            "A fighter without a weapon is just a person in a bad situation.",
            "Perform an <strong>Athletics</strong> check to knock a weapon, shield, or tool from their grip.",
            [
                (1, [("off", "Advance")], "Their guard opens exactly where you wanted it."),
                (2, [("off", "Advance")], "They're fighting you with empty hands."),
            ],
        ),
    },
    {
        "class": "Fighter",
        "name": "Covering Fire",
        "build": lambda: right_card(
            "fighter",
            "Fighter",
            "Covering Fire",
            "You don't need to hit. You need them to duck.",
            "Perform a <strong>Tactics</strong> check to <strong>Strike</strong> at enemies who might "
            "intercept your allies this beat.",
            [
                (1, [("def", "Defend")], "They duck your fire and can't watch everywhere at once."),
                (2, [("boost", "Boost")], "Your suppression hides your ally's next move completely."),
            ],
        ),
    },
    {
        "class": "Fighter",
        "name": "Interpose",
        "build": lambda: right_card(
            "fighter",
            "Fighter",
            "Interpose",
            "You put yourself between them.",
            "When an ally within reach would take a hit, perform an <strong>Athletics</strong> check to "
            "<strong>Move</strong> into the blow's path.",
            [
                (1, [("def", "Defend")], "The blow finds you instead."),
                (2, [("res", "Restore")], "You take it — they shake it off and stay in the fight."),
            ],
            act=False,
        ),
    },
    # Bard
    {
        "class": "Bard",
        "name": "Battle Hymn",
        "build": lambda: right_card(
            "bard",
            "Bard",
            "Battle Hymn",
            "Fear can't compete with what you're singing.",
            "Perform a <strong>Performance</strong> check to keep allies steady under fire — volume, "
            "rhythm, something they can follow.",
            [
                (1, [("def", "Defend")], "They find the beat and don't break."),
                (
                    2,
                    [("def", "Defend"), ("res", "Restore")],
                    "The song reaches them — fear loosens its grip.",
                ),
            ],
        ),
    },
    {
        "class": "Bard",
        "name": "Cutting Words",
        "build": lambda: right_card(
            "bard",
            "Bard",
            "Cutting Words",
            "The right sentence at the wrong time.",
            "Perform a <strong>Deception</strong> check to land a verbal jab that throws off their next move.",
            [
                (1, [("off", "Advance")], "They stumble over your words instead of their footing."),
                (2, [("off", "Advance")], "The room hears how wrong they are."),
            ],
        ),
    },
    {
        "class": "Bard",
        "name": "Steady the Heart",
        "build": lambda: right_card(
            "bard",
            "Bard",
            "Steady the Heart",
            "Not this one. Not today.",
            "Perform a <strong>Medicine</strong> check to talk an ally through fear, pain, or doubt "
            "in the moment.",
            [
                (1, [("res", "Restore")], "They remember why they're still here."),
                (
                    2,
                    [("res", "Restore"), ("boost", "Boost")],
                    "Your steadiness becomes theirs — they act with purpose.",
                ),
            ],
        ),
    },
    {
        "class": "Bard",
        "name": "Vicious Mockery",
        "build": lambda: right_card(
            "bard",
            "Bard",
            "Vicious Mockery",
            "You're not talking to them. You're talking about them.",
            "Perform a <strong>Deception</strong> check to mock them until everyone in earshot is "
            "watching the wrong thing.",
            [
                (1, [("off", "Advance")], "They're performing for an audience that isn't you."),
                (
                    2,
                    [("off", "Advance"), ("def", "Defend")],
                    "Everyone's laughing at the wrong person — your ally walks through.",
                ),
            ],
        ),
    },
]


def write_proof() -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_class: dict[str, list[dict]] = {}
    for spec in SAMPLE_CARDS:
        by_class.setdefault(spec["class"], []).append(spec)

    sections: list[str] = []
    for cls in ("Rogue", "Fighter", "Bard"):
        chunks = []
        for spec in by_class[cls]:
            chunks.append(
                f'<div class="sample"><div class="stag">{spec["name"]}</div>'
                f'<div class="primer-cards"><div class="cardwrap scope-ability cls-{cls.lower()}">'
                f'{spec["build"]()}</div></div></div>'
            )
        sections.append(f'<h2>{cls}</h2><div class="proof-grid">{"".join(chunks)}</div>')

    legend = """
<div class="legend">
  <span class="lg-item"><span class="yield-tri cat-off"></span> Advance</span>
  <span class="lg-item"><span class="yield-sq cat-def"></span> Defend</span>
  <span class="lg-item"><span class="yield-sq cat-boost"></span> Boost</span>
  <span class="lg-item"><span class="yield-dot cat-res"></span> Restore</span>
</div>
"""

    proof_css = """
body.proof-v6{background:#14100a;padding:28px 20px 48px;color:#f0e6cf;font-family:system-ui,sans-serif;}
body.proof-v6 h1{font-size:20px;letter-spacing:1px;color:#e7d6ac;margin-bottom:6px;}
body.proof-v6 h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;
  margin:32px 0 14px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}
body.proof-v6 p.sub{color:#a08a5c;font-size:14px;margin-bottom:20px;max-width:52rem;line-height:1.5;}
body.proof-v6 .legend{display:flex;flex-wrap:wrap;gap:14px 20px;margin-bottom:20px;font-size:13px;color:#d8c8a0;}
body.proof-v6 .lg-item{display:flex;align-items:center;gap:6px;}
body.proof-v6 .proof-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:32px 24px;align-items:start;}
body.proof-v6 .sample{display:flex;flex-direction:column;align-items:center;gap:10px;}
body.proof-v6 .stag{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#c9b896;text-align:center;}
body.proof-v6 .primer-cards{margin:0;display:flex;justify-content:center;width:100%;}
body.proof-v6 .primer-cards .cardwrap{transform:none;margin-bottom:0;margin-right:0;width:auto;height:auto;}
body.proof-v6 .primer-cards .cardwrap .card{
  width:300px;height:420px;
  background:#f7f0e0;border:0.5px solid #c8a96e;box-shadow:6px 6px 0 #1a1a1a;
}
body.proof-v6 .spark-kw{font-size:9.5px;font-weight:800;font-family:system-ui,-apple-system,sans-serif;}
body.proof-v6 .spark-kw-off{color:#991B1B;}
body.proof-v6 .spark-kw-def{color:#2563EB;}
body.proof-v6 .spark-kw-boost{color:#0d9488;}
body.proof-v6 .spark-kw-res{color:#166534;}
body.proof-v6 .yield-sq.cat-boost{background:#0d9488;}
"""

    PROOF_OUT.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Flourish v6 — Spark narrative samples</title>"
        f"<style>{css}{proof_css}</style></head>"
        '<body class="proof-v6">'
        "<h1>Flourish v6 — Spark narrative pass</h1>"
        f"<p class=\"sub\">12 ability cards · RIGHT layout (flavor · Effect · Spark + invite) · {DATE}</p>"
        f"{legend}"
        f'{"".join(sections)}'
        "</body></html>",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    print(f"Spark narrative samples: {len(SAMPLE_CARDS)} cards")
    for spec in SAMPLE_CARDS:
        print(f"  [{spec['class']}] {spec['name']}")

    if args.write:
        write_proof()
        print(f"Wrote {PROOF_OUT.name}")


if __name__ == "__main__":
    main()
