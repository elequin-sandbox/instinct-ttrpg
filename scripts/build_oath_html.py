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

# Body typography — +5% vs prior oath baseline (post-header only).
BODY_FONT = "9px"
BODY_FONT_SM = "8.5px"

# Phrase typography — verb/noun lists: bold serif, not italic (readability at print size).
VOW_TERM = (
    "font-family:'EB Garamond',Georgia,serif;font-size:9.5px;font-weight:700;font-style:normal;"
    "color:var(--ad,#976e09);letter-spacing:0.35px;line-height:1.2;"
)

VOW_THE = (
    "font-family:'EB Garamond',Georgia,serif;font-size:11.5px;font-weight:700;font-style:italic;"
    "color:var(--ad,#976e09);letter-spacing:0.5px;line-height:1;"
)

# Center spine width — index chips and die slots share this column.
SPINE_W = "22px"

ROW_INDEX = (
    '<span class="vow-ix" style="flex-shrink:0;width:{w};height:12px;padding:0;'
    "display:inline-flex;align-items:center;justify-content:center;"
    "font-family:system-ui,-apple-system,sans-serif;font-size:8.5px;font-weight:800;"
    "color:#fffef8;background:var(--a,#B8860B);border-radius:3px;"
    'line-height:1;box-shadow:0 0 0 0.5px var(--ad,#976e09);">{n}</span>'
)

DIE_TARGET = (
    '<span class="die-target" style="flex-shrink:0;width:22px;height:22px;'
    "border:1.5px dashed rgba(184,134,11,0.55);border-radius:5px;"
    'background:rgba(255,252,245,0.65);display:inline-block;"></span>'
)

VOW_PHRASE = (
    '<div class="vow-phrase" style="border:1px dotted rgba(184,134,11,0.55);border-radius:10px;'
    'padding:2px 4px 3px;margin:0;">{inner}</div>'
)

KW_SM = (
    "font-size:7.9px;padding:0 2px;border-radius:2px;line-height:1.35;"
    "vertical-align:baseline;font-weight:700;"
)

ENTER_VOW = (
    "At <strong>Scene start</strong>: roll 2d6 to determine your new <strong>Vow</strong>:"
)

FULFILL_VOW = (
    "When an <strong>Action</strong> fulfills your <strong>Vow</strong>, add these dice to "
    '<span class="kw kw-boost" style="' + KW_SM + '">Boost</span> the roll.'
)

DEFIANCE_LABEL = (
    '<span style="font-family:system-ui,-apple-system,sans-serif;font-size:'
    + BODY_FONT_SM
    + ";"
    "letter-spacing:0.6px;text-transform:uppercase;color:#5a4020;font-weight:800;"
    '">Defiance:</span>'
)

BREAK_VOW = (
    DEFIANCE_LABEL
    + " Describe how you are defying your <strong>Vow</strong> and place these dice into your "
    '<span class="kw kw-resolve" style="' + KW_SM + '">Resolve</span>. The GM gains '
    '<span class="kw kw-toll" style="' + KW_SM + '">Toll 2</span> to use against you.'
)

BODY_STYLE = "gap:2px;padding:2px 9px 28px;"
TEMPLATE_BODY_STYLE = "gap:2px;padding:2px 8px 28px;"
WRITEIN = (
    '<div class="writein-line" style="flex:1;min-height:15px;'
    'border-bottom:1px dashed rgba(184,134,11,0.45);"></div>'
)


def _hdr_name(name: str = "", *, blank: bool = False) -> str:
    if blank:
        title = (
            '<span class="hdr-title" style="flex:1;min-width:0;min-height:14px;'
            'border-bottom:1px dashed rgba(90,74,32,0.35);margin-right:4px;">&nbsp;</span>'
        )
        return (
            '<div class="hdr-name hdr-bar">'
            + OATH_OF_PREFIX
            + title
            + "</div>"
        )
    return (
        '<div class="hdr-name hdr-bar">'
        + OATH_OF_PREFIX
        + f'<span class="hdr-title">{name}</span></div>'
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
    style = f"font-size:{BODY_FONT};line-height:1.45;text-align:left;{extra_style}"
    return f'<div class="effect-text" style="{style}">{content}</div>'


def etxt_break(content: str) -> str:
    style = f"font-size:{BODY_FONT_SM};line-height:1.45;color:#1a1008;text-align:left;"
    return f'<div class="effect-text" style="{style}">{content}</div>'


def _row_index(n: int, *, width: str = SPINE_W) -> str:
    return ROW_INDEX.format(n=n, w=width)


def _ornate_the() -> str:
    """Weighty center pivot — fleur-de-lis caps on a golden ring."""
    return (
        '<span class="vow-the-ring" style="position:relative;display:inline-flex;'
        "align-items:center;justify-content:center;min-width:28px;min-height:16px;"
        "padding:1px 7px 2px;border:1.5px solid var(--a,#B8860B);border-radius:14px;"
        "background:linear-gradient(180deg,rgba(255,252,245,0.95),rgba(247,240,224,0.55));"
        "box-shadow:inset 0 0 0 0.5px rgba(184,134,11,0.35),0 0 0 1px rgba(184,134,11,0.12);"
        'flex-shrink:0;">'
        '<span style="position:absolute;top:-5px;left:50%;transform:translateX(-50%);'
        "font-size:7px;line-height:1;color:var(--ad,#976e09);opacity:0.9;"
        'pointer-events:none;">⚜</span>'
        f'<span style="{VOW_THE}">the</span>'
        '<span style="position:absolute;bottom:-5px;left:50%;transform:translateX(-50%) scaleY(-1);'
        "font-size:7px;line-height:1;color:var(--ad,#976e09);opacity:0.9;"
        'pointer-events:none;">⚜</span>'
        "</span>"
    )


def _term_cell(word: str | None, *, side: str, blank: bool) -> str:
    term = WRITEIN if blank else f'<span style="{VOW_TERM}">{word}</span>'
    justify = "flex-end" if side == "verb" else "flex-start"
    return (
        f'<div class="vow-row" style="display:flex;align-items:center;justify-content:{justify};'
        f'min-height:13px;padding:0;width:100%;">{term}</div>'
    )


def _indexed_row(
    n: int,
    word: str | None,
    *,
    side: str,
    align: str,
    blank: bool,
) -> str:
    """side: verb | noun. align: outward (default) | meet (verbs→right, nouns→left)."""
    gap = "gap:5px;"
    base = f"display:flex;align-items:center;{gap}min-height:14px;padding:1px 0;width:100%;"
    term = WRITEIN if blank else f'<span style="{VOW_TERM}">{word}</span>'
    ix = _row_index(n, width="12px")

    if align == "meet" and side == "verb":
        style = base + "justify-content:flex-end;"
        inner = term + ix
    elif align == "meet" and side == "noun":
        style = base + "justify-content:flex-start;"
        inner = ix + term
    else:
        style = base + "justify-content:flex-start;"
        inner = ix + term

    return f'<div class="vow-row" style="{style}">{inner}</div>'


def _word_stack_meet(
    *,
    blank: bool = False,
    verbs: list[str] | None = None,
    nouns: list[str] | None = None,
) -> str:
    """L→R mad lib — one shared grid so dice columns track with index columns."""
    grid = (
        "display:grid;"
        "grid-template-columns:minmax(0,1fr) 22px minmax(26px,auto) 22px minmax(0,1fr);"
        "column-gap:4px;row-gap:0;align-items:center;"
    )
    cells = [
        "<div></div>",
        f'<div style="display:flex;justify-content:center;">{DIE_TARGET}</div>',
        f'<div style="display:flex;justify-content:center;">{_ornate_the()}</div>',
        f'<div style="display:flex;justify-content:center;">{DIE_TARGET}</div>',
        "<div></div>",
        '<div style="grid-column:1/-1;border-top:1px dotted rgba(184,134,11,0.4);'
        'height:0;margin:1px 0 0;padding:0;"></div>',
    ]
    vlist = verbs or []
    nlist = nouns or []
    for i in range(6):
        n = i + 1
        cells.extend(
            [
                _term_cell(None if blank else vlist[i], side="verb", blank=blank),
                f'<div style="display:flex;justify-content:center;">{_row_index(n)}</div>',
                "<div></div>",
                f'<div style="display:flex;justify-content:center;">{_row_index(n)}</div>',
                _term_cell(None if blank else nlist[i], side="noun", blank=blank),
            ]
        )
    inner = f'<div class="vow-grid" style="{grid}">{"".join(cells)}</div>'
    return VOW_PHRASE.format(inner=inner)


def word_stack(
    *,
    blank: bool = False,
    verbs: list[str] | None = None,
    nouns: list[str] | None = None,
    align: str = "meet",
) -> str:
    """L→R mad lib — dice in top slots; numbered verb/noun columns below."""
    if align == "meet":
        return _word_stack_meet(blank=blank, verbs=verbs, nouns=nouns)

    phrase_top = (
        '<div class="vow-skeleton" style="display:flex;align-items:center;justify-content:center;'
        'gap:10px;margin:0 0 3px;padding:0;">'
        + DIE_TARGET
        + f'<span style="{VOW_THE}">the</span>'
        + DIE_TARGET
        + "</div>"
    )
    vlist = verbs or []
    nlist = nouns or []
    rows = (
        '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0 12px;align-items:baseline;">'
        + "".join(
            f'<div>{_indexed_row(i + 1, None if blank else vlist[i], side="verb", align=align, blank=blank)}</div>'
            f'<div>{_indexed_row(i + 1, None if blank else nlist[i], side="noun", align=align, blank=blank)}</div>'
            for i in range(6)
        )
        + "</div>"
    )
    inner = (
        phrase_top
        + '<div class="vow-lr-columns" style="border-top:1px dotted rgba(184,134,11,0.4);padding-top:3px;">'
        + rows
        + "</div>"
    )
    return VOW_PHRASE.format(inner=inner)


def _patron_mark_grid() -> str:
    """Six blank mark slots for Warlock patron template (3×2)."""
    cells = []
    for i in range(6):
        n = i + 1
        cells.append(
            '<div style="display:flex;align-items:center;gap:3px;padding:1px 0;">'
            + _row_index(n, width="12px")
            + '<div class="writein-line" style="flex:1;min-height:14px;'
            'border-bottom:1px dashed rgba(184,134,11,0.4);"></div></div>'
        )
    return (
        '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
        'gap:3px 4px;margin:2px 0;">'
        + "".join(cells)
        + "</div>"
    )


def _break_section() -> str:
    return (
        '<div class="rule" style="margin:4px 0 2px;"></div>'
        + etxt_break(BREAK_VOW)
    )


def _body_block(
    *,
    blank: bool = False,
    verbs: list[str] | None = None,
    nouns: list[str] | None = None,
    align: str = "outward",
) -> str:
    return (
        etxt(ENTER_VOW, extra_style="margin-bottom:2px;")
        + word_stack(blank=blank, verbs=verbs, nouns=nouns, align=align)
        + '<div class="rule" style="margin:3px 0 2px;"></div>'
        + etxt(FULFILL_VOW)
    )


def _hdr(*, name: str = "", sub: str = "", blank: bool = False, include_sub: bool = False) -> str:
    sub_html = _hdr_sub(sub, blank=blank) if include_sub else ""
    return (
        '<div class="hdr">'
        + HDR_TOP
        + _hdr_name(name, blank=blank)
        + sub_html
        + "</div>"
    )


def build(oath: dict, *, include_break: bool = True, phrase_align: str = "meet") -> str:
    return (
        '<div class="card paladin acc-paladin">'
        + _hdr(name=oath["name"])
        + f'<div class="card-body" style="{BODY_STYLE}">'
        + _body_block(verbs=oath["verbs"], nouns=oath["nouns"], align=phrase_align)
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
        + _patron_mark_grid()
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
