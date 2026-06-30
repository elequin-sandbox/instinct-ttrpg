#!/usr/bin/env python3
"""Build Barbarian Rage + Retribution Core card HTML.

Usage:
  python3 scripts/build_barbarian_core.py              # dry-run
  python3 scripts/build_barbarian_core.py --write    # patch card-data.js + batch JSON
  python3 scripts/build_barbarian_core.py --push     # write + push to Baserow
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

BATCH_OUT = ROOT / "scripts" / "barbarian_core_batch.json"
PROOF_OUT = ROOT / "barbarian-core-proof.html"
DATE = "2026-06-30"

MISS = '<span class="kw kw-miss">Miss</span>'
HD = '<span class="kw kw-hd">Hit Die</span>'
BOOST1 = '<span class="kw kw-boost">Boost 1</span>'
BOOST3 = '<span class="kw kw-boost">Boost 3</span>'
RESOLVE3 = '<span class="kw kw-resolve">Resolve 3</span>'

RAGE = {
    "id": 431,
    "key": "rage-barbarian-core",
    "name": "Rage",
    "card_type": "Core",
    "effect_plain": (
        "Core Rage Everything that hurts you makes you worse to face. "
        "Place dice into your Rage Pool whenever you: Roll a Miss (1) during any Check; "
        "Lose a Hit Die. Whenever you have 5 or more Rage Dice, you enter a Frenzy: "
        "You must play the top card of your deck immediately — narrate how your rage shapes it. "
        "If it is an Action, it gains Boost 3. If it is not, you gain Resolve 3. "
        "Then clear your Rage Pool. Barbarian"
    ),
}

RETRIBUTION = {
    "id": 432,
    "key": "retribution-barbarian-core",
    "name": "Retribution",
    "card_type": "React",
    "effect_plain": (
        "Core React Retribution They shouldn't have touched them. "
        "After an ally suffers from a negative effect, you may play an Action as a Reaction "
        "against the source of that negative effect. Spend 3 Rage Dice and roll with Boost 1 "
        "on the attempt. Barbarian"
    ),
}


def build_rage_html() -> str:
    return (
        '<div class="card barbarian acc-barbarian">'
        '<div class="hdr">'
        '<div class="hdr-top"><span class="cap cap-neutral">Core</span><span></span></div>'
        '<div class="hdr-name">Rage</div>'
        '<div class="hdr-sub">Everything that hurts you makes you worse to face.</div>'
        "</div>"
        '<div class="card-body">'
        '<div class="effect-text">Place dice into your <strong>Rage Pool</strong> whenever you:</div>'
        '<div class="choose-list">'
        f'<div class="choose-item">Roll a {MISS} (1) during any <strong>Check</strong></div>'
        f'<div class="choose-item">Lose a {HD}</div>'
        "</div>"
        '<div class="rule"></div>'
        '<div class="effect-text">Whenever you have 5 or more <strong>Rage Dice</strong>, '
        "you enter a <strong>Frenzy</strong>:</div>"
        '<div class="choose-list">'
        '<div class="choose-item">You must play the top card of your deck immediately — '
        "narrate how your rage shapes it</div>"
        f'<div class="choose-item">If it is an <strong>Action</strong>, it gains {BOOST3}. '
        f"If it is not, you gain {RESOLVE3}</div>"
        '<div class="choose-item">Then clear your <strong>Rage Pool</strong></div>'
        "</div>"
        "</div>"
        '<div class="idtag">Barbarian</div>'
        "</div>"
    )


def build_retribution_html() -> str:
    hdr_top = (
        '<div class="hdr-top"><span style="display:inline-flex;gap:3px;align-items:center;">'
        '<span class="cap cap-neutral">Core</span><span class="cap cap-neutral">React</span>'
        "</span><span></span></div>"
    )
    return (
        '<div class="card barbarian acc-barbarian">'
        f'<div class="hdr">{hdr_top}'
        '<div class="hdr-name">Retribution</div>'
        '<div class="hdr-sub">They shouldn\'t have touched them.</div>'
        "</div>"
        '<div class="card-body">'
        '<div class="effect-text">After an ally suffers from a negative effect, you may play an '
        f'<strong>Action</strong> as a <strong>Reaction</strong> against the source of that negative '
        f"effect. Spend 3 <strong>Rage Dice</strong> and roll with {BOOST1} on the attempt.</div>"
        "</div>"
        '<div class="idtag">Barbarian</div>'
        "</div>"
    )


def patch_cards(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    specs = [
        (RAGE, build_rage_html()),
        (RETRIBUTION, build_retribution_html()),
    ]
    by_key = {c.get("Card_Key"): c for c in cards}
    batch: list[dict] = []
    for spec, html in specs:
        card = by_key[spec["key"]]
        card["HTML"] = html
        card["EffectText_Plain"] = spec["effect_plain"]
        card["Card_Type"] = spec["card_type"]
        card["Last_Rework_Date"] = DATE
        batch.append(
            {
                "id": spec["id"],
                "Name": spec["name"],
                "Card_Key": spec["key"],
                "Card_Type": spec["card_type"],
                "HTML": html,
                "EffectText_Plain": spec["effect_plain"],
                "Last_Rework_Date": DATE,
            }
        )
    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Generated by scripts/build_barbarian_core.py — do not edit manually. "
        f"Last updated: {DATE}\n"
        f"// Full regen: py -3 scripts/regenerate_card_data.py\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof(rage_html: str, retribution_html: str) -> None:
    css = """
:root{--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;line-height:1.55;max-width:720px;margin-bottom:24px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:28px;align-items:start;max-width:720px;}
.stag{font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#e7d6ac;text-align:center;margin-bottom:8px;}
.acc-barbarian{--a:#9E2B2B;--ad:#822323;--al:#E8C4A8;--ah:#F5EDE4;--at:#f5eedd;}
.kw{display:inline-block;padding:0 4px;border-radius:3px;font-size:10px;font-weight:700;vertical-align:middle;line-height:1.5;font-family:system-ui,sans-serif;}
.kw-boost{background:#0F766E;color:#CCFBF1;}.kw-resolve{background:#166534;color:#F0FDF4;}
.kw-miss{background:#7F1D1D;color:#FEF2F2;}.kw-hd{background:#991B1B;color:#FEF2F2;}
.cardwrap{position:relative;width:2.5in;height:3.5in;margin:0 auto;overflow:hidden;}
.scope-core .card{position:relative;display:flex;flex-direction:column;width:2.5in;height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;color:#241a08;overflow:hidden;box-shadow:5px 5px 0 rgba(0,0,0,.55);}
.scope-core .hdr{padding:7px 9px 5px;background:var(--ah);border-bottom:1px solid rgba(0,0,0,.1);flex-shrink:0;}
.scope-core .hdr-top{display:flex;justify-content:space-between;align-items:center;min-height:16px;}
.scope-core .cap{display:inline-flex;border:1.5px solid;border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;}
.scope-core .cap-neutral{border-color:#3a3320;color:#3a3320;}
.scope-core .hdr-name{font-family:'EB Garamond',Georgia,serif;font-weight:700;font-size:14px;text-align:center;padding:3px 10px;margin:4px 0 2px;color:var(--ad);background:var(--al);border-top:2px solid var(--a);border-bottom:2px solid var(--a);}
.scope-core .hdr-sub{font-style:italic;font-size:9px;color:#5a4020;text-align:center;line-height:1.35;padding:0 4px 2px;}
.scope-core .card-body{flex:1;padding:4px 9px 28px;display:flex;flex-direction:column;gap:3px;overflow:hidden;}
.scope-core .effect-text{font-size:9px;line-height:1.4;color:#1a1008;}
.scope-core .choose-list{display:flex;flex-direction:column;gap:2px;}
.scope-core .choose-item{font-size:9.35px;line-height:1.4;color:#1a1008;padding-left:8px;position:relative;}
.scope-core .choose-item::before{content:'·';position:absolute;left:0;color:#8a6a30;}
.scope-core .rule{height:0.5px;background:#c8a96e;opacity:.45;margin:2px 0;}
.scope-core .idtag{position:absolute;left:8px;bottom:7px;border:1.5px solid var(--a);color:var(--ad);background:var(--at);border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;}
"""
    body = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600;700&display=swap" rel="stylesheet">
<title>Instinct RPG — Barbarian Core Proof</title><style>{css}</style></head><body>
<h1>Barbarian Core — Rage + Retribution</h1>
<p class="sub">June 30 2026 rework. Rage: Miss + Hit Die fuel, Frenzy at 5+ Rage Dice. Retribution: Core React, spend 3 Rage Dice.</p>
<div class="grid">
<div><div class="stag">Rage (Core)</div><div class="cardwrap"><div class="scope-core cls-barbarian">{rage_html}</div></div></div>
<div><div class="stag">Retribution (Core · React)</div><div class="cardwrap"><div class="scope-core cls-barbarian">{retribution_html}</div></div></div>
</div></body></html>"""
    PROOF_OUT.write_text(body, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    cards = load_cards()
    cards, batch = patch_cards(cards)

    print("Barbarian Core cards:")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']} ({item['Card_Type']})")

    if args.write or args.push:
        write_card_data(cards)
        write_proof(build_rage_html(), build_retribution_html())
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name}, {PROOF_OUT.name}, and {BATCH_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run only. Pass --write or --push to apply.")


if __name__ == "__main__":
    main()
