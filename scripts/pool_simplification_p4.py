#!/usr/bin/env python3
"""Playtest 4 — Phase 2C pool simplification pass.

Audits + rewrites active-pool (Act/React/Core) cards that still carry legacy
unit-linked condition language (duration tracking, stacked conditions, GM-
improvised effects) or retired mechanics (Item Check / placed dice / Disguised).
Model: pared Smite (Paladin) / Strike (Barbarian) — one clear effect, glossed
narrative terms, no lingering per-unit state for the GM to track.

Usage:
  python3 scripts/pool_simplification_p4.py              # dry-run summary
  python3 scripts/pool_simplification_p4.py --write       # patch card-data.js + batch JSON + proof
  python3 scripts/pool_simplification_p4.py --push        # write + push to Baserow
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.regenerate_card_data import effect_plain, flavor_plain  # noqa: E402
from scripts.strip_origin_stems import push_baserow  # noqa: E402

CARD_DATA = ROOT / "card-data.js"
PROOF_OUT = ROOT / "pool-simplification-p4-proof.html"
BATCH_OUT = ROOT / "scripts" / "pool_simplification_p4_batch.json"
REWORK_DATE = "2026-07-01"

# Each entry: Card_Key -> list of (old_substring, new_substring) applied verbatim
# to that card's current HTML. Every old_substring must match exactly once.
REPLACEMENTS: dict[str, list[tuple[str, str]]] = {
    # ---------------------------------------------------------------- ITEMS
    "smoke-bomb-item": [
        (
            "Fill a 10-foot area with smoke. All creatures within are <strong>Hidden</strong> from each other until the smoke clears or the <strong>Scene</strong> ends.",
            "Fill a 10-foot area with smoke. Anyone inside is <strong>Hidden</strong> from anyone outside it, and you and your allies inside may <strong>Move</strong> freely this beat without being intercepted.",
        ),
    ],
    "weighted-net-item": [
        (
            'Perform an <strong>Item Check</strong> — place the dice as <strong>Rooted</strong> on the target. Until <strong>Cleared</strong>, they cannot move from their position.',
            "Throw to entangle a target within reach — <strong>Rooted</strong>, netted at the ankles.",
        ),
    ],
    "blinding-flash-powder-item": [
        (
            'Perform an <strong>Item Check</strong> — place the dice as <strong>Exposed</strong> on the attacker. Until <strong>Cleared</strong>, they are <strong>Exposed</strong>.',
            "Throw the powder into their eyes — <strong>Exposed</strong>, they're blinking through spots and swinging blind.",
        ),
    ],
    "vial-of-acid-item": [
        (
            'Dissolve any non-magical lock, bar, or thin barrier. — or — Perform an <strong>Item Check</strong> — place the dice as <strong>Exposed</strong> on a target.',
            "Dissolve any non-magical lock, bar, or thin barrier. — or — Splash a target within reach: <strong>Exposed</strong>, the acid finds every gap in their guard.",
        ),
    ],
    "disguise-kit-item": [
        (
            'Perform an <strong>Item Check</strong> — place the dice as <strong>Disguised</strong> on yourself. You appear as a type of NPC the GM approves. Until <strong>Cleared</strong>, you are <strong>Disguised</strong>.',
            "Spend a few minutes transforming your face and dress — you pass as a type of NPC the GM approves, until something breaks the act.",
        ),
    ],
    "oil-flask-item": [
        (
            "Coat a 10-foot area of ground. Any creature moving through must succeed on a check or become <strong>Exposed 1</strong>. If lit, any creature that acts within it takes a consequence.",
            "Coat a 10-foot area of ground. Any creature moving through must succeed on a check or lose their footing — <strong>Exposed</strong>. If lit, anyone who acts within it takes 1 damage.",
        ),
    ],
    "caltrops-item": [
        (
            "Scatter in a 10-foot area. Any creature moving through becomes <strong>Rooted 1</strong> and cannot continue moving that <strong>Action</strong>.",
            "Scatter across a 10-foot area. Any creature moving through is <strong>Rooted</strong> — spikes catch mid-stride, and that <strong>Action</strong> ends right there.",
        ),
    ],
    # -------------------------------------------------------------- WARLOCK
    "eldritch-strike-warlock": [
        (
            "add that die to your strike. On success, the target is <strong>Exposed</strong>.",
            "add that die to your strike. On success, they're <strong>Exposed</strong> — the dark magic marks exactly where to hit next.",
        ),
        (
            "Target loses their next defensive <strong>Action</strong>.",
            "An ally gains <span class=\"kw kw-boost\">Boost 1</span> on their next <strong>Strike</strong> against this target.",
        ),
    ],
    "dark-grasp-warlock": [
        (
            "they are <strong>Rooted</strong>. The grip holds until they break it.",
            "they're <strong>Rooted</strong> — your will made physical around them.",
        ),
        (
            "They are also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the grip is colder than they expected.",
        ),
    ],
    "terrify-warlock": [
        (
            "all enemies who witness it are <strong>Rattled</strong>.",
            "all enemies who witness it are <strong>Rattled</strong> — your patron's shadow falls fully across the room.",
        ),
        (
            "One target flees entirely.",
            "One target's nerve breaks — they flee the <strong>Scene</strong> entirely.",
        ),
    ],
    "misdirection-warlock": [
        (
            "Redirected target is also <strong>Exposed</strong>.",
            "<strong>Exposed</strong> — they don't see it coming from this angle.",
        ),
    ],
    "shadow-step-warlock": [
        (
            "Arrive <strong>Hidden</strong>.",
            "Arrive <strong>Hidden</strong> — the shadows close behind you.",
        ),
    ],
    "whisper-of-ruin-warlock": [
        (
            "They must immediately choose: stand down, or continue with <strong>Rattled</strong>.",
            "They must choose: <strong>Stand down</strong> — abandon it now, or <strong>Press on</strong> — walk into it <strong>Rattled</strong>, nerve fraying.",
        ),
        (
            "If they continue, they are also <strong>Exposed</strong>.",
            "<strong>Exposed</strong> — if they press on, their focus is already gone.",
        ),
    ],
    # -------------------------------------------------------------- FIGHTER
    "disarm-fighter": [
        (
            "they are <strong>Exposed</strong> until they retrieve or replace it.",
            "they're <strong>Exposed</strong> — hands empty when it matters most.",
        ),
    ],
    "covering-fire-fighter": [
        (
            "Targets are also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the near-misses shake their aim.",
        ),
    ],
    "feint-fighter": [
        (
            "they are <strong>Exposed</strong> and your next",
            "they're <strong>Exposed</strong> — they defended the wrong line — and your next",
        ),
    ],
    "grapple-fighter": [
        (
            "they are <strong>Rooted</strong> and cannot act freely. You control their position until they break the hold.",
            "they're <strong>Rooted</strong> — your grip is the only thing holding them there.",
        ),
        (
            "They are also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the fight goes out of them for a moment.",
        ),
    ],
    "overrun-fighter": [
        (
            "every enemy you pass through is knocked aside and <strong>Rattled</strong>.",
            "every enemy you pass through is knocked aside — <strong>Rattled</strong>, they didn't see the wall of you coming.",
        ),
        (
            "One enemy is also <strong>Rooted</strong> where you left them.",
            "<strong>Rooted</strong> — one of them goes down and stays down.",
        ),
    ],
    "size-up-fighter": [
        (
            "drive your shield into a target — they are <strong>Rattled</strong> and <strong>Rooted</strong> where they stand.",
            "drive your shield into a target — <strong>Rattled</strong>, the impact rings through their skull.",
        ),
        (
            "They are also knocked back one position.",
            "<strong>Rooted</strong> — they buckle and stay down where they land.",
        ),
    ],
    # ---------------------------------------------------------------- DRUID
    "root-hold-druid": [
        (
            "a target is <strong>Rooted</strong> in place.",
            "a target is <strong>Rooted</strong> — the ground itself refuses to let go.",
        ),
        (
            "A second target is also <strong>Rooted</strong>.",
            "<strong>Rooted</strong> — a second target as the roots spread.",
        ),
    ],
    "entangle-druid": [
        (
            "all are <strong>Rooted</strong> until they break free.",
            "all are <strong>Rooted</strong> — the ground itself joins the fight.",
        ),
        (
            "Breaking free costs them their next <strong>Action</strong>.",
            "An ally gains <span class=\"kw kw-boost\">Boost 1</span> against every <strong>Rooted</strong> enemy this beat.",
        ),
    ],
    "thornwall-druid": [
        (
            "the enemy is <strong>Rooted</strong> and takes the consequences of moving into sharp terrain.",
            "the enemy is <strong>Rooted</strong> — the thorns draw blood on the way in.",
        ),
        (
            "All enemies who witness hesitate — <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — nearby enemies flinch back from the terrain itself.",
        ),
    ],
    "camouflage-druid": [
        (
            "you and up to two allies are <strong>Hidden</strong> as long as you remain still — the environment absorbs you.",
            "you and up to two allies become <strong>Hidden</strong>, folded into the terrain around you.",
        ),
        (
            "Hidden persists even through slow movement.",
            "<strong>Hidden</strong> holds even as you move — slow and unseen.",
        ),
    ],
    # ------------------------------------------------- CLERIC / RANGER / WIZARD
    "word-of-comfort-cleric": [
        (
            "the target is <strong>Rattled</strong> and <strong>Exposed</strong> until they recover their composure.",
            "they're <strong>Rattled</strong> — their composure cracks in front of everyone.",
        ),
        (
            "The condition spreads to one nearby witness.",
            "<strong>Exposed</strong> — the crack widens; a witness sees exactly where to press.",
        ),
    ],
    "weal-cleric": [
        (
            "all enemies in it are <strong>Rooted</strong> and must spend an <strong>Action</strong> to break free.",
            "all enemies in it are <strong>Rooted</strong> — the ground itself turns against them.",
        ),
        (
            "They are also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the mire has a will, and it's watching.",
        ),
    ],
    "mark-prey-ranger": [
        (
            "<strong>Move</strong> to any unoccupied dark space in the <strong>Scene</strong> and become <strong>Hidden</strong> until you act.",
            "<strong>Move</strong> to any unoccupied dark space in the <strong>Scene</strong>, <strong>Hidden</strong> in the dark you just became part of.",
        ),
    ],
    "called-shot-ranger": [
        (
            "The GM applies a matching condition: hands drop things, legs become <strong>Rooted</strong>, voice is silenced.",
            "Call the location before you fire. Legs: <strong>Rooted</strong>. Hands: <strong>Exposed</strong>, their weapon almost drops.",
        ),
        (
            "Condition lasts the full <strong>Scene</strong>.",
            "An ally gains <span class=\"kw kw-boost\">Boost 1</span> on their next <strong>Strike</strong> against this target.",
        ),
    ],
    "set-trap-ranger": [
        (
            "When triggered, target is <strong>Rooted</strong> and <strong>Exposed</strong>.",
            "When triggered, the target is <strong>Rooted</strong> — caught exactly where you planned it.",
        ),
    ],
    "volley-ranger": [
        (
            "One target is also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — one target's ears are still ringing.",
        ),
    ],
    "read-the-land-ranger": [
        (
            "They are also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the cold bites deeper than the damage.",
        ),
    ],
    "ambush-ranger": [
        (
            "you gain <span class=\"kw kw-boost\">Boost 1</span> on every <strong>Action</strong> against them until they are removed from the <strong>Scene</strong>. The mark transfers to a new target when they fall.",
            "you gain <span class=\"kw kw-boost\">Boost 1</span> on every <strong>Action</strong> against them this <strong>Scene</strong>.",
        ),
        (
            "Target is also <strong>Exposed</strong>.",
            "<strong>Exposed</strong> — you've read exactly where they're weakest.",
        ),
    ],
    "survival-instinct-ranger": [
        (
            "they are <strong>Rooted</strong> until they break free with an <strong>Action</strong>.",
            "they're <strong>Rooted</strong> — nailed where they stand.",
        ),
    ],
    "suppressing-fire-ranger": [
        (
            "The attacker is also <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — the deflection singes them on the way past.",
        ),
    ],
    "discipline-ranger": [
        (
            "The caster is <strong>Rattled</strong>.",
            "<strong>Rattled</strong> — their own magic backlashes against them.",
        ),
    ],
}

# Cards reviewed and judged already compliant (no tracked condition, has gloss,
# or bounded/immediate effect) — logged for the audit table, not rewritten.
CLEAN_NO_CHANGE = [
    "press-the-advantage-fighter",
    "living-ground-druid",
    "ghost-step-ranger",
]

# Rows with Name/Card_Key/Class drift vs. the HTML actually stored — flagged for
# Annie, not touched by this pass (see final report / conflicts note).
DATA_INTEGRITY_FLAGS = {
    "weal-cleric": "Name/Key say Cleric ('Weal'); Class field + HTML are Warlock ('Mire').",
    "mark-prey-ranger": "Name/Key say Ranger ('Mark Prey'); Class field + HTML are Warlock "
    "('Shadow Step') — and warlock already has its own separate 'Shadow Step' card "
    "(shadow-step-warlock) with a different effect (Hit Die spend vs. Arcana check). Duplicate name.",
    "volley-ranger": "Name/Key say Ranger ('Volley'); Class field + HTML are Wizard ('Magic Missile').",
    "read-the-land-ranger": "Name/Key say Ranger ('Read the Land'); Class field + HTML are Wizard ('Frost Nova').",
    "suppressing-fire-ranger": "Name/Key say Ranger ('Suppressing Fire'); Class field + HTML are Wizard ('Arcane Deflection').",
    "discipline-ranger": "Name/Key say Ranger ('Discipline'); Class field + HTML are Wizard ('Counterspell').",
}


def load_cards() -> list[dict]:
    text = CARD_DATA.read_text(encoding="utf-8")
    start = text.index("[")
    end = text.rindex("]") + 1
    return json.loads(text[start:end])


def apply_replacements(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    by_key = {c["Card_Key"]: c for c in cards}
    batch: list[dict] = []
    missing_keys = [k for k in REPLACEMENTS if k not in by_key]
    if missing_keys:
        raise SystemExit(f"Card keys not found in card-data.js: {missing_keys}")

    for key, pairs in REPLACEMENTS.items():
        card = by_key[key]
        html = card["HTML"]
        for old, new in pairs:
            count = html.count(old)
            if count != 1:
                raise SystemExit(
                    f"{key}: expected exactly 1 match for replacement, found {count}\n  OLD: {old!r}"
                )
            html = html.replace(old, new)
        if html == card["HTML"]:
            continue
        card["HTML"] = html
        card["Last_Rework_Date"] = REWORK_DATE
        card["FlavorText_Plain"] = flavor_plain(html)
        card["EffectText_Plain"] = effect_plain(html)
        batch.append(
            {
                "id": card["id"],
                "HTML": html,
                "Name": card["Name"],
                "Card_Key": key,
                "Last_Rework_Date": REWORK_DATE,
            }
        )

    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    cards_sorted = sorted(cards, key=lambda c: c["id"])
    today = date.today().isoformat()
    header = (
        f"// Generated by scripts/pool_simplification_p4.py — do not edit manually. Last updated: {today}\n"
        f"// Playtest 4 Phase 2C — pool simplification pass (Exposed/Rattled/Rooted/Hidden narrative-term audit)\n"
    )
    CARD_DATA.write_text(
        header + "window.CARD_DATA = " + json.dumps(cards_sorted, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )


def _cards_grid(cards_by_key: dict[str, dict], keys: list[str]) -> str:
    chunks = []
    for key in keys:
        c = cards_by_key[key]
        cls = c.get("Class", "any")
        chunks.append(
            f'<div class="sample"><div class="stag">{c["Name"]} <span class="skey">({key})</span></div>'
            f'<div class="cardwrap scope-ability cls-{cls}">{c["HTML"]}</div></div>'
        )
    return f'<div class="grid">{"".join(chunks)}</div>'


def write_proof(cards: list[dict], keys: list[str]) -> None:
    css = (ROOT / "primer-card-scope.css").read_text(encoding="utf-8")
    by_key = {c["Card_Key"]: c for c in cards}

    groups = {
        "Items": [k for k in keys if k.endswith("-item")],
        "Warlock": [k for k in keys if k.endswith("-warlock")],
        "Fighter": [k for k in keys if k.endswith("-fighter")],
        "Druid": [k for k in keys if k.endswith("-druid")],
        "Cleric / Ranger / Wizard": [
            k for k in keys if not k.endswith(("-item", "-warlock", "-fighter", "-druid"))
        ],
    }
    sections = "".join(
        f"<h2>{title} ({len(group_keys)})</h2>{_cards_grid(by_key, group_keys)}"
        for title, group_keys in groups.items()
        if group_keys
    )

    PROOF_OUT.write_text(
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<title>Pool simplification — Playtest 4 Phase 2C proof</title>"
        f"<style>{css}\n"
        "body{background:#0f1419;padding:24px;color:#e8eef5;font-family:system-ui,sans-serif;}"
        "h1{font-size:20px;}h2{font-size:15px;margin-top:36px;color:#c9b896;"
        "text-transform:uppercase;letter-spacing:1px;border-bottom:1px solid #333;padding-bottom:6px;}"
        ".grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px;margin-top:16px;}"
        ".stag{font-size:10px;text-transform:uppercase;letter-spacing:1px;text-align:center;"
        "margin-bottom:8px;color:#c9b896;}.skey{color:#777;text-transform:none;letter-spacing:0;}"
        "</style></head><body>"
        "<h1>Pool simplification pass — Playtest 4 Phase 2C</h1>"
        "<p style=\"max-width:760px;color:#aab;\">Every card below had legacy unit-linked condition "
        "language (duration tracking, stacked conditions, GM-improvised effects) or a retired mechanic "
        "(Item Check / placed dice / Disguised) removed. Narrative terms (Exposed, Rattled, Rooted, "
        "Hidden) now follow the locked Playtest 4 pattern: bold word + em-dash gloss, one term per line, "
        "no cross-turn tracking.</p>"
        f"{sections}"
        "</body></html>",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Patch card-data.js and write batch JSON + proof")
    parser.add_argument("--push", action="store_true", help="Write, then push to Baserow")
    args = parser.parse_args()

    cards = load_cards()
    cards, batch = apply_replacements(cards)

    print(f"Rewrote {len(batch)} / {len(REPLACEMENTS)} targeted cards")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']} -> {item['Name']}")
    print(f"Reviewed clean (no change): {len(CLEAN_NO_CHANGE)} — {', '.join(CLEAN_NO_CHANGE)}")
    print(f"Data-integrity flags noted (not touched): {len(DATA_INTEGRITY_FLAGS)}")

    if args.write or args.push:
        write_card_data(cards)
        write_proof(cards, list(REPLACEMENTS.keys()))
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name}, {PROOF_OUT.name}, {BATCH_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run only. Pass --write or --push to apply.")


if __name__ == "__main__":
    main()
