#!/usr/bin/env python3
"""Build Paladin Oath Core card HTML (compact Vow layout)."""
from __future__ import annotations

# Permanent Oath pick at creation — each has lateral, spread-out word pools.
OATHS = [
    {
        "name": "The Open Hand",
        "key": "the-open-hand-paladin-core",
        "sub": "What you reach for defines you.",
        "verbs": ["Shelter", "Mend", "Witness", "Carry", "Welcome"],
        "nouns": ["Frail", "Stranger", "Threshold", "Burden", "Ember"],
    },
    {
        "name": "The Severed Ledger",
        "key": "the-severed-ledger-paladin-core",
        "sub": "Some accounts refuse to stay closed.",
        "verbs": ["Name", "Trace", "Unmask", "Settle", "Refuse"],
        "nouns": ["Debt", "Liar", "Scar", "Silence", "Price"],
    },
    {
        "name": "The Last Bastion",
        "key": "the-last-bastion-paladin-core",
        "sub": "When everything else gives way, something must not.",
        "verbs": ["Hold", "Keep", "Rally", "Seal", "Bind"],
        "nouns": ["Gate", "Line", "Banner", "Bastion", "Standard"],
    },
    {
        "name": "The Wax and the Wick",
        "key": "the-wax-and-the-wick-paladin-core",
        "sub": "You carry fire where the map runs out.",
        "verbs": ["Kindle", "Reveal", "Mark", "Chase", "Weather"],
        "nouns": ["Fog", "Path", "Spark", "Shadow", "Crossroads"],
    },
    {
        "name": "The Old Compass",
        "key": "the-old-compass-paladin-core",
        "sub": "North is whoever needs you when you arrive.",
        "verbs": ["Find", "Follow", "Return", "Chart", "Answer"],
        "nouns": ["Lost", "Horizon", "Anchor", "Mile", "Promise"],
    },
]

OATH_ROW_IDS = {
    "the-open-hand-paladin-core": 697,
    "the-severed-ledger-paladin-core": 698,
    "the-last-bastion-paladin-core": 699,
    "the-wax-and-the-wick-paladin-core": 700,
    "the-old-compass-paladin-core": 701,
    "oath-template-paladin-core": 702,
    "patron-template-warlock-core": 703,
}

PILL = (
    '<div class="mark-pill" style="display:inline-flex;align-items:stretch;border-radius:2px;'
    'overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);">'
    '<span class="kw kw-crit" style="font-size:7px;padding:1px 3px;">{n}</span>'
    '<strong style="color:#1a1008;font-size:7px;font-weight:700;padding:1px 4px;'
    'font-family:system-ui,-apple-system,sans-serif;text-transform:uppercase;letter-spacing:0.3px;">'
    "{word}</strong></div>"
)

BLANK_PILL = (
    '<div class="mark-pill" style="display:inline-flex;align-items:stretch;border-radius:2px;'
    'overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);min-width:22px;">'
    '<span class="kw kw-crit" style="font-size:7px;padding:1px 3px;">{n}</span>'
    '<strong style="color:#1a1008;font-size:7px;font-weight:700;padding:1px 5px;'
    'font-family:system-ui,-apple-system,sans-serif;letter-spacing:0.3px;">&nbsp;</strong></div>'
)

CENTER_ROW = (
    '<div class="marks-row" style="display:flex;flex-wrap:wrap;gap:2px;'
    'justify-content:center;margin:1px 0;">{pills}</div>'
)

THE_DIVIDER = (
    '<div style="display:flex;align-items:center;justify-content:center;position:relative;'
    'height:10px;margin:1px 0;">'
    '<span style="position:absolute;left:4px;right:4px;top:50%;height:1px;'
    'background:#c8a96e;opacity:0.45;"></span>'
    '<span style="position:relative;z-index:1;background:#f7f0e0;padding:0 6px;'
    "font-family:'EB Garamond',Georgia,serif;font-size:8px;font-style:italic;"
    'color:#7a6030;">the</span></div>'
)

ENTER_VOW = (
    "At <strong>Enter</strong>, roll 2d6 for your scene <strong>Vow</strong> on this "
    "<strong>Oath</strong>."
)

FULFILL_VOW = (
    "Once per <strong>Scene</strong>, if the GM agrees your <strong>Action</strong> fulfills "
    "your <strong>Vow</strong> in purpose, add both dice — "
    '<span class="kw kw-boost">Boost 2</span> on that roll.'
)

BREAK_VOW = (
    "At <strong>Enter</strong>, before rolling, you may <strong>Break</strong> your "
    "<strong>Vow</strong>. <strong>Discard</strong> your hand, <strong>Draw</strong> that many. "
    "No <strong>Vow</strong> this scene; <strong>Oath</strong> stays Active."
)

BODY_STYLE = "gap:2px;padding:4px 9px 32px;"


def etxt(content: str, *, extra_style: str = "") -> str:
    style = f"font-size:8.5px;line-height:1.35;text-align:center;{extra_style}"
    return f'<div class="effect-text" style="{style}">{content}</div>'


def etxt_break(content: str) -> str:
    style = "font-size:7px;line-height:1.35;color:#5a4020;font-style:italic;text-align:left;"
    return f'<div class="effect-text" style="{style}">{content}</div>'


def row(words: list[str] | None = None, *, blank: bool = False) -> str:
    if blank:
        pills = [BLANK_PILL.format(n=i + 1) for i in range(6)]
    else:
        pills = [PILL.format(n=i + 1, word=words[i]) for i in range(5)]
        pills.append(PILL.format(n=6, word="★"))
    return CENTER_ROW.format(pills="".join(pills))


def word_stack(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    verb_row = row(blank=blank) if blank else row(verbs or [])
    noun_row = row(blank=blank) if blank else row(nouns or [])
    return verb_row + THE_DIVIDER + noun_row


def _break_box() -> str:
    return (
        '<div class="rule" style="margin:2px 0 1px;"></div>'
        '<div style="background:rgba(90,74,32,0.08);border:0.5px solid rgba(90,74,32,0.35);'
        'border-radius:3px;padding:2px 5px 3px;margin-bottom:2px;">'
        + etxt_break(BREAK_VOW)
        + "</div>"
    )


def _body_block(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    return (
        etxt(ENTER_VOW, extra_style="margin-bottom:2px;")
        + word_stack(blank=blank, verbs=verbs, nouns=nouns)
        + '<div class="rule" style="margin:3px 0 2px;"></div>'
        + etxt(FULFILL_VOW)
    )


def build(oath: dict, *, include_break: bool = True) -> str:
    return (
        '<div class="card paladin acc-paladin"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        f'<div class="hdr-name">{oath["name"]}</div>'
        f'<div class="hdr-sub">{oath["sub"]}</div></div>'
        f'<div class="card-body" style="{BODY_STYLE}">'
        + _body_block(verbs=oath["verbs"], nouns=oath["nouns"])
        + (_break_box() if include_break else "")
        + "</div><div class=\"idtag\">Paladin</div></div>"
    )


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
        + f'</div><div class="card-body" style="{BODY_STYLE}">'
        + _body_block(blank=True)
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
