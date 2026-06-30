#!/usr/bin/env python3
"""Paladin Bulwark + thematic ability rework — patch card-data.js and push Baserow."""
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
REWORK_DATE = "2026-06-30"


def _kw_resolve() -> str:
    return '<span class="kw kw-resolve">Resolve</span>'


def _kw_boost(n: int = 1) -> str:
    return f'<span class="kw kw-boost">Boost {n}</span>'


def _kw_crit(n: int = 1) -> str:
    return f'<span class="kw kw-crit">{n}</span>'


def _kw_hd() -> str:
    return '<span class="kw kw-hd">Hit Die</span>'


def _ability_card(
    *,
    name: str,
    subtype: str = "",
    flavor: str,
    effect: str,
    crit: str | None = None,
) -> str:
    sub_cap = f'<span class="cap cap-neutral">{subtype}</span>' if subtype else "<span></span>"
    crit_block = ""
    if crit:
        crit_block = (
            f'<div class="csec"><div class="clbl">Crit</div>'
            f'<div class="crow"><div class="ci">{crit}</div></div></div>'
        )
    return (
        f'<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        f'<span class="cap cap-neutral">Ability</span>{sub_cap}'
        f'</div><div class="hdr-name">{name}</div></div><div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div><div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>{crit_block}</div>'
        f'<div class="idtag">Paladin</div><div class="tier-float"><span>t1</span></div></div>'
    )


def build_bulwark() -> str:
    r = _kw_resolve()
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
    "bulwark-paladin-core": {
        "id": 622,
        "name": "Bulwark",
        "build": build_bulwark,
        "scope": "Core",
    },
    "interpose-paladin": {
        "id": 368,
        "name": "Interpose",
        "build": lambda: _ability_card(
            name="Interpose",
            subtype="React",
            flavor="You put yourself between them.",
            effect=(
                "When an ally within reach would take a hit, perform a <strong>Faith</strong> check. "
                "On success, <strong>Move</strong> into the blow's path — you become the target. "
                "Narrate how your body turns the strike aside."
            ),
            crit=f"{_kw_crit()} The ally gains {_kw_boost()} on their next <strong>Action</strong>.",
        ),
    },
    "rebuke-paladin": {
        "id": 379,
        "name": "Aura of Courage",
        "build": lambda: _ability_card(
            name="Aura of Courage",
            flavor="While in hand: fear finds no purchase here.",
            effect=(
                "While this card is in hand, your steadiness anchors everyone near you. "
                "Allies within reach who would be <strong>Rattled</strong> stand firm instead — "
                "describe what courage looks like from where you stand."
            ),
            crit=f"{_kw_crit()} Each steadied ally gains {_kw_boost()} on their next check.",
        ),
    },
    "sacred-ground-paladin": {
        "id": 378,
        "name": "Condemn",
        "build": lambda: _ability_card(
            name="Condemn",
            subtype="Act",
            flavor="You don't curse them. You recognize what they are.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, speak what they have done aloud — "
                "the truth lands. They must choose: stand down, or continue with <strong>Rattled</strong>."
            ),
            crit=(
                f"{_kw_crit()} All allies gain {_kw_boost()} on their next <strong>Strike</strong> "
                "against this target."
            ),
        ),
    },
    "sentence-paladin": {
        "id": 375,
        "name": "Marked Wrath",
        "build": lambda: _ability_card(
            name="Marked Wrath",
            flavor="While in hand: someone still owes.",
            effect=(
                "While this card is in hand, name one who wronged the innocent. "
                f"When you <strong>Act</strong> against them, gain {_kw_boost()} — "
                "describe how your focus sharpens the moment. "
                f"Allies who <strong>Strike</strong> them this beat share that focus."
            ),
            crit=f"{_kw_crit()} The target is <strong>Exposed</strong> to all attacks this beat.",
        ),
    },
    "aura-of-protection-paladin": {
        "id": 372,
        "name": "Aura of Protection",
        "build": lambda: _ability_card(
            name="Aura of Protection",
            flavor="While in hand: you are a wall between them and harm.",
            effect=(
                "While this card is in hand, allies at your side fight from behind your guard. "
                "When harm would reach them, narrate how you intercept — the GM honors reasonable deflections. "
                "You sense threats aimed at them before they land."
            ),
            crit=(
                f"{_kw_crit()} Allies beside you gain {_kw_boost()} on their next "
                "<strong>Defensive</strong> roll while you stand with them."
            ),
        ),
    },
    "shield-of-faith-paladin": {
        "id": 371,
        "name": "Shield of Faith",
        "build": lambda: _ability_card(
            name="Shield of Faith",
            subtype="Act",
            flavor="Belief, made solid.",
            effect=(
                "Perform a <strong>Faith</strong> check. On success, consecrate a ward over yourself and one ally — "
                "name what harm it turns aside. Each ward holds once before fading this <strong>Scene</strong>."
            ),
            crit=f"{_kw_crit()} Consecrate a third ally also.",
        ),
    },
    "vow-of-enmity-paladin": {
        "id": 377,
        "name": "Divine Shield",
        "build": lambda: _ability_card(
            name="Divine Shield",
            subtype="React",
            flavor="Something steps in front of the blow.",
            effect=(
                "When you or an ally takes damage, perform a <strong>Faith</strong> check. "
                "On success, divine force interposes — the blow glances off. "
                f"Remove the weakest {_kw_hd()} from the hit."
            ),
            crit=f"{_kw_crit()} The attacker is <strong>Rattled</strong>.",
        ),
    },
    "ward-paladin": {
        "id": 376,
        "name": "Ward",
        "build": lambda: _ability_card(
            name="Ward",
            subtype="React",
            flavor="You placed yourself here for exactly this reason.",
            effect=(
                "When harm would reach an ally you have chosen to protect, perform a <strong>Faith</strong> check. "
                "On success, the ward flares — they are untouched, or you <strong>Move</strong> to take it instead."
            ),
            crit=f"{_kw_crit()} The threat's scope narrows for the whole <strong>Scene</strong>.",
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
        "Class": guess_class(html),
        "Card_Type": card_type,
        "Scope": scope,
        "Ruleset": "base",
        "Status": "current",
        "Last_Rework_Date": REWORK_DATE,
        "HTML": html,
        "FlavorText_Plain": flavor_plain(html),
        "EffectText_Plain": effect_plain(html),
    }


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
                "Card_Type": obj["Card_Type"],
                "Last_Rework_Date": REWORK_DATE,
                "FlavorText_Plain": obj["FlavorText_Plain"],
                "EffectText_Plain": obj["EffectText_Plain"],
            }
        )

    cards = sorted(by_id.values(), key=lambda c: c["id"])
    today = date.today().isoformat()
    header = (
        f"// Generated by scripts/rework_paladin_thematic.py — do not edit manually. Last updated: {today}\n"
        f"// Paladin Bulwark + thematic ability rework\n"
        f"// Full regen: py -3 scripts/regenerate_card_data.py\n"
    )
    OUT.write_text(header + "window.CARD_DATA = " + json.dumps(cards, separators=(",", ":")) + ";\n", encoding="utf-8")
    return cards, batch


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--push", action="store_true", help="Push updated rows to Baserow")
    args = parser.parse_args()

    cards, batch = patch_card_data()
    print(f"Patched {OUT} — updated {len(batch)} Paladin cards")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']} → {item['Name']}")

    if args.push:
        push_baserow(batch)


if __name__ == "__main__":
    main()
