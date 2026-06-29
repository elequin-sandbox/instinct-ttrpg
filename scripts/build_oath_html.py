#!/usr/bin/env python3
"""Build Paladin Oath Core card HTML (compact Vow layout)."""
from __future__ import annotations

# Permanent Oath pick at creation — each has lateral, spread-out word pools (6×6).
OATHS = [
    {
        "name": "The Open Hand",
        "key": "the-open-hand-paladin-core",
        "sub": "What you reach for defines you.",
        "verbs": ["Shelter", "Mend", "Witness", "Carry", "Welcome", "Tend"],
        "nouns": ["Frail", "Stranger", "Threshold", "Burden", "Ember", "Need"],
    },
    {
        "name": "The Severed Ledger",
        "key": "the-severed-ledger-paladin-core",
        "sub": "Some accounts refuse to stay closed.",
        "verbs": ["Name", "Trace", "Unmask", "Settle", "Refuse", "Reckon"],
        "nouns": ["Debt", "Liar", "Scar", "Silence", "Price", "Account"],
    },
    {
        "name": "The Last Bastion",
        "key": "the-last-bastion-paladin-core",
        "sub": "When everything else gives way, something must not.",
        "verbs": ["Hold", "Keep", "Rally", "Seal", "Bind", "Endure"],
        "nouns": ["Gate", "Line", "Banner", "Bastion", "Standard", "Refuge"],
    },
    {
        "name": "The Wax and the Wick",
        "key": "the-wax-and-the-wick-paladin-core",
        "sub": "You carry fire where the map runs out.",
        "verbs": ["Kindle", "Reveal", "Mark", "Chase", "Weather", "Light"],
        "nouns": ["Fog", "Path", "Spark", "Shadow", "Crossroads", "Flame"],
    },
    {
        "name": "The Old Compass",
        "key": "the-old-compass-paladin-core",
        "sub": "North is whoever needs you when you arrive.",
        "verbs": ["Find", "Follow", "Return", "Chart", "Answer", "Seek"],
        "nouns": ["Lost", "Horizon", "Anchor", "Mile", "Promise", "Call"],
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
    '<div class="mark-pill" style="display:flex;flex-direction:column;align-items:stretch;'
    'width:100%;border-radius:2px;overflow:hidden;border:0.5px solid rgba(0,0,0,0.2);">'
    '<span class="kw kw-crit" style="font-size:6.5px;padding:1px 0;line-height:1.1;text-align:center;">'
    "{n}</span>"
    '<strong style="color:#1a1008;font-size:6.5px;font-weight:700;padding:0 2px 2px;'
    "font-family:system-ui,-apple-system,sans-serif;text-transform:uppercase;"
    'letter-spacing:0.2px;line-height:1.15;text-align:center;word-break:break-word;">'
    "{word}</strong></div>"
)

BLANK_PILL = (
    '<div class="mark-pill" style="display:flex;flex-direction:column;align-items:stretch;'
    'width:100%;min-height:18px;border-radius:2px;overflow:hidden;'
    'border:0.5px solid rgba(0,0,0,0.2);">'
    '<span class="kw kw-crit" style="font-size:6.5px;padding:1px 0;line-height:1.1;text-align:center;">'
    "{n}</span>"
    '<strong style="color:#1a1008;font-size:6.5px;font-weight:700;padding:0 2px 2px;'
    'font-family:system-ui,-apple-system,sans-serif;letter-spacing:0.2px;">&nbsp;</strong></div>'
)

VOW_GRID = (
    '<div class="vow-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
    'gap:2px;margin:1px 0;width:100%;">{cells}</div>'
)

VOW_CELL = (
    '<div class="vow-cell" style="display:flex;min-width:0;">{pill}</div>'
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


def _pill(n: int, word: str | None = None) -> str:
    if word is None:
        return BLANK_PILL.format(n=n)
    return PILL.format(n=n, word=word)


def word_grid(words: list[str] | None = None, *, blank: bool = False) -> str:
    cells = []
    for i in range(6):
        n = i + 1
        pill = _pill(n, None if blank else words[i])  # type: ignore[index]
        cells.append(VOW_CELL.format(pill=pill))
    return VOW_GRID.format(cells="".join(cells))


def word_stack(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    verb_grid = word_grid(blank=blank) if blank else word_grid(verbs or [])
    noun_grid = word_grid(blank=blank) if blank else word_grid(nouns or [])
    return verb_grid + THE_DIVIDER + noun_grid


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
        + word_grid(blank=True)
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
