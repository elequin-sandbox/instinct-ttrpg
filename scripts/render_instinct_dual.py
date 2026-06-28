#!/usr/bin/env python3
"""Generate dual-purpose Instinct card HTML — Strength top / Flaw bottom stack."""
from __future__ import annotations

INSTINCT_WORDS = [
    "Bold", "Perceptive", "Tenacious", "Resourceful", "Charismatic", "Cunning",
    "Nimble", "Steadfast", "Intuitive", "Fierce", "Learned", "Empathic",
    "Vigilant", "Resilient", "Subtle", "Diplomatic", "Commanding", "Daring",
    "Resolute", "Primal",
    "Stoic", "Impulsive", "Wistful", "Sardonic", "Devoted", "Impish",
    "Brooding", "Earnest", "Guarded", "Gregarious",
]

DIVIDER = {
    "v1": '<div class="inst-divider"><span class="inst-divider-or">OR</span></div>',
    "v2": '<div class="inst-divider"></div>',
    "v3": '<div class="inst-divider"></div>',
    "v4": '<div class="inst-divider"><span class="inst-divider-or">OR</span></div>',
}


def render_instinct_dual(word: str, variant: str = "v1") -> str:
    art = "an" if word[0].lower() in "aeiou" else "a"
    preamble = (
        '<div class="instinct-preamble">This instinct is driving your behavior this scene. '
        "When you <strong>Reveal</strong> this card, perform an <strong>Action</strong> "
        f"in {art} <strong>{word}</strong> manner. <strong>Choose one:</strong></div>"
    )
    pos = (
        "Describe how it benefits your party. If the GM agrees, gain "
        '<span class="kw kw-boost">Boost 2</span> on the <strong>Action</strong>.'
    )
    neg = (
        "Describe how it hinders you or your party. If the GM agrees, <strong>Draw 2</strong>."
    )
    fork = (
        f'<div class="instinct-fork fork-{variant}">'
        '<div class="inst-path inst-path-strength">'
        '<div class="inst-path-lbl">Strength</div>'
        f'<div class="inst-path-txt">{pos}</div></div>'
        f'{DIVIDER.get(variant, DIVIDER["v1"])}'
        '<div class="inst-path inst-path-flaw">'
        '<div class="inst-path-lbl">Flaw</div>'
        f'<div class="inst-path-txt">{neg}</div></div>'
        "</div>"
    )
    return (
        '<div class="card acc-instinct">'
        '<div class="hdr">'
        '<div class="hdr-top"><span class="cap cap-accent">Instinct</span>'
        '<span class="cap cap-neutral">Act</span></div>'
        f'<div class="hdr-name">{word}</div>'
        "</div>"
        f'<div class="cbody cbody-dual">{preamble}{fork}</div>'
        "</div>"
    )


if __name__ == "__main__":
    import json
    import sys

    variant = sys.argv[1] if len(sys.argv) > 1 else "v1"
    out = {w.lower(): render_instinct_dual(w, variant) for w in INSTINCT_WORDS}
    print(json.dumps(out, indent=2))
