#!/usr/bin/env python3
"""Build Background Snap Check + Mill HTML for all 12 deck cards.

Usage:
  python3 scripts/build_background_snap.py              # dry-run
  python3 scripts/build_background_snap.py --write    # patch card-data.js + batch JSON
  python3 scripts/build_background_snap.py --push     # write + push to Baserow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.boon_snap_render import (  # noqa: E402
    Option,
    render_mill_line,
    render_options_list,
    render_react_trigger,
    render_snap_compact,
)
from scripts.strip_origin_stems import BACKGROUND_FLAVOR, CARD_DATA, push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "background_snap_batch.json"
PROOF_OUT = ROOT / "background-snap-proof.html"
DATE = "2026-06-29"
BOOST = '<span class="kw kw-boost">Boost 1</span>'

BACKGROUNDS: list[dict] = [
    {
        "id": 469,
        "name": "Gambler",
        "key": "gambler-background",
        "react_condition": "luck could plausibly tip your way",
        "options": [
            ("Call It", "name one small true thing about this <strong>Scene</strong>; the GM builds from it"),
            ("Ride the Wave", f"press your luck; take {BOOST} on your next check where chance matters"),
            ("Tip the Table", f"nudge fate toward an ally; they take {BOOST} on their next check"),
        ],
    },
    {
        "id": 470,
        "name": "Field Medic",
        "key": "field-medic-background",
        "react_condition": "precision matters and the pressure is high",
        "options": [
            ("Steady the Hand", f"your hands do exactly what they must; take {BOOST} on the careful action"),
            ("Hold Them Together", "keep someone beside you calm enough to do their part"),
            ("Work the Margin", "narrate the small, exact thing that keeps it from getting worse"),
        ],
    },
    {
        "id": 471,
        "name": "Inspector",
        "key": "inspector-background",
        "react_condition": "close study could reveal what others missed",
        "options": [
            ("Probe", "ask the GM one honest question about what you're studying; they answer truthfully"),
            ("Spot the Tell", "name one detail that doesn't fit; the GM confirms if it's there"),
            ("Name the Risk", "name the fastest way this goes wrong; the GM answers honestly"),
        ],
    },
    {
        "id": 472,
        "name": "Trade Road Courier",
        "key": "trade-road-courier-background",
        "react_condition": "a familiar face or name could change how this moment goes",
        "options": [
            ("Known Face", "declare who or what recognizes you; the GM plays it accordingly"),
            ("Dropped Name", "invoke a connection; one NPC shifts their stance"),
            ("Fast Talk", f"slip through on reputation; take {BOOST} on your next social check"),
        ],
    },
    {
        "id": 473,
        "name": "Cutpurse",
        "key": "cutpurse-background",
        "react_condition": "precision and control matter more than force",
        "options": [
            ("Light Fingers", "take or place something small, unseen"),
            ("Slip the Notice", "move through a watched space as if you belong"),
            ("Misdirect", "draw eyes elsewhere so the move lands clean"),
        ],
    },
    {
        "id": 474,
        "name": "Pit Fighter",
        "key": "pit-fighter-background",
        "react_condition": "you deliberately face something that would shake anyone else",
        "options": [
            ("Walk Into It", f"close the distance you're meant to flee; take {BOOST} on what it takes"),
            ("Set the Tone", "let them see you unbothered; steady an ally beside you"),
            ("Stare It Down", "make the threatening thing hesitate"),
        ],
    },
    {
        "id": 475,
        "name": "Musician",
        "key": "musician-background",
        "react_condition": "timing is everything in this beat",
        "options": [
            ("Right on the Beat", "act at the exact moment it lands hardest"),
            ("Set the Pace", "give the group a rhythm to move on together"),
            ("Feel the Turn", "sense when the moment is about to change; call it"),
        ],
    },
    {
        "id": 476,
        "name": "Street-Raised",
        "key": "street-raised-background",
        "react_condition": "things turn sharp or strange",
        "options": [
            ("Already Knew", "react as if you saw it coming — because part of you did"),
            ("Read the Angle", "spot who benefits; say so"),
            ("Keep Your Footing", "stay steady; give the others something to hold to"),
        ],
    },
    {
        "id": 477,
        "name": "Caravan Guard",
        "key": "caravan-guard-background",
        "react_condition": "differences would be a barrier between people",
        "options": [
            ("Find Common Ground", "name the thing both sides actually want"),
            ("Speak Their Way", "frame it so it lands for them, not you"),
            ("Vouch", "put your own standing behind someone to bridge the gap"),
        ],
    },
    {
        "id": 478,
        "name": "Pilgrim",
        "key": "pilgrim-background",
        "react_condition": "you meet someone driven by the same devotion",
        "options": [
            ("Recognize the Road", "name what you share; you both move easier for it"),
            ("Offer the Path", "open a door only a fellow traveler would see"),
            ("Invoke It", "call on the shared cause; one listener responds honestly"),
        ],
    },
    {
        "id": 479,
        "name": "Ascetic",
        "key": "ascetic-background",
        "react_condition": "your conviction is tested — by pain, pressure, or doubt",
        "options": [
            ("Endure It", "take the cost without bending; let it show"),
            ("Steady the Doubting", "hold someone else's faith up when theirs slips"),
            ("Refuse the Bargain", "turn down the easy way; narrate why"),
        ],
    },
    {
        "id": 480,
        "name": "Pathfinder",
        "key": "pathfinder-background",
        "react_condition": "you're navigating uncertain or dangerous ground",
        "options": [
            ("Read the Land", "name a feature of the terrain and how you'll use it"),
            ("Find the Way", f"pick the route others would miss; take {BOOST} on the crossing"),
            ("Set the Trail", "lead so the group moves safe and quick"),
        ],
    },
]


def render_background_snap(card: dict) -> str:
    flavor = BACKGROUND_FLAVOR.get(card["name"])
    if not flavor:
        raise ValueError(f"Missing BACKGROUND_FLAVOR for {card['name']!r}")
    return (
        f'<div class="card bf-bg acc-background">'
        f'<div class="hdr">'
        f'<div class="hdr-top">'
        f'<span class="cap cap-accent">Background</span>'
        f'<span class="cap cap-neutral">React</span>'
        f"</div>"
        f'<div class="hdr-name">{card["name"]}</div>'
        f"</div>"
        f'<div class="bf-body">'
        f'<div class="bf-flv">{flavor}</div>'
        f"{render_react_trigger(card['react_condition'])}"
        f"{render_options_list(card['options'])}"
        f"{render_snap_compact()}"
        f"{render_mill_line()}"
        f"</div>"
        f"</div>"
    )


def load_cards() -> list[dict]:
    text = CARD_DATA.read_text(encoding="utf-8")
    m = re.search(r"window\.CARD_DATA\s*=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse card-data.js")
    return json.loads(m.group(1))


def patch_card_data(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c["key"]: c for c in BACKGROUNDS}
    batch: list[dict] = []
    for card in cards:
        key = card.get("Card_Key", "")
        if key not in by_key:
            continue
        spec = by_key[key]
        html = render_background_snap(spec)
        card["HTML"] = html
        card["Last_Rework_Date"] = DATE
        batch.append(
            {
                "id": spec["id"],
                "Name": spec["name"],
                "Card_Key": key,
                "HTML": html,
                "Last_Rework_Date": DATE,
            }
        )
    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Auto-generated card data — do not hand-edit; regenerate from Baserow.\n"
        f"// Source: build_background_snap.py ({DATE})\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof_html() -> None:
    rows = []
    for c in BACKGROUNDS:
        rows.append(
            f'<div class="sample"><div class="stag">{c["name"]}</div>'
            f'<div class="cardwrap">{render_background_snap(c)}</div></div>'
        )
    css = """\
:root{--snap:#6D28D9;--snap-l:#EDE9FE;--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,sans-serif;background:#16110a;color:#f0e6cf;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:20px;line-height:1.55;max-width:920px;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;align-items:start;}
.sample{display:flex;flex-direction:column;gap:10px;}.stag{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--snap-l);text-align:center;}
.kw{display:inline-block;padding:0 5px;border-radius:3px;font-size:10px;font-weight:700;vertical-align:middle;line-height:1.6;font-family:system-ui,sans-serif;}
.kw-boost{background:#0F766E;color:#CCFBF1;}.kw-snap{background:var(--snap);color:var(--snap-l);font-size:9px;min-width:1.6em;text-align:center;}
.kw-mill{background:#0C4A6E;color:#BAE6FD;}
.acc-background{--a:#2f6da8;--ad:#27598a;--al:#b8cde1;--ah:#eaf0f6;}
.cardwrap{width:2.5in;margin:0 auto;}.cardwrap .card{box-shadow:5px 5px 0 rgba(0,0,0,.55);}
.card{position:relative;border-left:5px solid var(--a);display:flex;flex-direction:column;width:2.5in;min-height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;color:#241a08;overflow:hidden;}
.hdr{padding:7px 9px 5px;background:var(--ah);border-bottom:1px solid rgba(0,0,0,.1);}
.hdr-top{display:flex;justify-content:space-between;align-items:center;min-height:16px;}
.cap{display:inline-flex;border:1.5px solid;border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;}
.cap-neutral{border-color:#3a3320;color:#3a3320;}.cap-accent{border-color:var(--ad);color:var(--ad);}
.hdr-name{font-family:'EB Garamond',Georgia,serif;font-weight:700;font-size:16.5px;text-align:center;padding:3px 12px;margin:6px -1px 2px;color:var(--ad);background:var(--al);border-top:2px solid var(--a);border-bottom:2px solid var(--a);clip-path:polygon(0 0,100% 0,calc(100% - 11px) 50%,100% 100%,0 100%,11px 50%);}
.bf-body{flex:1;padding:7px 9px 10px;display:flex;flex-direction:column;gap:5px;font-size:10.5px;line-height:1.42;}
.bf-flv{font-style:italic;color:#5a4020;font-size:10px;}
.anc-trigger{display:flex;flex-direction:column;gap:2px;}.anc-freq{font-size:7.5px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#8a6a40;}
.anc-callout{font-style:normal;font-weight:600;font-size:10px;line-height:1.45;color:#1c1408;padding:5px 7px;border-left:3px solid #6D28D9;background:rgba(109,40,217,.08);border-radius:0 4px 4px 0;}
.bf-choices{display:flex;flex-direction:column;gap:4px;}.bf-choice{font-size:10px;line-height:1.45;color:#1c1408;}
.snap-compact{margin-top:auto;padding-top:5px;display:flex;flex-wrap:wrap;align-items:center;gap:3px 5px;font-size:9px;color:#5a4520;border-top:0.5px solid rgba(200,169,110,.45);}
.snap-chip{display:inline-flex;align-items:center;gap:3px;white-space:nowrap;}.snap-dot{opacity:.45;}
.bf-mill{font-size:9px;line-height:1.4;color:#4a6080;padding-top:3px;border-top:0.5px dashed rgba(12,74,110,.35);}
"""
    html = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<link href=\"https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600;700&display=swap\" rel=\"stylesheet\">"
        "<title>Instinct RPG — Background Snap Check Proof</title>"
        f"<style>{css}</style></head><body>"
        "<h1>Background Snap Check — Proof</h1>"
        "<p class=\"sub\">All 12 Backgrounds · <strong>React</strong> + Snap Check · "
        "<span class=\"kw kw-mill\">Mill</span> at scene start.</p>"
        f'<div class="grid">{"".join(rows)}</div>'
        "</body></html>"
    )
    PROOF_OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {PROOF_OUT.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    for spec in BACKGROUNDS:
        html = render_background_snap(spec)
        print(f"{spec['key']} — {len(html)} chars")

    if args.write or args.push:
        cards = load_cards()
        cards, batch = patch_card_data(cards)
        if len(batch) != len(BACKGROUNDS):
            raise SystemExit(f"Expected {len(BACKGROUNDS)} background rows, got {len(batch)}")
        write_card_data(cards)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_proof_html()
        print(f"Wrote {CARD_DATA.name} and {BATCH_OUT.name}")
        if args.push:
            push_baserow(batch)
    elif not args.write:
        print("Dry run only. Pass --write or --push to apply.")


if __name__ == "__main__":
    main()
