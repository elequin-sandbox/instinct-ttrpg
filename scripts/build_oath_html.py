#!/usr/bin/env python3
"""Build Paladin Oath Core card HTML (matches patron mark-pill layout)."""
from __future__ import annotations

OATHS = [
    {
        "name": "Oath of Devotion",
        "key": "oath-of-devotion-paladin-core",
        "sub": "The good is not safe. You stand anyway.",
        "verbs": ["Protect", "Shield", "Uphold", "Shelter", "Answer"],
        "nouns": ["Innocent", "Vow", "Light", "Weak", "Truth", "Sacred"],
        "example": "Protect the Innocent",
    },
    {
        "name": "Oath of Vengeance",
        "key": "oath-of-vengeance-paladin-core",
        "sub": "Someone will answer for what was done.",
        "verbs": ["Hunt", "Break", "Punish", "Avenge", "Expose", "End"],
        "nouns": ["Guilty", "Betrayer", "Debt", "Wrath", "Wrong", "Traitor"],
        "example": "Hunt the Betrayer",
    },
    {
        "name": "Oath of the Crown",
        "key": "oath-of-the-crown-paladin-core",
        "sub": "The realm does not hold itself.",
        "verbs": ["Serve", "Keep", "Hold", "Lead", "Stand", "Guard"],
        "nouns": ["Realm", "Crown", "Law", "Banner", "Gate", "People"],
        "example": "Serve the Realm",
    },
]

PILL = (
    '<div class="mark-pill" style="display:inline-flex;align-items:stretch;border-radius:2px;'
    'overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);">'
    '<span class="kw kw-crit" style="font-size:7.5px;padding:1px 4px;">{n}</span>'
    '<strong style="color:#1a1008;font-size:7.5px;font-weight:700;padding:1px 5px;'
    'font-family:system-ui,-apple-system,sans-serif;text-transform:uppercase;letter-spacing:0.3px;">'
    "{word}</strong></div>"
)


def row(words: list[str]) -> str:
    pills = [PILL.format(n=i + 1, word=words[i]) for i in range(5)]
    pills.append(PILL.format(n=6, word="★ Choose"))
    return '<div class="marks-row" style="display:flex;flex-wrap:wrap;gap:2px;">' + "".join(pills) + "</div>"


def build(oath: dict) -> str:
    set_text = (
        f"When you <strong>Enter</strong> a <strong>Scene</strong>, roll 2d6. Place one die on a "
        f"<strong>Verb</strong> and one on a <strong>Noun</strong>. Your scene <strong>Charge</strong> "
        f"is that phrase — e.g. <em>{oath['example']}</em>. It is your priority above all else this "
        f"<strong>Scene</strong>."
    )
    fulfill = (
        "Once per <strong>Scene</strong>, when the GM agrees your <strong>Action</strong> fulfills "
        "your <strong>Charge</strong>, add both dice from the card to that roll, then remove them."
    )
    return (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        f'<div class="hdr-name">{oath["name"]}</div>'
        f'<div class="hdr-sub">{oath["sub"]}</div></div>'
        '<div class="card-body" style="gap:3px;padding:5px 10px;">'
        '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Verbs</div>'
        + row(oath["verbs"])
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Nouns</div>'
        + row(oath["nouns"])
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Set Your Charge</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{set_text}</div>'
        + '<div class="rule"></div>'
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Fulfill Your Charge</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{fulfill}</div>'
        + "</div><div class=\"idtag\">Paladin</div></div>"
    )


if __name__ == "__main__":
    import json

    for o in OATHS:
        print(o["name"], len(build(o)))
