#!/usr/bin/env python3
"""Strip Origin/Bond stems from Background, Ancestry, and Bond cards.

Tier 2 pass:
- Remove bf-stem-label / bf-stem / bf-fill blocks
- Remove bf-type chips from Background cards
- Inject 1-line bf-flv on all Backgrounds
- Reformat Bond bf-eff into Find / Act / Then zones

Usage:
  python3 scripts/strip_origin_stems.py              # dry-run summary
  python3 scripts/strip_origin_stems.py --write      # patch card-data.js + emit batch JSON
  python3 scripts/strip_origin_stems.py --push       # patch + push to Baserow (needs token)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD_DATA = ROOT / "card-data.js"
BATCH_OUT = ROOT / "scripts" / "strip_origin_stems_batch.json"
API = "https://api.baserow.io/api/database/rows/table/911939/batch/?user_field_names=true"
DATE = "2026-06-29"

# Tier 2 — one-line flavor per Background (2nd person, present tense)
BACKGROUND_FLAVOR: dict[str, str] = {
    "Gambler": "You have learned that fortune favors the prepared — and the reckless.",
    "Field Medic": "You know what to do when someone is bleeding and the clock is running.",
    "Inspector": "You notice what others walk past — the detail that changes everything.",
    "Trade Road Courier": "You have carried messages and names across distances most people never cross.",
    "Cutpurse": "Your hands know routes that eyes never track.",
    "Pit Fighter": "You have stood in places that would break most people and walked out standing.",
    "Musician": "You feel the rhythm of a room before anyone else names it.",
    "Street-Raised": "The city taught you early that nothing stays still for long.",
    "Caravan Guard": "You have learned to read people faster than you read terrain.",
    "Pilgrim": "You walk toward something larger than any single road.",
    "Ascetic": "You have tested what you believe against pain, pressure, and doubt.",
    "Pathfinder": "You read uncertain ground the way others read faces.",
}

# Bond Find / Act zones (Act extracted from legacy effect where not overridden)
BOND_ZONES: dict[str, dict[str, str]] = {
    "Warm Presence": {
        "find": "Someone carrying weight they have not named.",
        "act": "Offer care or support without being asked.",
    },
    "The Spark": {
        "find": "Someone who has disengaged or stalled.",
        "act": "Draw them back in — a question, a nudge, a small invitation.",
    },
    "Steady Hands": {
        "find": "Someone facing a moment that could shake them.",
        "act": "Stay grounded and steady while the tension holds.",
    },
    "The Listener": {
        "find": "Someone with something they have not said aloud.",
        "act": "Ask a genuine question and hold space for whatever comes back.",
    },
    "Sharp Eye": {
        "find": "Someone who missed what you noticed.",
        "act": "Share something specific you saw that they did not.",
    },
    "The Confessor": {
        "find": "Someone who needs a witness, not advice.",
        "act": "Make yourself fully open — no agenda, no judgment, just presence.",
    },
    "Loyal to a Fault": {
        "find": "Someone you would stand beside without needing a reason.",
        "act": "Make clear, without qualification, that you are with them.",
    },
    "The Levity": {
        "find": "A room that needs to breathe.",
        "act": "Ease tension with something light — a joke, a story, a moment of warmth.",
    },
    "Quiet Respect": {
        "find": "Someone whose effort deserves to be named.",
        "act": "Name something specific you noticed or respect about them.",
    },
    "The Protector": {
        "find": "Someone who should not face what comes next alone.",
        "act": "Commit, plainly, to facing it with them.",
    },
    "Honest Mirror": {
        "find": "Someone who needs truth more than comfort.",
        "act": "Tell them something true and necessary, even when it is uncomfortable.",
    },
    "The Witness": {
        "find": "Someone whose moment deserves to be held.",
        "act": "Tell them specifically what you have seen them do or endure.",
    },
}

THEN_HTML = (
    'If it lands, you both gain <span class="kw kw-boost">Boost 1</span>.'
)

STEM_RE = re.compile(
    r'<div class="bf-stem-label">[^<]*</div>\s*'
    r'<div class="bf-stem">.*?</div>',
    re.DOTALL,
)
TYPE_CHIP_RE = re.compile(r'<div class="bf-type">[^<]*</div>\s*')


def read_token() -> str:
    token = os.environ.get("BASEROW_TOKEN", "").strip()
    if token:
        return token
    text = (ROOT / "config.js").read_text(encoding="utf-8")
    m = re.search(r'IRPG_TOKEN\s*=\s*"([^"]*)"', text)
    token = (m.group(1) if m else "").strip()
    if token and token != "PASTE_YOUR_SCOPED_BASEROW_TOKEN_HERE":
        return token
    return ""


def load_cards() -> list[dict]:
    text = CARD_DATA.read_text(encoding="utf-8")
    start = text.index("[")
    end = text.rindex("]") + 1
    return json.loads(text[start:end])


def build_bond_eff(name: str, legacy_html: str) -> str:
    zones = BOND_ZONES.get(name)
    if not zones:
        m = re.search(
            r"Start a conversation where you (.+?)\. If it lands",
            re.sub(r"<[^>]+>", "", legacy_html),
        )
        act = m.group(1).strip() if m else legacy_html
        zones = {"find": "Someone at the table who fits this moment.", "act": act}
    parts = [
        '<div class="bf-zone">',
        '<div class="bf-zone-lbl">Find</div>',
        f'<div class="bf-zone-txt">{zones["find"]}</div>',
        "</div>",
        '<div class="bf-zone">',
        '<div class="bf-zone-lbl">Act</div>',
        f'<div class="bf-zone-txt">{zones["act"]}</div>',
        "</div>",
        '<div class="bf-zone">',
        '<div class="bf-zone-lbl">Then</div>',
        f'<div class="bf-zone-txt">{THEN_HTML}</div>',
        "</div>",
    ]
    return "<div class=\"bf-eff\">" + "".join(parts) + "</div>"


def transform_html(card: dict) -> str | None:
    ctype = card.get("Card_Type", "")
    if ctype not in {"Background", "Ancestry", "Bond"}:
        return None

    html = card.get("HTML", "")
    if "bf-stem-label" not in html and ctype != "Background":
        return None

    out = html

    if ctype == "Bond":
        m = re.search(r'<div class="bf-eff">(.+?)</div>\s*<div class="bf-stem-label">', out, re.DOTALL)
        if m:
            new_eff = build_bond_eff(card.get("Name", ""), m.group(1))
            out = out[: m.start()] + new_eff + out[m.end() - len('<div class="bf-stem-label">') :]

    if ctype == "Background":
        out = TYPE_CHIP_RE.sub("", out)
        name = card.get("Name", "")
        flavor = BACKGROUND_FLAVOR.get(name)
        if flavor and 'class="bf-flv"' not in out:
            insert = f'<div class="bf-body"><div class="bf-flv">{flavor}</div>'
            out = out.replace('<div class="bf-body">', insert, 1)
        elif flavor is None:
            raise ValueError(f"Missing BACKGROUND_FLAVOR for {name!r}")

    out = STEM_RE.sub("", out)
    return out


def patch_card_data(cards: list[dict]) -> tuple[list[dict], list[dict]]:
    """Return (updated_cards, batch_items for Baserow)."""
    batch: list[dict] = []
    for card in cards:
        new_html = transform_html(card)
        if new_html and new_html != card.get("HTML"):
            card["HTML"] = new_html
            card["Last_Rework_Date"] = DATE
            batch.append(
                {
                    "id": card["id"],
                    "Name": card.get("Name"),
                    "Card_Key": card.get("Card_Key"),
                    "HTML": new_html,
                    "Last_Rework_Date": DATE,
                }
            )
    return cards, batch


def write_card_data(cards: list[dict]) -> None:
    payload = json.dumps(cards, ensure_ascii=False, separators=(",", ":"))
    CARD_DATA.write_text(
        f"// Auto-generated card data — do not hand-edit; regenerate from Baserow.\n"
        f"// Source: strip_origin_stems.py ({DATE})\n"
        f"window.CARD_DATA = {payload};\n",
        encoding="utf-8",
    )


def push_baserow(batch: list[dict]) -> None:
    token = read_token()
    if not token:
        raise SystemExit(
            "Baserow token required: set BASEROW_TOKEN or window.IRPG_TOKEN in config.js"
        )
    body = json.dumps({"items": batch}).encode("utf-8")
    req = urllib.request.Request(
        API,
        data=body,
        method="PATCH",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise SystemExit(
            f"Baserow PATCH failed ({e.code}): {e.read().decode('utf-8', errors='replace')}"
        ) from e
    items = result.get("items") or batch
    print(f"Pushed {len(items)} rows to Baserow table 911939:")
    for item in batch:
        print(f"  row {item['id']}: {item['Card_Key']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Patch card-data.js and write batch JSON")
    parser.add_argument("--push", action="store_true", help="Patch, write batch, and push to Baserow")
    args = parser.parse_args()

    cards = load_cards()
    targets = [c for c in cards if c.get("Card_Type") in {"Background", "Ancestry", "Bond"}]
    cards, batch = patch_card_data(cards)

    print(f"Transformed {len(batch)} / {len(targets)} boon-family cards")
    for item in batch:
        print(f"  {item['Card_Key']}")

    if args.write or args.push:
        write_card_data(cards)
        BATCH_OUT.write_text(json.dumps(batch, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {CARD_DATA.name} and {BATCH_OUT.name}")

    if args.push:
        push_baserow(batch)
    elif not args.write:
        print("Dry run only. Pass --write or --push to apply.")


if __name__ == "__main__":
    main()
