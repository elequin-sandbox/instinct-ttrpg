#!/usr/bin/env python3
"""Paladin ability + Bulwark rework: thematic utility + PbtA narrative glosses."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regenerate_card_data import effect_plain, flavor_plain, guess_class, guess_type  # noqa: E402
from scripts.strip_origin_stems import push_baserow  # noqa: E402

OUT = ROOT / "card-data.js"
PROOF_OUT = ROOT / "paladin-pool-proof.html"
BATCH_OUT = ROOT / "scripts" / "paladin_pool_batch.json"
REWORK_DATE = "2026-06-30"


def _r() -> str:
    return '<span class="kw kw-resolve">Resolve</span>'


def _b(n: int = 1) -> str:
    return f'<span class="kw kw-boost">Boost {n}</span>'


def _hd() -> str:
    return '<span class="kw kw-hd">Hit Die</span>'


def _c1() -> str:
    return '<span class="kw kw-crit">1</span>'


def _cloop() -> str:
    return '<span class="kw kw-crit">1↻</span>'


def _crit_block(*lines: str) -> str:
    rows = "".join(f'<div class="ci">{line}</div>' for line in lines)
    return f'<div class="csec"><div class="clbl">Crit</div><div class="crow">{rows}</div></div>'


def _ability(
    *,
    name: str,
    flavor: str,
    effect: str,
    subtype: str = "",
    crit: str = "",
) -> str:
    sub = f'<span class="cap cap-neutral">{subtype}</span>' if subtype else "<span></span>"
    crit_html = crit if crit else ""
    return (
        f'<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{sub}'
        f'</div><div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div><div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>{crit_html}</div>'
        f'<div class="idtag">Paladin</div><div class="tier-float"><span>t1</span></div></div>'
    )


def build_bulwark() -> str:
    r = _r()
    return (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        '<div class="hdr-name">Bulwark</div></div><div class="card-body">'
        '<div class="zone-label">Courageous Resolve</div>'
        f'<div class="effect-text">When rolling {r}, roll an additional die, then re-roll any {r} dice.</div>'
        '<div class="rule"></div>'
        '<div class="zone-label">Parry This</div>'
        '<div class="effect-text">During <strong>Contests</strong>, after you make a <strong>Defensive</strong> roll '
        f'but before it resolves, you may add any of your {r} dice with their current value.</div>'
        '</div><div class="idtag">Paladin</div></div>'
    )


CARDS: dict[str, dict] = {
    "bulwark-paladin-core": {"id": 622, "name": "Bulwark", "scope": "Core", "build": build_bulwark},
    "interpose-paladin": {
        "id": 368,
        "name": "Interpose",
        "build": lambda: _ability(
            name="Interpose",
            subtype="React",
            flavor="You put yourself between them.",
            effect=(
                "When an ally within reach would take a hit, perform a <strong>Faith</strong> check. "
                "On success, <strong>Move</strong> into the blow's path — you become the target. "
                "Narrate how your body turns the strike aside."
            ),
            crit=_crit_block(f"{_c1()} The ally gains {_b()} on their next <strong>Action</strong>."),
        ),
    },
    "rebuke-paladin": {
        "id": 379,
        "name": "Aura of Courage",
        "build": lambda: _ability(
            name="Aura of Courage",
            flavor="While in hand: fear finds no purchase here.",
            effect=(
                "While this card is in hand, your steadiness anchors everyone near you. "
                "Allies within reach who would lose their nerve stand firm instead — "
                "describe what courage looks like from where you stand."
            ),
            crit=_crit_block(f"{_c1()} Each steadied ally gains {_b()} on their next check."),
        ),
    },
    "aura-of-protection-paladin": {
        "id": 372,
        "name": "Aura of Protection",
        "build": lambda: _ability(
            name="Aura of Protection",
            flavor="While in hand: you are a wall between them and harm.",
            effect=(
                "While this card is in hand, allies at your side fight from behind your guard. "
                "When harm would reach them, narrate how you intercept — the GM honors reasonable deflections. "
                "You sense threats aimed at them before they land."
            ),
            crit=_crit_block(
                f"{_c1()} Allies beside you gain {_b()} on their next <strong>Defensive</strong> roll "
                "while you stand with them."
            ),
        ),
    },
    "beacon-paladin": {
        "id": 374,
        "name": "Beacon",
        "build": lambda: _ability(
            name="Beacon",
            subtype="Act",
            flavor="Not a miracle. A decision.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, restore one ally's composure — "
                f"they recover a spent {_hd()} at its current face value."
            ),
            crit=_crit_block(
                f"{_c1()} They also shed the weight they've been carrying — describe what lifts."
            ),
        ),
    },
    "charge-paladin": {
        "id": 381,
        "name": "Charge",
        "build": lambda: _ability(
            name="Charge",
            subtype="Act",
            flavor="It doesn't burn. It reveals.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, call divine fire down on a target — "
                f"they take {_b()} bonus fire damage. <strong>Exposed</strong> — the flames mark where the next blow will tell."
            ),
            crit=_crit_block(
                f"{_c1()} <strong>Rattled</strong> — they stagger blind, hands up against the light.",
                f"{_c1()} The fire spreads — add {_b()} to the damage.",
            ),
        ),
    },
    "sacred-ground-paladin": {
        "id": 378,
        "name": "Condemn",
        "build": lambda: _ability(
            name="Condemn",
            subtype="Act",
            flavor="You don't curse them. You recognize what they are.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, speak what they have done aloud — "
                "the truth lands. They must choose: <strong>Stand down</strong> — abandon their course, visibly shaken; "
                "or <strong>Press on</strong> — everyone present sees them clearly now."
            ),
            crit=_crit_block(
                f"{_c1()} <strong>Exposed</strong> — their guard drops; the next honest strike finds a gap.",
                f"{_c1()} All allies gain {_b()} on their next <strong>Strike</strong> against them.",
            ),
        ),
    },
    "divine-challenge-paladin": {
        "id": 373,
        "name": "Divine Challenge",
        "build": lambda: _ability(
            name="Divine Challenge",
            subtype="Act",
            flavor="Conviction lands harder than steel.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, <strong>Strike</strong> with divine force — "
                f"gain {_b()} on the damage roll. <strong>Exposed</strong> — your blow finds the fault in their defense."
            ),
            crit=_crit_block(
                f"{_c1()} <strong>Rattled</strong> — they reel; their allies see them humbled.",
                f"{_c1()} Gain {_b()} on the damage roll.",
            ),
        ),
    },
    "sentence-paladin": {
        "id": 375,
        "name": "Marked Wrath",
        "build": lambda: _ability(
            name="Marked Wrath",
            flavor="While in hand: someone still owes.",
            effect=(
                "While this card is in hand, name one who wronged the innocent. "
                f"When you <strong>Act</strong> against them, gain {_b()} — describe how your focus sharpens the moment. "
                "Allies who <strong>Strike</strong> them this beat share that focus."
            ),
            crit=_crit_block(
                f"{_c1()} <strong>Exposed</strong> — you have read their pattern; they cannot hide their next move.",
                f"{_c1()} All allies who <strong>Strike</strong> them this beat gain {_b()}.",
            ),
        ),
    },
    "shield-of-faith-paladin": {
        "id": 371,
        "name": "Shield of Faith",
        "build": lambda: _ability(
            name="Shield of Faith",
            subtype="Act",
            flavor="Belief, made solid.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, consecrate a ward over yourself and one ally — "
                "name what harm it turns aside. Each ward holds once before fading this <strong>Scene</strong>."
            ),
            crit=_crit_block(f"{_c1()} Consecrate a third ally also."),
        ),
    },
    "vow-of-enmity-paladin": {
        "id": 377,
        "name": "Divine Shield",
        "build": lambda: _ability(
            name="Divine Shield",
            subtype="React",
            flavor="Something steps in front of the blow.",
            effect=(
                "When you or an ally takes damage, perform a <strong>Faith</strong> check. "
                "On success, divine force interposes — the blow glances off. "
                f"Remove the weakest {_hd()} from the hit."
            ),
            crit=_crit_block(
                f"{_c1()} <strong>Rattled</strong> — the attacker flinches; their next swing comes wide."
            ),
        ),
    },
    "ward-paladin": {
        "id": 376,
        "name": "Ward",
        "build": lambda: _ability(
            name="Ward",
            subtype="React",
            flavor="You placed yourself here for exactly this reason.",
            effect=(
                "When harm would reach an ally you have chosen to protect, perform a <strong>Faith</strong> check. "
                "On success, the ward flares — they are untouched, or you <strong>Move</strong> to take it instead."
            ),
            crit=_crit_block(
                f"{_c1()} The threat's scope narrows for the whole <strong>Scene</strong>."
            ),
        ),
    },
    "hand-of-mercy-paladin": {
        "id": 380,
        "name": "Hand of Mercy",
        "build": lambda: _ability(
            name="Hand of Mercy",
            subtype="Act",
            flavor="You reach into the wound and pull something back.",
            effect=(
                "Perform a <strong>Medicine</strong> check. On success, an ally recovers 1 "
                f"{_hd()} — choose the die and set it to its maximum face value."
            ),
            crit=_crit_block(f"{_c1()} Recover 2 {_hd()} instead."),
        ),
    },
    "lay-on-hands-paladin": {
        "id": 369,
        "name": "Lay on Hands",
        "build": lambda: _ability(
            name="Lay on Hands",
            subtype="Act",
            flavor="Not this one. Not today.",
            effect=(
                "Perform a <strong>Medicine</strong> check. On success, touch an ally — "
                f"they shake off the worst thing pressing on them and recover a lost {_hd()}."
            ),
            crit=_crit_block(f"{_c1()} They recover one additional lost {_hd()}."),
        ),
    },
    "smite-paladin": {
        "id": 370,
        "name": "Smite",
        "build": lambda: _ability(
            name="Smite",
            subtype="Act",
            flavor="You make yourself the problem they can't ignore.",
            effect=(
                "Perform a <strong>Presence</strong> check. On success, draw an enemy's focus entirely to you. "
                "<strong>Rattled</strong> — they cannot look away; they must answer your challenge before acting on anyone else."
            ),
            crit=_crit_block(
                f"{_cloop()} <strong>Rattled</strong> — another enemy who heard you falters, fixing on you instead."
            ),
        ),
    },
}


def card_obj(key: str, spec: dict, html: str) -> dict:
    card_type = guess_type(html)
    scope = spec.get("scope") or ("Core" if card_type == "Core" else "ability")
    return {
        "id": spec["id"],
        "Name": spec["name"],
        "Card_Key": key,
        "Class": guess_class(html) or "paladin",
        "Card_Type": card_type,
        "Scope": scope,
        "Ruleset": "base",
        "Status": "current",
        "Last_Rework_Date": REWORK_DATE,
        "HTML": html,
        "FlavorText_Plain": flavor_plain(html),
        "EffectText_Plain": effect_plain(html),
    }


def write_proof(cards: list[dict], keys: list[str]) -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_key = {c["Card_Key"]: c for c in cards}
    chunks = []
    for key in keys:
        c = by_key[key]
        chunks.append(
            f'<div class="sample"><div class="stag">{c["Name"]}</div>'
            f'<div class="cardwrap scope-ability cls-paladin">{c["HTML"]}</div></div>'
        )
    PROOF_OUT.write_text(
        f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>Paladin pool proof</title><style>{css}"
        "body{{background:#0f1419;padding:24px;color:#e8eef5;font-family:system-ui,sans-serif;}}"
        ".grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}}"
        ".stag{{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#c9b896;}}</style></head><body>"
        "<h1>Paladin pool — narrative crit audit</h1>"
        f'<div class="grid">{"".join(chunks)}</div></body></html>',
        encoding="utf-8",
    )


def patch_card_data() -> tuple[list[dict], list[dict]]:
    text = OUT.read_text(encoding="utf-8")
    m = re.search(r"window\.CARD_DATA\s*=\s*", text)
    if not m:
        raise SystemExit("CARD_DATA assignment not found")
    cards = json.loads(text[m.end() :].strip().rstrip(";"))
    by_id = {c["id"]: c for c in cards}
    batch: list[dict] = []

    for key, spec in CARDS.items():
        html = spec["build"]()
        obj = card_obj(key, spec, html)
        by_id[obj["id"]] = obj
        batch.append(
            {
                "id": obj["id"],
                "HTML": html,
                "Name": obj["Name"],
                "Card_Key": key,
                "Last_Rework_Date": REWORK_DATE,
            }
        )

    cards = sorted(by_id.values(), key=lambda c: c["id"])
    today = date.today().isoformat()
    header = (
        f"// Generated by scripts/rework_paladin_cards.py — do not edit manually. Last updated: {today}\n"
        f"// Paladin thematic + PbtA narrative gloss pass\n"
    )
    OUT.write_text(header + "window.CARD_DATA = " + json.dumps(cards, separators=(",", ":")) + ";\n", encoding="utf-8")
    return cards, batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--push", action="store_true", help="Push to Baserow via API")
    args = parser.parse_args()
    cards, batch = patch_card_data()
    write_proof(cards, list(CARDS.keys()))
    BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Patched {len(batch)} Paladin cards in {OUT}")
    print(f"Wrote {PROOF_OUT.name}, {BATCH_OUT.name}")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']} → {item['Name']}")
    if args.push:
        push_baserow(batch)


if __name__ == "__main__":
    main()
