#!/usr/bin/env python3
"""Rogue deck audit — narrative-term glosses, PbtA choose-one, In the Shadows fix.

Usage:
  python3 scripts/build_rogue_pool.py --write
  python3 scripts/build_rogue_pool.py --push
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

BATCH_OUT = ROOT / "scripts" / "rogue_pool_batch.json"
PROOF_OUT = ROOT / "rogue-pool-proof.html"
DATE = "2026-06-30"

C1 = '<span class="kw kw-crit">1</span>'
B1 = '<span class="kw kw-boost">Boost 1</span>'


def _crit(*rows: str) -> str:
    body = "".join(f'<div class="ci">{r}</div>' for r in rows)
    return f'<div class="csec"><div class="clbl">Crit</div><div class="crow">{body}</div></div>'


def _choose(*rows: str) -> str:
    body = "".join(f'<div class="qi">{r}</div>' for r in rows)
    return '<div class="co">Choose one:</div><div class="ql">' + body + "</div>"


def _ability(
    name: str,
    flavor: str,
    effect: str,
    crit: str = "",
    *,
    act: bool = False,
    react: bool = False,
    extra_body: str = "",
) -> str:
    badges = '<span class="cap cap-neutral">Ability</span>'
    if act:
        badges += '<span class="cap cap-neutral">Act</span>'
    elif react:
        badges += '<span class="cap cap-neutral">React</span>'
    return (
        '<div class="card acc-rogue">'
        f'<div class="hdr"><div class="hdr-top">{badges}</div>'
        f'<div class="hdr-name">{name}</div></div>'
        '<div class="cbody">'
        f'<div class="flv">{flavor}</div><div class="hr"></div>'
        '<div class="elbl">Effect</div>'
        f'<div class="etxt">{effect}</div>'
        f"{extra_body}{crit}"
        "</div>"
        '<div class="idtag">Rogue</div>'
        '<div class="tier-float"><span>t1</span></div></div>'
    )


def strip_plain(html: str) -> str:
    t = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", t).strip()


CARDS: list[dict] = [
    {
        "id": 308,
        "key": "case-the-scene-rogue",
        "name": "Case the Scene",
        "card_type": "Act",
        "build": lambda: _ability(
            "Case the Scene",
            "You spend thirty seconds doing what others spend an hour missing.",
            "Perform an <strong>Investigation</strong> check. On success, name one escape route, "
            "one hidden object, or one person in this <strong>Scene</strong> the GM has not yet "
            "mentioned — it exists.",
            _crit(f"{C1} Name a second true thing."),
            act=True,
        ),
    },
    {
        "id": 301,
        "key": "cheap-shot-rogue",
        "name": "Cheap Shot",
        "card_type": "Act",
        "build": lambda: _ability(
            "Cheap Shot",
            "Fair fights are for people with something to prove.",
            "Perform an <strong>Acrobatics</strong> check. On success, <strong>Strike</strong> a target "
            "from an unexpected angle — they are <strong>Rattled</strong>, caught wrong-footed by the "
            "cheap hit.",
            _crit(
                f"{C1} <strong>Exposed</strong> — the dirty angle leaves a clear opening for the next blow."
            ),
            act=True,
        ),
    },
    {
        "id": 309,
        "key": "cunning-strike-rogue",
        "name": "Cunning Strike",
        "card_type": "Act",
        "build": lambda: _ability(
            "Cunning Strike",
            "The injury is secondary. The message is the point.",
            "Perform a <strong>Sleight of Hand</strong> check. On success, <strong>Strike</strong> a "
            "target and:",
            _crit(f"{C1} <strong>Strike</strong> for damage and apply the narrative you chose."),
            act=True,
            extra_body=_choose(
                "<strong>Hurt</strong> them — deal damage.",
                "<strong>Rattle</strong> them — they flinch and fight sloppy this beat.",
                "<strong>Expose</strong> a weakness — a flaw showing; allies know where to strike.",
                "<strong>Root</strong> them — a twist or pin; they can't reposition cleanly until "
                "they shake it off.",
            ),
        ),
    },
    {
        "id": 303,
        "key": "distract-rogue",
        "name": "Distract",
        "card_type": "Act",
        "build": lambda: _ability(
            "Distract",
            "Their attention is a resource. You just spent it.",
            "Perform a <strong>Deception</strong> check. On success, a target's attention is fully on "
            f"you — all other creatures in the <strong>Scene</strong> gain {B1} on their next "
            "<strong>Action</strong> this beat.",
            _crit(
                f"{C1} <strong>Rattled</strong> — they're fixated on you and can't track the rest "
                "of the room."
            ),
            act=True,
        ),
    },
    {
        "id": 304,
        "key": "exploit-opening-rogue",
        "name": "Exploit Opening",
        "card_type": "React",
        "build": lambda: _ability(
            "Exploit Opening",
            "You were waiting for exactly that.",
            "When an ally's <strong>Action</strong> leaves a target off-balance, perform an "
            "<strong>Acrobatics</strong> check. On success, <strong>Strike</strong> that target "
            "immediately.",
            _crit(
                f"{C1} <strong>Exposed</strong> — you land on the gap they opened.",
                f"{C1} <strong>Rooted</strong> — you pin them before they recover their footing.",
            ),
            react=True,
        ),
    },
    {
        "id": 299,
        "key": "find-the-gap-rogue",
        "name": "Find the Gap",
        "card_type": "Act",
        "build": lambda: _ability(
            "Find the Gap",
            "Every lock has a mechanism.",
            "Perform an <strong>Investigation</strong> check. On success:",
            _crit(f"{C1} Ask one additional question."),
            act=True,
            extra_body=_choose(
                "<strong>Name</strong> the fastest way through this obstacle.",
                "<strong>Spot</strong> what is being deliberately kept from view here.",
                "<strong>Identify</strong> who here cannot afford to have you proceed.",
            ),
        ),
    },
    {
        "id": 307,
        "key": "in-the-shadows-rogue",
        "name": "In the Shadows",
        "card_type": "",
        "build": lambda: _ability(
            "In the Shadows",
            "While in hand: you are unseen.",
            "While this card is in hand, you remain <strong>Hidden</strong> between turns — unseen "
            f"until you <strong>Act</strong> or draw attention. Any <strong>Strike</strong> from this "
            f"state gains {B1}.",
            _crit(
                f"{C1} Remain <strong>Hidden</strong> after striking — you don't break cover when "
                "the blow lands."
            ),
        ),
    },
    {
        "id": 306,
        "key": "read-the-mark-rogue",
        "name": "Read the Mark",
        "card_type": "Act",
        "build": lambda: _ability(
            "Read the Mark",
            "You size up a target before they know you're looking.",
            "Perform a <strong>Perception</strong> check. On success:",
            _crit(f"{C1} Ask one additional question."),
            act=True,
            extra_body=_choose(
                "<strong>Name</strong> what this person is trying to hide right now.",
                "<strong>Name</strong> what would make them flinch.",
                "<strong>Point out</strong> where they are most exposed.",
            ),
        ),
    },
    {
        "id": 302,
        "key": "shadowstep-rogue",
        "name": "Shadowstep",
        "card_type": "Act",
        "build": lambda: _ability(
            "Shadowstep",
            "Distance is a suggestion.",
            "Perform a <strong>Stealth</strong> check. On success, <strong>Move</strong> instantly to "
            "any unoccupied position in the <strong>Scene</strong> — you arrive "
            "<strong>Hidden</strong>, unseen in the new spot.",
            _crit(f"{C1} <strong>Strike</strong> immediately on arrival."),
            act=True,
        ),
    },
    {
        "id": 305,
        "key": "slip-away-rogue",
        "name": "Slip Away",
        "card_type": "React",
        "build": lambda: _ability(
            "Slip Away",
            "You were already leaving.",
            "When targeted by an attack or hostile <strong>Action</strong>, perform an "
            "<strong>Acrobatics</strong> check. On success, the <strong>Action</strong> misses — "
            "<strong>Move</strong> to an adjacent position.",
            _crit(
                f"{C1} <strong>Exposed</strong> — your dodge left them overextended on the swing."
            ),
            react=True,
        ),
    },
    {
        "id": 310,
        "key": "smoke-and-mirrors-rogue",
        "name": "Smoke and Mirrors",
        "card_type": "Act",
        "build": lambda: _ability(
            "Smoke and Mirrors",
            "Let them argue about what they saw.",
            "Perform a <strong>Deception</strong> check. On success, create a false impression — a "
            "sound, a silhouette, a dropped object. Every enemy in the <strong>Scene</strong> is "
            "<strong>Rattled</strong>, wrong-footed by what they think they saw, until one spends an "
            "<strong>Action</strong> investigating.",
            _crit(f"{C1} Two enemies investigate, not one."),
            act=True,
        ),
    },
    {
        "id": 300,
        "key": "sneak-attack-rogue",
        "name": "Sneak Attack",
        "card_type": "Act",
        "build": lambda: _ability(
            "Sneak Attack",
            "You weren't watching the right shadow.",
            "Perform a <strong>Stealth</strong> check. On success, <strong>Strike</strong> a target "
            "that is unaware of you or occupied with an ally.",
            _crit(
                f"{C1} <strong>Exposed</strong> — the blow caught them unaware; allies find the gap.",
                f"{C1} <strong>Hidden</strong> — slip back into cover nearby.",
            ),
            act=True,
        ),
    },
    {
        "id": 298,
        "key": "vanish-rogue",
        "name": "Vanish",
        "card_type": "React",
        "build": lambda: _ability(
            "Vanish",
            "You were never quite where they thought.",
            "When an enemy declares an attack against you, play this card. The attack lands on nothing. "
            "Enter <strong>Hidden</strong> — you melt out of the line of attack — and "
            "<strong>Move</strong> to any unoccupied position within reach.",
            _crit(
                f"{C1} <strong>Exposed</strong> — they swung at empty air; the GM has an honest "
                "opening on them.",
                f"{C1} Gain 1 <strong>Notoriety</strong>.",
            ),
            react=True,
        ),
    },
    {
        "id": 311,
        "key": "vanishing-strike-rogue",
        "name": "Vanishing Strike",
        "card_type": "Act",
        "build": lambda: _ability(
            "Vanishing Strike",
            "One moment, a blade. The next, nothing.",
            "Perform a <strong>Stealth</strong> check. On success, <strong>Strike</strong> from "
            "<strong>Hidden</strong> — then immediately re-enter <strong>Hidden</strong> in a new "
            "position.",
            _crit(
                f"{C1} <strong>Exposed</strong> — you mark the wound before you vanish; allies see "
                "where to follow up."
            ),
            act=True,
        ),
    },
]


def patch_cards(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c.get("Card_Key"): c for c in cards}
    batch: list[dict] = []

    for spec in CARDS:
        html = spec["build"]()
        card = by_key[spec["key"]]
        plain = f"> {strip_plain(html)}"
        card["HTML"] = html
        card["EffectText_Plain"] = plain
        card["Last_Rework_Date"] = DATE
        if spec["card_type"]:
            card["Card_Type"] = spec["card_type"]
        else:
            card["Card_Type"] = ""
        batch.append(
            {
                "id": spec["id"],
                "Name": spec["name"],
                "Card_Key": spec["key"],
                "HTML": html,
                "EffectText_Plain": plain,
                "Last_Rework_Date": DATE,
                **({"Card_Type": spec["card_type"]} if spec["card_type"] else {"Card_Type": ""}),
            }
        )

    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Generated by scripts/build_rogue_pool.py — do not edit manually. "
        f"Last updated: {DATE}\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def write_proof(cards: list[dict], keys: list[str]) -> None:
    css = open(ROOT / "primer-card-scope.css").read()
    chunks = []
    for key in keys:
        c = next(x for x in cards if x["Card_Key"] == key)
        chunks.append(
            f'<div class="sample"><div class="stag">{c["Name"]}</div>'
            f'<div class="cardwrap scope-ability cls-rogue">{c["HTML"]}</div></div>'
        )
    PROOF_OUT.write_text(
        f"<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>Rogue pool proof</title><style>{css}"
        "body{{background:#16110a;padding:24px;color:#f0e6cf;font-family:system-ui,sans-serif;}}"
        ".grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;}}"
        ".stag{{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#e7d6ac;}}</style></head><body>"
        "<h1>Rogue pool — narrative crit audit</h1>"
        f'<div class="grid">{"".join(chunks)}</div></body></html>',
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--push", action="store_true")
    args = parser.parse_args()

    cards = load_cards()
    cards, batch = patch_cards(cards)
    proof_keys = [s["key"] for s in CARDS]

    print(f"Patched {len(batch)} Rogue ability cards")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']}")

    if args.write or args.push:
        write_card_data(cards)
        write_proof(cards, proof_keys)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name}, {PROOF_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run — pass --write or --push")


if __name__ == "__main__":
    main()
