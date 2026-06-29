#!/usr/bin/env python3
"""Build Paladin Oath Core card HTML (Vow grid + Oath-of ribbon header)."""
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

HDR_TOP = (
    '<div class="hdr-top"><span style="display:inline-flex;gap:3px;align-items:center;">'
    '<span class="cap cap-neutral">Core</span><span class="cap cap-neutral">Oath</span>'
    "</span><span></span></div>"
)

OATH_OF_PREFIX = (
    '<span style="flex-shrink:0;font-family:system-ui,-apple-system,sans-serif;font-size:7px;'
    "font-weight:800;letter-spacing:0.5px;text-transform:uppercase;padding:2px 6px;"
    "background:var(--ad,#976e09);color:var(--at,#f5eedd);border:1px solid var(--a,#B8860B);"
    'border-radius:3px;line-height:1.2;">Oath of</span>'
)

# Shared phrase styling — verb, *the*, noun read as one golden constructed line.
VOW_TERM = (
    "font-family:'EB Garamond',Georgia,serif;font-size:7.5px;font-weight:700;font-style:italic;"
    "color:var(--ad,#976e09);letter-spacing:0.25px;line-height:1.1;"
)

KW_SM = (
    "font-size:7px;padding:0 2px;border-radius:2px;line-height:1.35;"
    "vertical-align:baseline;font-weight:700;"
)

DIE_SLOT = (
    '<span class="die-slot kw kw-crit" style="flex-shrink:0;width:16px;height:16px;'
    "display:flex;align-items:center;justify-content:center;font-size:7.5px;font-weight:700;"
    'border-radius:3px;margin:1px;line-height:1;">{n}</span>'
)

PILL = (
    '<div class="vow-entry" style="display:flex;align-items:stretch;width:100%;min-height:18px;'
    'border:0.5px solid rgba(184,134,11,0.2);border-radius:3px;overflow:hidden;background:rgba(255,252,245,0.5);">'
    + DIE_SLOT
    + '<span class="vow-term" style="flex:1;display:flex;align-items:center;justify-content:center;'
    "padding:1px 4px 1px 2px;"
    + VOW_TERM
    + 'word-break:break-word;text-align:center;text-transform:none;">'
    "{word}</span></div>"
)

BLANK_PILL = (
    '<div class="vow-entry vow-entry-blank" style="display:flex;align-items:center;width:100%;'
    "min-height:24px;border:0.5px solid rgba(184,134,11,0.25);border-radius:3px;overflow:hidden;"
    'background:rgba(255,252,245,0.55);">'
    + DIE_SLOT
    + '<div class="writein-line" style="flex:1;min-height:16px;margin:3px 6px 3px 2px;'
    'border-bottom:1px dashed rgba(184,134,11,0.4);"></div></div>'
)

VOW_GRID = (
    '<div class="vow-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
    'gap:2px;margin:2px 0;width:100%;">{cells}</div>'
)

BLANK_VOW_GRID = (
    '<div class="vow-grid vow-grid-blank" style="display:grid;'
    'grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(2,minmax(24px,auto));'
    'gap:3px;margin:2px 0;width:100%;">{cells}</div>'
)

VOW_CELL = '<div class="vow-cell" style="display:flex;min-width:0;">{pill}</div>'

THE_DIVIDER = (
    '<div class="vow-the" style="display:flex;align-items:center;justify-content:center;'
    'gap:5px;height:11px;margin:1px 0;">'
    '<span style="flex:1;border-top:1px dotted rgba(184,134,11,0.3);"></span>'
    '<span class="vow-term" style="'
    + VOW_TERM
    + 'padding:0 3px;">the</span>'
    '<span style="flex:1;border-top:1px dotted rgba(184,134,11,0.3);"></span></div>'
)

VOW_PHRASE = (
    '<div class="vow-phrase" style="border:1px dotted rgba(184,134,11,0.5);border-radius:10px;'
    'padding:4px 5px 5px;margin:1px 0;">{inner}</div>'
)

ENTER_VOW = (
    "At <strong>Scene start</strong>: roll 2d6 to determine your new <strong>Vow</strong>:"
)

FULFILL_VOW = (
    "Once per <strong>Scene</strong>: if any <strong>Action</strong> you are taking fulfills your "
    "<strong>Vow</strong> and the GM agrees, add these dice to give that roll "
    '<span class="kw kw-boost" style="' + KW_SM + '">Boost 2</span>'
)

BREAK_VOW = (
    "Describe how you are defying your <strong>Vow</strong>, then place these dice into your "
    '<span class="kw kw-resolve" style="' + KW_SM + '">Resolve</span>. The GM gains '
    '<span class="kw kw-toll" style="' + KW_SM + '">Toll 2</span> and must use it against you this scene.'
)

BODY_STYLE = "gap:3px;padding:4px 9px 32px;"
TEMPLATE_BODY_STYLE = "gap:3px;padding:3px 8px 30px;"


def _hdr_name(name: str = "", *, blank: bool = False) -> str:
    ribbon = (
        'display:flex;align-items:center;justify-content:flex-start;gap:5px;'
        "padding-left:8px;padding-right:10px;text-align:left;"
    )
    if blank:
        title = (
            '<span style="flex:1;min-height:14px;border-bottom:1px dashed rgba(90,74,32,0.35);'
            'margin-right:4px;">&nbsp;</span>'
        )
        return (
            f'<div class="hdr-name hdr-blankname" style="{ribbon}min-height:26px;">'
            + OATH_OF_PREFIX
            + title
            + "</div>"
        )
    return (
        f'<div class="hdr-name" style="{ribbon}">'
        + OATH_OF_PREFIX
        + f'<span style="flex:1;line-height:1.08;">{name}</span></div>'
    )


def _hdr_sub(sub: str = "", *, blank: bool = False) -> str:
    if blank:
        return (
            '<div class="hdr-sub" style="min-height:16px;border-bottom:1px dashed rgba(90,74,32,0.35);'
            'margin:0 10px 5px;padding-bottom:3px;text-align:left;">'
            '<span style="opacity:.2;font-style:italic;font-size:7px;">subtitle</span></div>'
        )
    return f'<div class="hdr-sub">{sub}</div>'


def etxt(content: str, *, extra_style: str = "") -> str:
    style = f"font-size:8px;line-height:1.42;text-align:left;{extra_style}"
    return f'<div class="effect-text" style="{style}">{content}</div>'


def etxt_break(content: str) -> str:
    style = "font-size:7.5px;line-height:1.42;color:#1a1008;text-align:left;"
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
    grid = BLANK_VOW_GRID if blank else VOW_GRID
    return grid.format(cells="".join(cells))


def word_stack(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    verb_grid = word_grid(blank=blank) if blank else word_grid(verbs or [])
    noun_grid = word_grid(blank=blank) if blank else word_grid(nouns or [])
    inner = verb_grid + THE_DIVIDER + noun_grid
    return VOW_PHRASE.format(inner=inner)


def _break_section() -> str:
    return (
        '<div class="rule" style="margin:5px 0 3px;"></div>'
        '<div class="zone-label" style="font-family:system-ui,-apple-system,sans-serif;font-size:7px;'
        "letter-spacing:0.8px;text-transform:uppercase;color:#5a4020;font-weight:800;"
        'margin-bottom:2px;">Break Your Oath:</div>'
        + etxt_break(BREAK_VOW)
    )


def _body_block(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    return (
        etxt(ENTER_VOW, extra_style="margin-bottom:1px;")
        + word_stack(blank=blank, verbs=verbs, nouns=nouns)
        + '<div class="rule" style="margin:4px 0 2px;"></div>'
        + etxt(FULFILL_VOW)
    )


def _hdr(*, name: str = "", sub: str = "", blank: bool = False) -> str:
    return (
        '<div class="hdr">'
        + HDR_TOP
        + _hdr_name(name, blank=blank)
        + _hdr_sub(sub, blank=blank)
        + "</div>"
    )


def build(oath: dict, *, include_break: bool = True) -> str:
    return (
        '<div class="card paladin acc-paladin">'
        + _hdr(name=oath["name"], sub=oath["sub"])
        + f'<div class="card-body" style="{BODY_STYLE}">'
        + _body_block(verbs=oath["verbs"], nouns=oath["nouns"])
        + (_break_section() if include_break else "")
        + '</div><div class="idtag">Paladin</div></div>'
    )


def build_oath_template() -> str:
    return (
        '<div class="card paladin acc-paladin">'
        + _hdr(blank=True)
        + f'<div class="card-body" style="{TEMPLATE_BODY_STYLE}">'
        + _body_block(blank=True)
        + _break_section()
        + '</div><div class="idtag">Paladin</div></div>'
    )


def build_patron_template() -> str:
    invoke = (
        "Call them forth and select one of the <strong>Marks</strong> above to warp the "
        "<strong>Scene</strong> in your favor. Then <strong>Shuffle</strong> this card into your "
        "<strong>Draw</strong> Pile."
    )
    bane = (
        "Announce that your Patron has arrived. Roll a d6 to determine which <strong>Mark</strong> "
        "you must pay. The GM decides the cost before this <strong>Scene</strong> ends."
    )
    blank_name = (
        '<div class="hdr-name hdr-blankname" style="min-height:28px;">'
        '<span style="opacity:.2;font-style:italic;font-weight:600;font-size:7.5px;">title</span></div>'
    )
    blank_sub = (
        '<div class="hdr-sub" style="min-height:16px;border-bottom:1px dashed rgba(90,74,32,0.35);'
        'margin:0 10px 5px;padding-bottom:3px;">'
        '<span style="opacity:.2;font-style:italic;font-size:7px;">subtitle</span></div>'
    )
    return (
        '<div class="card warlock acc-warlock"><div class="hdr"><div class="hdr-top">'
        '<span class="cap cap-neutral">Core</span><span></span></div>'
        + blank_name
        + blank_sub
        + '</div><div class="card-body" style="gap:3px;padding:4px 9px 28px;">'
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
