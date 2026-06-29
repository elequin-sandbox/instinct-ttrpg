#!/usr/bin/env python3
"""Build Paladin Oath Core card HTML (patron mark-pill layout)."""
from __future__ import annotations

# Permanent Oath pick at creation — each has lateral, spread-out word pools.
OATHS = [
    {
        "name": "The Open Hand",
        "key": "the-open-hand-paladin-core",
        "sub": "What you reach for defines you.",
        "verbs": ["Shelter", "Mend", "Witness", "Carry", "Welcome"],
        "nouns": ["Frail", "Stranger", "Threshold", "Burden", "Ember"],
        "example": "Shelter the Frail",
    },
    {
        "name": "The Severed Ledger",
        "key": "the-severed-ledger-paladin-core",
        "sub": "Some accounts refuse to stay closed.",
        "verbs": ["Name", "Trace", "Unmask", "Settle", "Refuse"],
        "nouns": ["Debt", "Liar", "Scar", "Silence", "Price"],
        "example": "Name the Liar",
    },
    {
        "name": "The Last Bastion",
        "key": "the-last-bastion-paladin-core",
        "sub": "When everything else gives way, something must not.",
        "verbs": ["Hold", "Keep", "Rally", "Seal", "Bind"],
        "nouns": ["Gate", "Line", "Banner", "Bastion", "Standard"],
        "example": "Hold the Line",
    },
    {
        "name": "The Wax and the Wick",
        "key": "the-wax-and-the-wick-paladin-core",
        "sub": "You carry fire where the map runs out.",
        "verbs": ["Kindle", "Reveal", "Mark", "Chase", "Weather"],
        "nouns": ["Fog", "Path", "Spark", "Shadow", "Crossroads"],
        "example": "Reveal the Path",
    },
    {
        "name": "The Old Compass",
        "key": "the-old-compass-paladin-core",
        "sub": "North is whoever needs you when you arrive.",
        "verbs": ["Find", "Follow", "Return", "Chart", "Answer"],
        "nouns": ["Lost", "Horizon", "Anchor", "Mile", "Promise"],
        "example": "Find the Lost",
    },
]

# Baserow row IDs for in-place updates (legacy keys retired via rename).
OATH_ROW_IDS = {
    "the-open-hand-paladin-core": 697,
    "the-severed-ledger-paladin-core": 698,
    "the-last-bastion-paladin-core": 699,
}

PILL = (
    '<div class="mark-pill" style="display:inline-flex;align-items:stretch;border-radius:2px;'
    'overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);">'
    '<span class="kw kw-crit" style="font-size:7.5px;padding:1px 4px;">{n}</span>'
    '<strong style="color:#1a1008;font-size:7.5px;font-weight:700;padding:1px 5px;'
    'font-family:system-ui,-apple-system,sans-serif;text-transform:uppercase;letter-spacing:0.3px;">'
    "{word}</strong></div>"
)

BLANK_PILL = (
    '<div class="mark-pill" style="display:inline-flex;align-items:stretch;border-radius:2px;'
    'overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);min-width:28px;">'
    '<span class="kw kw-crit" style="font-size:7.5px;padding:1px 4px;">{n}</span>'
    '<strong style="color:#1a1008;font-size:7.5px;font-weight:700;padding:1px 8px;'
    'font-family:system-ui,-apple-system,sans-serif;letter-spacing:0.3px;">&nbsp;</strong></div>'
)


def row(words: list[str] | None = None, *, blank: bool = False) -> str:
    if blank:
        pills = [BLANK_PILL.format(n=i + 1) for i in range(6)]
    else:
        pills = [PILL.format(n=i + 1, word=words[i]) for i in range(5)]
        pills.append(PILL.format(n=6, word="★ Choose"))
    return '<div class="marks-row" style="display:flex;flex-wrap:wrap;gap:2px;">' + "".join(pills) + "</div>"


SET_STAND = (
    "When you <strong>Enter</strong> a <strong>Scene</strong>, roll 2d6. Place one die on a "
    "<strong>Verb</strong> and one on a <strong>Noun</strong>. Your <strong>Stand</strong> is that "
    "phrase{example}. It is your priority above all else this <strong>Scene</strong>."
)

FULFILL_STAND = (
    "Once per <strong>Scene</strong>, when the GM agrees your <strong>Action</strong>'s "
    "<em>primary purpose</em> fulfills your <strong>Stand</strong>, add both dice from the card "
    "to that roll, then remove them."
)

BREAK_STAND = (
    "When you <strong>Enter</strong> a <strong>Scene</strong>, before rolling, you may "
    "<strong>Break</strong> your <strong>Stand</strong> — narrate turning from it. "
    "<strong>Discard</strong> your hand, <strong>Draw</strong> that many. You do not roll a "
    "<strong>Stand</strong> this scene. Your Oath card stays in the Active area."
)


def _break_box() -> str:
    return (
        '<div class="rule"></div>'
        '<div style="background:rgba(90,74,32,0.08);border:0.5px solid rgba(90,74,32,0.35);'
        'border-radius:3px;padding:3px 5px;">'
        '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;color:#5a4020;">'
        "Break Your Stand</div>"
        f'<div class="effect-text" style="font-size:7.5px;line-height:1.4;color:#5a4020;font-style:italic;">'
        f"{BREAK_STAND}</div></div>"
    )


def build(oath: dict, *, include_break: bool = True) -> str:
    ex = oath.get("example", "")
    example = f" — e.g. <em>{ex}</em>" if ex else ""
    body = (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        f'<div class="hdr-name">{oath["name"]}</div>'
        f'<div class="hdr-sub">{oath["sub"]}</div></div>'
        '<div class="card-body" style="gap:3px;padding:5px 10px;">'
        '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Verbs</div>'
        + row(oath["verbs"])
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Nouns</div>'
        + row(oath["nouns"])
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Set Your Stand</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{SET_STAND.format(example=example)}</div>'
        + '<div class="rule"></div>'
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Fulfill Your Stand</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{FULFILL_STAND}</div>'
        + (_break_box() if include_break else "")
        + "</div><div class=\"idtag\">Paladin</div></div>"
    )
    return body


def build_oath_template() -> str:
    blank_name = (
        '<div class="hdr-name" style="min-height:18px;border-bottom:1px dashed rgba(0,0,0,0.25);'
        'background:transparent;">&nbsp;</div>'
    )
    blank_sub = (
        '<div class="hdr-sub" style="min-height:12px;border-bottom:1px dashed rgba(0,0,0,0.15);'
        'margin:0 12px 4px;">&nbsp;</div>'
    )
    return (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        + blank_name
        + blank_sub
        + '</div><div class="card-body" style="gap:3px;padding:5px 10px;">'
        '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Verbs</div>'
        + row(blank=True)
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Nouns</div>'
        + row(blank=True)
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Set Your Stand</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{SET_STAND.format(example="")}</div>'
        + '<div class="rule"></div>'
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Fulfill Your Stand</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{FULFILL_STAND}</div>'
        + _break_box()
        + "</div><div class=\"idtag\">Paladin</div></div>"
    )


def build_patron_template() -> str:
    blank_name = (
        '<div class="hdr-name" style="min-height:18px;border-bottom:1px dashed rgba(0,0,0,0.25);'
        'background:transparent;">&nbsp;</div>'
    )
    blank_sub = (
        '<div class="hdr-sub" style="min-height:12px;border-bottom:1px dashed rgba(0,0,0,0.15);'
        'margin:0 12px 4px;">&nbsp;</div>'
    )
    invoke = (
        "Call them forth and select one of the <strong>Marks</strong> above to warp the "
        "<strong>Scene</strong> in your favor. Then <strong>Shuffle</strong> this card into your "
        "<strong>Draw</strong> Pile."
    )
    bane = (
        "Announce that your Patron has arrived. Roll a d6 to determine which <strong>Mark</strong> "
        "you must pay. The GM decides the cost before this <strong>Scene</strong> ends."
    )
    return (
        '<div class="card warlock acc-warlock"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        + blank_name
        + blank_sub
        + '</div><div class="card-body" style="gap:3px;padding:5px 10px;">'
        '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">The Marks of</div>'
        + row(blank=True)
        + '<div class="zone-label" style="font-size:6px;letter-spacing:0.8px;margin-top:0;">Invoke Their Name</div>'
        + f'<div class="effect-text" style="font-size:9px;line-height:1.4;">{invoke}</div>'
        + '<div class="rule"></div>'
        + '<div style="background:rgba(138,32,16,0.08);border:0.5px solid rgba(138,32,16,0.3);border-radius:3px;padding:3px 5px;">'
        + '<div class="bane-label" style="font-family:\'Cinzel\',serif;font-size:6px;letter-spacing:1px;'
        'text-transform:uppercase;color:#8a2010;margin-bottom:1px;">🔒 Bane — To Clear This:</div>'
        + f'<div class="effect-text" style="font-size:7.5px;line-height:1.4;color:#8a2010;font-style:italic;">{bane}</div>'
        + "</div></div><div class=\"idtag\">Warlock</div></div>"
    )


if __name__ == "__main__":
    for o in OATHS:
        print(o["name"], len(build(o)))
