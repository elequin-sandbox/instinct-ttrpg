#!/usr/bin/env python3
"""Build Ancestry Snap Check HTML for all 10 deck cards.

Usage:
  python3 scripts/build_ancestry_snap.py              # dry-run
  python3 scripts/build_ancestry_snap.py --write    # patch card-data.js + batch JSON
  python3 scripts/build_ancestry_snap.py --push     # write + push to Baserow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.strip_origin_stems import CARD_DATA, push_baserow  # noqa: E402

BATCH_OUT = ROOT / "scripts" / "ancestry_snap_batch.json"
DATE = "2026-06-29"

# (verb, description) — CRPG syntax; Boost 1 max; niche fiction only
Option = tuple[str, str]

ANCESTRIES: list[dict] = [
    {
        "id": 505,
        "name": "Human",
        "key": "human-ancestry",
        "timing": "Act",
        "flavor": "You were not born with magic or ancient lineage. You were born with will.",
        "act_phrase": "push through with sheer determination when a moment is stuck",
        "options": [
            ("Press On", "name what you're reaching for; take <span class=\"kw kw-boost\">Boost 1</span> on your next check toward it"),
            ("Find a Way", "improvise an angle nobody else thought of; the GM names what opens"),
            ("Rally", "steady an ally beside you; they take <span class=\"kw kw-boost\">Boost 1</span> on their next check"),
        ],
    },
    {
        "id": 506,
        "name": "Elf",
        "key": "elf-ancestry",
        "timing": "Act",
        "flavor": "Something in you is older than this world, and it always notices.",
        "act_phrase": "attune to old memory or a hidden detail",
        "options": [
            ("Listen", "ask the GM one honest question about this <strong>Scene</strong>; they answer truthfully"),
            ("Trace", "name one detail others missed; the GM confirms if it's there"),
            ("Stillness", "read the room's weight; take <span class=\"kw kw-boost\">Boost 1</span> on your next social check"),
        ],
    },
    {
        "id": 507,
        "name": "Dwarf",
        "key": "dwarf-ancestry",
        "timing": "React",
        "flavor": "You were carved from stone and stubbornness — and it shows.",
        "react_condition": "a blow — physical, social, or emotional — would stagger you",
        "options": [
            ("Absorb It", "take the hit and stay standing; narrate what you refuse to show"),
            ("Dig In", "anchor the beat; the <strong>Scene</strong> must work around you"),
            ("Answer Back", "a short, grounded reply that shifts the pressure"),
        ],
    },
    {
        "id": 508,
        "name": "Halfling",
        "key": "halfling-ancestry",
        "timing": "React",
        "flavor": "You've gotten away with things that should have ended you more times than you can count.",
        "react_condition": "a bad roll would cost you in a tight moment",
        "options": [
            ("Slip Away", "narrate how you duck the worst of it"),
            ("Look Harmless", "seem too small to bother; someone looks past you"),
            ("Small Fortune", "name one absurd lucky break; the GM plays it fairly"),
        ],
    },
    {
        "id": 509,
        "name": "Half-Orc",
        "key": "half-orc-ancestry",
        "timing": "React",
        "flavor": "You have been underestimated your whole life. You have learned to use that.",
        "react_condition": "the <strong>Scene</strong> pushes you to yield or fall",
        "options": [
            ("Stand", "stay on your feet; narrate what keeps you there"),
            ("Snarl", "let your heritage show; one foe hesitates"),
            ("Press", "ride the refusal; take <span class=\"kw kw-boost\">Boost 1</span> on your very next check"),
        ],
    },
    {
        "id": 510,
        "name": "Tiefling",
        "key": "tiefling-ancestry",
        "timing": "Act",
        "flavor": "You carry something ancient and unholy in your blood. It is not a curse. It is yours.",
        "act_phrase": "bend a social beat with your unsettling heritage",
        "options": [
            ("Shadow", "your presence shifts the mood; name what changes"),
            ("Bargain", "offer a small infernal favor; the GM names the price"),
            ("Whisper", "speak one truth that shouldn't be known; one listener reacts honestly"),
        ],
    },
    {
        "id": 511,
        "name": "Dragonborn",
        "key": "dragonborn-ancestry",
        "timing": "Act",
        "flavor": "Every choice you make is an answer to what your bloodline means.",
        "act_phrase": "let your draconic nature unsettle or awe",
        "options": [
            ("Bearing", "your stillness or voice changes the room's temperature"),
            ("Ember", "a small elemental tell; name it; the GM plays it fairly"),
            ("Lineage", "name what your blood remembers; ask one honest GM question"),
        ],
    },
    {
        "id": 512,
        "name": "Gnome",
        "key": "gnome-ancestry",
        "timing": "Act",
        "flavor": "Your mind moves in directions that simply do not occur to anyone else.",
        "act_phrase": "find an odd angle or trick that could help",
        "options": [
            ("Tinker", "use something here in an unintended way; name how"),
            ("Misdirect", "draw eyes elsewhere; take <span class=\"kw kw-boost\">Boost 1</span> on your next sneaky check"),
            ("Spark", "name the overlooked solution; the GM confirms if it could work"),
        ],
    },
    {
        "id": 513,
        "name": "Half-Elf",
        "key": "half-elf-ancestry",
        "timing": "Act",
        "flavor": "You belong to neither world completely. You have learned to make that a strength.",
        "act_phrase": "bridge two peoples or ways of seeing",
        "options": [
            ("Translate", "name the thread between two opposed parties; they hear you"),
            ("Soften", "ease tension with the right tone; one NPC shifts their stance"),
            ("Switch", "lean elven grace or human drive; take <span class=\"kw kw-boost\">Boost 1</span> on your next check"),
        ],
    },
    {
        "id": 514,
        "name": "Orc",
        "key": "orc-ancestry",
        "timing": "Act",
        "flavor": "You are built for things that require more than most people have.",
        "act_phrase": "bring raw force or presence to shift the moment",
        "options": [
            ("Rush", "close distance; name what gives way before you"),
            ("Roar", "your voice carries; one ally takes <span class=\"kw kw-boost\">Boost 1</span> on their next <strong>Action</strong>"),
            ("Break", "name what cracks, splinters, or yields under your weight"),
        ],
    },
]


def _trigger_callout_html(card: dict) -> str:
    timing = card["timing"]
    if timing == "React":
        body = (
            f"When {card['react_condition']}, "
            f"<strong>React</strong> with a <strong>Snap Check</strong>:"
        )
        kind = "react"
    else:
        body = (
            f"You may take an <strong>Action</strong> to {card['act_phrase']} "
            f"by making a <strong>Snap Check</strong>:"
        )
        kind = "act"
    return (
        '<div class="anc-trigger">'
        '<div class="anc-freq">Once per Scene</div>'
        f'<div class="anc-callout anc-callout-{kind}">{body}</div>'
        "</div>"
    )


def _options_list_html(options: list[Option]) -> str:
    rows = []
    for verb, desc in options:
        rows.append(f'<div class="bf-choice"><strong>{verb}</strong> — {desc}</div>')
    return '<div class="bf-choices">' + "".join(rows) + "</div>"


def _snap_compact_html() -> str:
    return (
        '<div class="snap-compact">'
        '<span class="snap-chip"><span class="kw kw-snap">1–3</span> Fails</span>'
        '<span class="snap-dot">·</span>'
        '<span class="snap-chip"><span class="kw kw-snap">4–8</span> Choose 1</span>'
        '<span class="snap-dot">·</span>'
        '<span class="snap-chip"><span class="kw kw-snap">9+</span> Choose 2</span>'
        "</div>"
    )


def render_ancestry_snap(card: dict) -> str:
    timing = card["timing"]
    return (
        f'<div class="card bf-ancestry acc-ancestry">'
        f'<div class="hdr">'
        f'<div class="hdr-top">'
        f'<span class="cap cap-accent">Ancestry</span>'
        f'<span class="cap cap-neutral">{timing}</span>'
        f"</div>"
        f'<div class="hdr-name">{card["name"]}</div>'
        f"</div>"
        f'<div class="bf-body">'
        f'<div class="bf-flv">{card["flavor"]}</div>'
        f"{_trigger_callout_html(card)}"
        f"{_options_list_html(card['options'])}"
        f"{_snap_compact_html()}"
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
    by_key = {c["key"]: c for c in ANCESTRIES}
    batch: list[dict] = []
    for card in cards:
        key = card.get("Card_Key", "")
        if key not in by_key:
            continue
        spec = by_key[key]
        html = render_ancestry_snap(spec)
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
        f"// Source: build_ancestry_snap.py ({DATE})\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


PROOF_OUT = ROOT / "ancestry-snap-proof.html"


def write_proof_html() -> None:
    acts = [c for c in ANCESTRIES if c["timing"] == "Act"]
    reacts = [c for c in ANCESTRIES if c["timing"] == "React"]

    def section(title: str, cards: list[dict]) -> str:
        rows = []
        for c in cards:
            rows.append(
                f'<div class="sample"><div class="stag">{c["name"]}</div>'
                f'<div class="cardwrap">{render_ancestry_snap(c)}</div></div>'
            )
        return f'<section><h2>{title}</h2><div class="grid">{"".join(rows)}</div></section>'

    css = """\
:root{--snap:#6D28D9;--snap-l:#EDE9FE;--gold:#c8a96e;--gold-d:#7a6030;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:system-ui,-apple-system,sans-serif;background:#16110a;color:#f0e6cf;padding:24px 18px 60px;}
h1{font-size:18px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:6px;}
.sub{color:var(--gold-d);font-size:13px;margin-bottom:20px;line-height:1.55;max-width:920px;}
section{margin-bottom:44px;}h2{font-size:13px;letter-spacing:1.5px;text-transform:uppercase;color:var(--gold);margin-bottom:16px;padding-bottom:6px;border-bottom:1px solid #2a1d10;}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:28px;align-items:start;}
.sample{display:flex;flex-direction:column;gap:10px;}.stag{font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:var(--snap-l);text-align:center;}
.kw{display:inline-block;padding:0 5px;border-radius:3px;font-size:10px;font-weight:700;vertical-align:middle;line-height:1.6;font-family:system-ui,sans-serif;}
.kw-boost{background:#0F766E;color:#CCFBF1;}.kw-snap{background:var(--snap);color:var(--snap-l);font-size:9px;min-width:1.6em;text-align:center;}
.acc-ancestry{--a:#9a6a2e;--ad:#7e5726;--al:#ddccb8;--ah:#f5f0ea;}
.cardwrap{width:2.5in;margin:0 auto;}.cardwrap .card{box-shadow:5px 5px 0 rgba(0,0,0,.55);}
.card{position:relative;border-left:5px solid var(--a);display:flex;flex-direction:column;width:2.5in;min-height:3.5in;background:#f7f0e0;border:0.5px solid #c8a96e;color:#241a08;overflow:hidden;}
.hdr{padding:7px 9px 5px;background:var(--ah);border-bottom:1px solid rgba(0,0,0,.1);}
.hdr-top{display:flex;justify-content:space-between;align-items:center;min-height:16px;}
.cap{display:inline-flex;border:1.5px solid;border-radius:4px;padding:1px 7px;font-size:9px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;}
.cap-neutral{border-color:#3a3320;color:#3a3320;}.cap-accent{border-color:var(--ad);color:var(--ad);}
.hdr-name{font-family:'EB Garamond',Georgia,serif;font-weight:700;font-size:16.5px;text-align:center;padding:3px 12px;margin:6px -1px 2px;color:var(--ad);background:var(--al);border-top:2px solid var(--a);border-bottom:2px solid var(--a);clip-path:polygon(0 0,100% 0,calc(100% - 11px) 50%,100% 100%,0 100%,11px 50%);}
.bf-body{flex:1;padding:7px 9px 10px;display:flex;flex-direction:column;gap:5px;font-size:10.5px;line-height:1.42;}
.bf-flv{font-style:italic;color:#5a4020;font-size:10px;}.anc-trigger{display:flex;flex-direction:column;gap:2px;}
.anc-freq{font-size:7.5px;font-weight:700;letter-spacing:1.3px;text-transform:uppercase;color:#8a6a40;}
.anc-callout{font-style:normal;font-weight:600;font-size:10px;line-height:1.45;color:#1c1408;padding:5px 7px;border-left:3px solid var(--ad);background:rgba(0,0,0,.04);border-radius:0 4px 4px 0;}
.anc-callout-act{border-left-color:#1C3A5E;background:rgba(28,58,94,.07);}.anc-callout-react{border-left-color:#6D28D9;background:rgba(109,40,217,.08);}
.bf-choices{display:flex;flex-direction:column;gap:4px;}.bf-choice{font-size:10px;line-height:1.45;color:#1c1408;}
.snap-compact{margin-top:auto;padding-top:5px;display:flex;flex-wrap:wrap;align-items:center;gap:3px 5px;font-size:9px;color:#5a4520;border-top:0.5px solid rgba(200,169,110,.45);}
.snap-chip{display:inline-flex;align-items:center;gap:3px;white-space:nowrap;}.snap-dot{opacity:.45;}
"""
    html = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        "<link href=\"https://fonts.googleapis.com/css2?family=EB+Garamond:wght@600;700&display=swap\" rel=\"stylesheet\">"
        "<title>Instinct RPG — Ancestry Snap Check Proof</title>"
        f"<style>{css}</style></head><body>"
        "<h1>Ancestry Snap Check — Proof</h1>"
        "<p class=\"sub\">Trigger → three options → compact bands. "
        "<strong>1–3</strong> Fails · <strong>4–8</strong> Choose 1 · <strong>9+</strong> Choose 2.</p>"
        + section("React (3)", reacts)
        + section("Act (7)", acts)
        + "</body></html>"
    )
    PROOF_OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {PROOF_OUT.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    for spec in ANCESTRIES:
        html = render_ancestry_snap(spec)
        print(f"{spec['key']} ({spec['timing']}) — {len(html)} chars")

    if args.write or args.push:
        cards = load_cards()
        cards, batch = patch_card_data(cards)
        if len(batch) != len(ANCESTRIES):
            raise SystemExit(f"Expected {len(ANCESTRIES)} ancestry rows, got {len(batch)}")
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
