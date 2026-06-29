#!/usr/bin/env python3
"""Patch card-data.js with Paladin Oath rework (when full Baserow regen unavailable)."""
from __future__ import annotations

import json
import re
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))
OUT = ROOT / "card-data.js"
from scripts.build_oath_html import OATHS, build  # noqa: E402
from scripts.regenerate_card_data import flavor_plain, effect_plain, guess_class, guess_type  # noqa: E402

LOADOUT_HTML = (
    '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
    '<span class="cap cap-neutral">Core</span><span></span></div>'
    '<div class="hdr-name">Loadout</div>'
    '<div class="hdr-sub">You go in with your word already given.</div></div>'
    '<div class="card-body"><div class="zone-label">Standard Deck Recipe</div>'
    '<div class="loadout-recipe"><div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">10 <span class="kw kw-paladin">Paladin</span> Ability Cards</span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">2 other Core <span class="kw kw-paladin">Paladin</span> cards</span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">1 <span class="kw kw-background">Background</span></span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">1 <span class="kw kw-ancestry">Ancestry</span></span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">1 <span class="kw kw-bond">Bond</span></span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">5 <span class="kw kw-instinct">Instincts</span></span></div>'
    '<div class="recipe-row"><span class="recipe-dot">·</span>'
    '<span class="recipe-text">1 <span class="kw kw-item">Item</span> (Tier 1)</span></div></div>'
    '<div class="rule"></div><div class="zone-label">Special Setup</div>'
    '<div class="effect-text" style="font-size:8.5px; color:#5a4a20; font-style:italic;">'
    "Choose 1 Oath card at character creation. It begins play in your Active area."
    "</div></div><div class=\"idtag\">Paladin</div></div>"
)

BUILD_HTML = (
    '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
    '<span class="cap cap-neutral">Core</span><span></span></div>'
    '<div class="hdr-name">Build Your Deck</div>'
    '<div class="hdr-sub">Paladin · character creation steps, in order.</div></div>'
    '<div class="card-body"><table style="width:100%;font-size:7.5px;border-collapse:collapse;color:#2a1a0a">'
    '<thead><tr style="border-bottom:1px solid #c8a84b"><th style="text-align:left;padding:1px 3px;font-size:7px">#</th>'
    '<th style="text-align:left;padding:1px 3px;font-size:7px">Card</th>'
    '<th style="text-align:right;padding:1px 3px;font-size:7px">Draft</th></tr></thead><tbody>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">1</td><td style="padding:1px 3px">'
    '<span class="kw kw-paladin">Paladin</span> Core cards</td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">auto</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">2</td><td style="padding:1px 3px">'
    '<span class="kw kw-background">Background</span></td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">5 → 1</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">3</td><td style="padding:1px 3px">'
    '<span class="kw kw-ancestry">Ancestry</span></td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">5 → 1</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">4</td><td style="padding:1px 3px">'
    '<span class="kw kw-bond">Bond</span></td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">5 → 1</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">5</td><td style="padding:1px 3px">'
    '<span class="kw kw-flaw">Flaw</span></td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">5 → 1</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">6</td><td style="padding:1px 3px">'
    '<span class="kw kw-instinct">Instinct</span> ×5</td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">3 → 1 each</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">7</td><td style="padding:1px 3px">'
    'Oath card → Active area</td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">pool → pick 1</td></tr>'
    '<tr><td style="padding:1px 3px;color:#7a6a4a;font-size:7px">8</td><td style="padding:1px 3px">'
    '<span class="kw kw-item">Item</span> (Tier 1)</td>'
    '<td style="text-align:right;padding:1px 3px;font-style:italic;color:#5a4a20;font-size:7px">5 → 1</td></tr>'
    "</tbody></table></div><div class=\"idtag\">Paladin</div></div>"
)

OATH_IDS = {
    "oath-of-devotion-paladin-core": 697,
    "oath-of-vengeance-paladin-core": 698,
    "oath-of-the-crown-paladin-core": 699,
}


def card_obj(row_id: int, name: str, key: str, html: str) -> dict:
    card_type = guess_type(html)
    return {
        "id": row_id,
        "Name": name,
        "Card_Key": key,
        "Class": guess_class(html),
        "Card_Type": card_type,
        "Scope": "Core" if card_type == "Core" else "ability",
        "Ruleset": "base",
        "Status": "current",
        "Last_Rework_Date": "2026-06-28",
        "HTML": html,
        "FlavorText_Plain": flavor_plain(html),
        "EffectText_Plain": effect_plain(html),
    }


def main() -> None:
    text = OUT.read_text(encoding="utf-8")
    m = re.search(r"window\.CARD_DATA\s*=\s*", text)
    if not m:
        raise SystemExit("CARD_DATA assignment not found")
    cards = json.loads(text[m.end() :].strip().rstrip(";"))
    cards = [c for c in cards if c.get("id") != 414 and c.get("Card_Key") != "conviction-defiance-paladin-core"]
    by_id = {c["id"]: c for c in cards}

    by_id[415] = card_obj(415, "Loadout", "loadout-paladin-core", LOADOUT_HTML)
    by_id[596] = card_obj(596, "Build Your Deck — Paladin", "build-your-deck-paladin", BUILD_HTML)

    for o in OATHS:
        html = build(o)
        row_id = OATH_IDS[o["key"]]
        by_id[row_id] = card_obj(row_id, o["name"], o["key"], html)

    cards = sorted(by_id.values(), key=lambda c: c["id"])
    today = date.today().isoformat()
    header = (
        f"// Generated by scripts/patch_card_data_oaths.py — do not edit manually. Last updated: {today}\n"
        f"// Source: Baserow table 911939 patch (Paladin Oath rework)\n"
        f"// Full regen: py -3 scripts/regenerate_card_data.py\n"
    )
    OUT.write_text(header + "window.CARD_DATA = " + json.dumps(cards, separators=(",", ":")) + ";\n", encoding="utf-8")
    print(f"Patched {OUT} — {len(cards)} cards")


if __name__ == "__main__":
    main()
