#!/usr/bin/env python3
"""Paladin Oath phrase-zone layout variants (exploration / proof)."""
from __future__ import annotations

from scripts.build_oath_html import (
    BODY_STYLE,
    BREAK_VOW,
    ENTER_VOW,
    FULFILL_VOW,
    KW_SM,
    OATHS,
    THE_DIVIDER,
    VOW_PHRASE,
    VOW_TERM,
    _break_section,
    _hdr,
    etxt,
    etxt_break,
)

# Neutral die target — index layer only (Rec 2 / shared).
DIE_NEUTRAL = (
    '<span class="die-slot die-slot-neutral" style="flex-shrink:0;width:15px;height:15px;'
    "display:flex;align-items:center;justify-content:center;font-size:7px;font-weight:600;"
    "color:#5a4020;border:1px solid rgba(90,74,32,0.42);border-radius:3px;"
    'background:rgba(255,252,248,0.85);line-height:1;">{n}</span>'
)

VOW_TERM_SPAN = f'<span class="vow-term" style="{VOW_TERM}">{{word}}</span>'


def _term(word: str) -> str:
    return VOW_TERM_SPAN.format(word=word)


def word_stack_current(*, blank: bool = False, verbs: list[str] | None = None, nouns: list[str] | None = None) -> str:
    """v6b production layout (reference)."""
    from scripts.build_oath_html import word_stack

    return word_stack(blank=blank, verbs=verbs, nouns=nouns)


def word_stack_columns(*, verbs: list[str], nouns: list[str]) -> str:
    """Rec 1 — three vertical column strips; die + word stacks, no per-cell boxes."""
    cols = []
    for i in range(3):
        cols.append(
            '<div class="vow-col" style="flex:1;display:flex;flex-direction:column;align-items:center;'
            'gap:2px;min-width:0;padding:0 2px;">'
            + DIE_NEUTRAL.format(n=i + 1)
            + _term(verbs[i])
            + DIE_NEUTRAL.format(n=i + 4)
            + _term(verbs[i + 3])
            + "</div>"
        )
    verb_band = (
        '<div style="display:flex;align-items:flex-start;gap:2px;width:100%;">'
        + "".join(cols)
        + "</div>"
    )
    noun_cols = []
    for i in range(3):
        noun_cols.append(
            '<div class="vow-col" style="flex:1;display:flex;flex-direction:column;align-items:center;'
            'gap:2px;min-width:0;padding:0 2px;">'
            + DIE_NEUTRAL.format(n=i + 1)
            + _term(nouns[i])
            + DIE_NEUTRAL.format(n=i + 4)
            + _term(nouns[i + 3])
            + "</div>"
        )
    noun_band = (
        '<div style="display:flex;align-items:flex-start;gap:2px;width:100%;">'
        + "".join(noun_cols)
        + "</div>"
    )
    inner = verb_band + THE_DIVIDER + noun_band
    return VOW_PHRASE.format(inner=inner)


def _layered_cell(n: int, word: str) -> str:
    return (
        '<div class="vow-cell" style="display:flex;align-items:center;gap:3px;min-width:0;padding:1px 0;">'
        + DIE_NEUTRAL.format(n=n)
        + f'<span style="{VOW_TERM}flex:1;text-align:left;padding-right:2px;">{word}</span>'
        + "</div>"
    )


def word_stack_layered(*, verbs: list[str], nouns: list[str]) -> str:
    """Rec 2 — same 3×2 grid; neutral die targets; language only, no inner boxes."""
    def grid(words: list[str]) -> str:
        cells = "".join(_layered_cell(i + 1, words[i]) for i in range(6))
        return (
            '<div class="vow-grid" style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));'
            'gap:3px 4px;margin:2px 0;width:100%;">'
            + cells
            + "</div>"
        )

    inner = grid(verbs) + THE_DIVIDER + grid(nouns)
    return VOW_PHRASE.format(inner=inner)


def word_stack_skeleton(*, verbs: list[str], nouns: list[str]) -> str:
    """Rec 3 — ghost sentence skeleton, subordinate compact word field."""
    skeleton = (
        '<div class="vow-skeleton" style="display:flex;align-items:baseline;justify-content:center;'
        'gap:7px;margin:0 0 5px;padding:2px 0 4px;">'
        f'<span style="{VOW_TERM}font-size:9px;opacity:0.32;letter-spacing:1px;">____</span>'
        f'<span style="{VOW_TERM}font-size:8.5px;">the</span>'
        f'<span style="{VOW_TERM}font-size:9px;opacity:0.32;letter-spacing:1px;">____</span>'
        "</div>"
    )
    muted = (
        "font-family:'EB Garamond',Georgia,serif;font-size:6.5px;font-weight:600;font-style:italic;"
        "color:rgba(151,110,9,0.72);letter-spacing:0.15px;line-height:1.1;"
    )

    def field_row(words: list[str], start_n: int) -> str:
        cells = []
        for i in range(3):
            n = start_n + i
            cells.append(
                '<div style="display:flex;align-items:center;gap:2px;min-width:0;">'
                + DIE_NEUTRAL.format(n=n)
                + f'<span style="{muted}">{words[i]}</span></div>'
            )
        return '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px 3px;">' + "".join(cells) + "</div>"

    word_field = (
        '<div class="vow-field" style="opacity:0.95;">'
        + field_row(verbs[:3], 1)
        + field_row(verbs[3:], 4)
        + THE_DIVIDER
        + field_row(nouns[:3], 1)
        + field_row(nouns[3:], 4)
        + "</div>"
    )
    inner = skeleton + word_field
    return VOW_PHRASE.format(inner=inner)


def _body_block_variant(
    layout: str,
    *,
    verbs: list[str],
    nouns: list[str],
) -> str:
    stacks = {
        "current": word_stack_current,
        "columns": word_stack_columns,
        "layered": word_stack_layered,
        "skeleton": word_stack_skeleton,
    }
    stack_fn = stacks[layout]
    if layout == "current":
        phrase = stack_fn(verbs=verbs, nouns=nouns)
    else:
        phrase = stack_fn(verbs=verbs, nouns=nouns)
    return (
        etxt(ENTER_VOW, extra_style="margin-bottom:1px;")
        + phrase
        + '<div class="rule" style="margin:4px 0 2px;"></div>'
        + etxt(FULFILL_VOW)
    )


def build_variant(oath: dict, layout: str) -> str:
    return (
        '<div class="card paladin acc-paladin">'
        + _hdr(name=oath["name"], sub=oath["sub"])
        + f'<div class="card-body" style="{BODY_STYLE}">'
        + _body_block_variant(layout, verbs=oath["verbs"], nouns=oath["nouns"])
        + _break_section()
        + '</div><div class="idtag">Paladin</div></div>'
    )


OPEN_HAND = OATHS[0]

LAYOUTS = [
    ("columns", "Rec 1 — Column strips", "Three vertical columns; die targets stack above words; no cell boxes."),
    ("layered", "Rec 2 — Two-layer grid", "Same 3×2 grid; neutral die squares; phrase words only (no inner chrome)."),
    ("skeleton", "Rec 3 — Sentence skeleton", "Ghost ____ the ____ line first; word bank subordinate below."),
]

if __name__ == "__main__":
    for key, _, _ in LAYOUTS:
        print(key, len(build_variant(OPEN_HAND, key)))
