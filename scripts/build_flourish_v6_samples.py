#!/usr/bin/env python3
"""Flourish v6 sample pass — attempt-only body + minimal mechanical Flourish box.

Nathan direction (July 2026 Discord / Squircle poll): crowd-favorite layout is the LEFT card —
no flavor line, no Effect label, attempt paragraph only, beige Flourish box with cost icons +
category shapes + global keywords (Advance / Defend / Restore) — no per-line narrative gloss.

Proof: flourish-v6-sample-proof.html (12 cards: 4 Rogue, 4 Fighter, 4 Bard)
Compare: Smoke and Mirrors × 3 content variants on the same chrome.

Usage:
  python3 scripts/build_flourish_v6_samples.py
  python3 scripts/build_flourish_v6_samples.py --write
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_spark_flourish_proof import (  # noqa: E402
    SAM_EFFECT,
    ability_card,
    cost_die_icons,
    sam_spark_inverted_card,
)

PROOF_OUT = ROOT / "flourish-v6-sample-proof.html"
DATE = "2026-07-01"

Cat = Literal["off", "def", "res"]


def cat_shape(cat: Cat) -> str:
    if cat == "def":
        return '<span class="yield-sq cat-def" aria-hidden="true"></span>'
    if cat == "off":
        return '<span class="yield-tri cat-off" aria-hidden="true"></span>'
    return '<span class="yield-dot cat-res" aria-hidden="true"></span>'


def flourish_line(cost: int, categories: list[tuple[Cat, str]]) -> str:
    icons = "".join(cat_shape(c) for c, _ in categories)
    label = " + ".join(kw for _, kw in categories)
    return (
        f'<div class="flourish-line">{cost_die_icons(cost)}{icons}'
        f'<span class="flourish-kw">{label}</span></div>'
    )


def flourish_block(*lines: str) -> str:
    body = "".join(lines)
    return f'<div class="csec flourish-sec"><div class="clbl">Flourish</div>{body}</div>'


def attempt_card(
    accent: str,
    idtag: str,
    name: str,
    attempt: str,
    flourish: str,
    *,
    act: bool = True,
    flavor: str | None = None,
    labeled_effect: bool = False,
) -> str:
    """v6 body: optional flavor; attempt with or without Effect label; flourish block."""
    badge = '<span class="cap cap-neutral">Act</span>' if act else '<span class="cap cap-neutral">React</span>'
    flavor_html = ""
    if flavor:
        flavor_html = f'<div class="flv">{flavor}</div><div class="hr"></div>'
    if labeled_effect:
        body_mid = f'<div class="elbl">Effect</div><div class="etxt">{attempt}</div>'
        extra_class = ""
    else:
        body_mid = f'<div class="etxt attempt-txt">{attempt}</div>'
        extra_class = " attempt-only"
    return (
        f'<div class="card acc-{accent}{extra_class}"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{badge}</div>'
        f'<div class="hdr-name">{name}</div></div><div class="cbody">'
        f"{flavor_html}{body_mid}{flourish}</div>"
        f'<div class="idtag">{idtag}</div><div class="tier-float"><span>t1</span></div></div>'
    )


def v6_card(
    accent: str,
    idtag: str,
    name: str,
    attempt: str,
    flourishes: list[tuple[int, list[tuple[Cat, str]]]],
    *,
    act: bool = True,
) -> str:
    lines = [flourish_line(cost, cats) for cost, cats in flourishes]
    return attempt_card(accent, idtag, name, attempt, flourish_block(*lines), act=act)


# ── Smoke and Mirrors comparison variants ───────────────────────────────────

def sam_v6_minimal() -> str:
    return v6_card(
        "rogue",
        "Rogue",
        "Smoke and Mirrors",
        SAM_EFFECT,
        [(1, [("def", "Defend")]), (2, [("def", "Defend"), ("off", "Advance")])],
    )


def sam_v6_with_flavor() -> str:
    return attempt_card(
        "rogue",
        "Rogue",
        "Smoke and Mirrors",
        SAM_EFFECT,
        flourish_block(
            flourish_line(1, [("def", "Defend")]),
            flourish_line(2, [("def", "Defend"), ("off", "Advance")]),
        ),
        flavor="Let them argue about what they saw.",
    )


def sam_v6_narrative_heavy() -> str:
    return sam_spark_inverted_card()


# ── 12 sample cards (4 × Rogue, Fighter, Bard) ────────────────────────────

SAMPLE_CARDS: list[dict] = [
    # Rogue
    {
        "class": "Rogue",
        "name": "Smoke and Mirrors",
        "build": sam_v6_minimal,
        "note": "Canonical v6 — poll winner layout.",
    },
    {
        "class": "Rogue",
        "name": "Sneak Attack",
        "build": lambda: v6_card(
            "rogue",
            "Rogue",
            "Sneak Attack",
            "Perform a <strong>Stealth</strong> check to <strong>Strike</strong> from somewhere "
            "they aren't looking.",
            [(1, [("off", "Advance")]), (2, [("off", "Advance")])],
        ),
    },
    {
        "class": "Rogue",
        "name": "Quick Hands",
        "build": lambda: v6_card(
            "rogue",
            "Rogue",
            "Quick Hands",
            "Perform a <strong>Sleight of Hand</strong> check to lift, switch, or plant something "
            "on someone who isn't watching closely.",
            [(1, [("off", "Advance")]), (2, [("def", "Defend"), ("off", "Advance")])],
        ),
    },
    {
        "class": "Rogue",
        "name": "Misdirection",
        "build": lambda: v6_card(
            "rogue",
            "Rogue",
            "Misdirection",
            "When an ally would be targeted, perform a <strong>Deception</strong> check to redirect "
            "attention elsewhere.",
            [(1, [("def", "Defend")]), (2, [("def", "Defend"), ("off", "Advance")])],
            act=False,
        ),
    },
    # Fighter
    {
        "class": "Fighter",
        "name": "Rallying Cry",
        "build": lambda: v6_card(
            "fighter",
            "Fighter",
            "Rallying Cry",
            "Perform a <strong>Presence</strong> check to shout what needs doing — cut through the noise.",
            [(1, [("def", "Defend")]), (2, [("def", "Defend")])],
        ),
    },
    {
        "class": "Fighter",
        "name": "Disarm",
        "build": lambda: v6_card(
            "fighter",
            "Fighter",
            "Disarm",
            "Perform an <strong>Athletics</strong> check to knock a weapon, shield, or tool from their grip.",
            [(1, [("off", "Advance")]), (2, [("off", "Advance")])],
        ),
    },
    {
        "class": "Fighter",
        "name": "Covering Fire",
        "build": lambda: v6_card(
            "fighter",
            "Fighter",
            "Covering Fire",
            "Perform a <strong>Tactics</strong> check to <strong>Strike</strong> at enemies who might "
            "intercept your allies this beat.",
            [(1, [("def", "Defend")]), (2, [("def", "Defend"), ("off", "Advance")])],
        ),
    },
    {
        "class": "Fighter",
        "name": "Interpose",
        "build": lambda: v6_card(
            "fighter",
            "Fighter",
            "Interpose",
            "When an ally within reach would take a hit, perform a <strong>Faith</strong> check to "
            "<strong>Move</strong> into the blow's path.",
            [(1, [("def", "Defend")]), (2, [("res", "Restore")])],
            act=False,
        ),
    },
    # Bard
    {
        "class": "Bard",
        "name": "Battle Hymn",
        "build": lambda: v6_card(
            "bard",
            "Bard",
            "Battle Hymn",
            "Perform a <strong>Performance</strong> check to keep allies steady under fire — volume, "
            "rhythm, something they can follow.",
            [(1, [("def", "Defend")]), (2, [("def", "Defend"), ("res", "Restore")])],
        ),
    },
    {
        "class": "Bard",
        "name": "Cutting Words",
        "build": lambda: v6_card(
            "bard",
            "Bard",
            "Cutting Words",
            "Perform a <strong>Deception</strong> check to land a verbal jab that throws off their next move.",
            [(1, [("off", "Advance")]), (2, [("off", "Advance")])],
        ),
    },
    {
        "class": "Bard",
        "name": "Steady the Heart",
        "build": lambda: v6_card(
            "bard",
            "Bard",
            "Steady the Heart",
            "Perform a <strong>Medicine</strong> check to talk an ally through fear, pain, or doubt "
            "in the moment.",
            [(1, [("res", "Restore")]), (2, [("def", "Defend"), ("res", "Restore")])],
        ),
    },
    {
        "class": "Bard",
        "name": "Vicious Mockery",
        "build": lambda: v6_card(
            "bard",
            "Bard",
            "Vicious Mockery",
            "Perform a <strong>Deception</strong> check to mock them until everyone in earshot is "
            "watching the wrong thing.",
            [(1, [("off", "Advance")]), (2, [("off", "Advance"), ("def", "Defend")])],
        ),
    },
]

SAM_COMPARE = [
    ("A · Minimal (poll winner)", "No flavor · no Effect label · mechanical Flourish only.", sam_v6_minimal),
    ("B · + flavor line", "Same Flourish box; italic line under the title returns.", sam_v6_with_flavor),
    ("C · Narrative Spark (heavy)", "Effect label + Spark invite boxes — prior direction.", sam_v6_narrative_heavy),
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
            note = spec.get("note", "")
            note_html = f'<div class="vnote">{note}</div>' if note else ""
            chunks.append(
                f'<div class="sample"><div class="stag">{spec["name"]}</div>{note_html}'
                f'<div class="primer-cards"><div class="cardwrap scope-ability">'
                f'{spec["build"]()}</div></div></div>'
            )
        sections.append(f'<h2>{cls}</h2><div class="proof-grid">{"".join(chunks)}</div>')

    compare_chunks = []
    for label, note, build in SAM_COMPARE:
        compare_chunks.append(
            f'<div class="sample variant-sample"><div class="stag">{label}</div>'
            f'<div class="vnote">{note}</div>'
            f'<div class="primer-cards"><div class="cardwrap scope-ability">'
            f"{build()}</div></div></div>"
        )
    compare_section = (
        "<h2>Smoke and Mirrors — content variants</h2>"
        "<p class=\"lab-intro\">Same card chrome (header, caps, idtag). Only the <strong>body copy</strong> "
        "and Flourish/Spark block differ. <strong>A</strong> is the July 2026 poll winner.</p>"
        f'<div class="proof-grid variant-grid">{"".join(compare_chunks)}</div>'
    )

    legend = """
<div class="legend">
  <span class="lg-item"><span class="yield-tri cat-off"></span> Advance — progress the objective</span>
  <span class="lg-item"><span class="yield-sq cat-def"></span> Defend — protect an ally / shed threat</span>
  <span class="lg-item"><span class="yield-dot cat-res"></span> Restore — recover Resolve or hope</span>
</div>
<div class="proc box">
  <strong>v6 content rules (prototype):</strong> The card body states only what you <em>attempt</em> —
  no guaranteed on-success outcome. In combat, the attempt still feeds the normal Offense/Defense
  roll; out of combat the GM can frame it as a Contest. On natural <strong>6</strong>s, you may spend
  each Crit to take a <strong>Flourish</strong> line instead of rolling the bonus die — category icons
  show the pool; keywords are global (not card-specific jargon).
</div>
"""

    proof_css = """
body.proof-v6{background:#14100a;padding:28px 20px 48px;color:#f0e6cf;font-family:system-ui,sans-serif;}
body.proof-v6 h1{font-size:20px;letter-spacing:1px;color:#e7d6ac;margin-bottom:6px;}
body.proof-v6 h2{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#c9a24a;
  margin:32px 0 14px;border-bottom:1px solid #3a2c19;padding-bottom:6px;}
body.proof-v6 p.sub,body.proof-v6 p.lab-intro{color:#a08a5c;font-size:14px;margin-bottom:20px;max-width:52rem;line-height:1.5;}
body.proof-v6 .legend{display:flex;flex-wrap:wrap;gap:14px 20px;margin-bottom:16px;font-size:13px;color:#d8c8a0;}
body.proof-v6 .lg-item{display:flex;align-items:center;gap:6px;}
body.proof-v6 .box{background:#1b130b;border:1px solid #3a2c19;border-radius:8px;padding:12px 14px;
  font-size:13px;line-height:1.55;color:#d8c8a0;margin-bottom:24px;max-width:52rem;}
body.proof-v6 .proof-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:32px 24px;align-items:start;}
body.proof-v6 .variant-grid{grid-template-columns:repeat(auto-fill,minmax(300px,1fr));}
body.proof-v6 .sample{display:flex;flex-direction:column;align-items:center;gap:10px;}
body.proof-v6 .variant-sample .vnote{font-size:11px;color:#8a7a5c;text-align:center;max-width:280px;line-height:1.45;}
body.proof-v6 .stag{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#c9b896;text-align:center;}
body.proof-v6 .primer-cards{margin:0;display:flex;justify-content:center;width:100%;}
body.proof-v6 .primer-cards .cardwrap{transform:none;margin-bottom:0;margin-right:0;width:auto;height:auto;}
body.proof-v6 .primer-cards .cardwrap .card{
  width:300px;height:420px;
  background:#f7f0e0;border:0.5px solid #c8a96e;box-shadow:6px 6px 0 #1a1a1a;
}
"""

    PROOF_OUT.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Flourish v6 samples — attempt + minimal Flourish box</title>"
        f"<style>{css}{proof_css}</style></head>"
        '<body class="proof-v6">'
        "<h1>Flourish v6 — sample pass</h1>"
        f"<p class=\"sub\">12 ability cards (4 Rogue · 4 Fighter · 4 Bard) · {DATE} · "
        "content prototype — card chrome unchanged.</p>"
        f"{legend}"
        f"{compare_section}"
        f'{"".join(sections)}'
        "</body></html>",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    print(f"Flourish v6 samples: {len(SAMPLE_CARDS)} cards + {len(SAM_COMPARE)} Smoke and Mirrors variants")
    for spec in SAMPLE_CARDS:
        print(f"  [{spec['class']}] {spec['name']}")

    if args.write:
        write_proof()
        print(f"Wrote {PROOF_OUT.name}")
    else:
        print("Dry run — pass --write to emit proof HTML")


if __name__ == "__main__":
    main()
