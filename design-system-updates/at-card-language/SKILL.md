---
name: at-card-language
description: Instinct RPG card language, formatting, and writing consistency guide. ALWAYS load this skill alongside at-card-rework and at-design-session — it is a required companion to both. Also trigger whenever reviewing, auditing, or approving card text, or before any card is pushed to Baserow. Triggers on phrases like "write the card text," "how should I word this," "is this capitalized right," "edit the trigger line," "review the language," "check the wording," "audit this card," or any session where words are being placed on cards. Never finalize a card design without running the audit checklist in this skill.
---

# Instinct RPG — Card Language Guide

*Companion to at-card-rework and at-design-session. Run the audit checklist at the bottom before finalizing any card.*

---

## HOW THIS SKILL FITS INTO THE WORKFLOW

This skill runs as a final quality gate — after design work, before approval and Baserow push.

**When running at-design-session:**
1. Design cards normally using that skill's process
2. Before presenting cards for approval → run the **Term Audit Checklist** (end of this document) on each card
3. Fix any violations inline
4. Present the corrected card(s) for approval
5. Once approved → push to Baserow

**When running at-card-rework:**
1. Complete the rework using that skill's process
2. Before archiving old version and finalizing → run the **Term Audit Checklist**
3. Fix any violations
4. Then present for approval and push

**Quick rule:** No card text is final until it has passed the Term Audit. If you catch a violation during design, fix it immediately rather than noting it for later.

---

## FORMATTING TIERS

There are exactly two formatting tiers for game terms.

**Tier 1 — Effect Keywords (pill format)**
Countable or trackable mechanical effects. Always appear as inline colored pills: `[Term]` or `[Term N]`. Never write them as plain text.

**Tier 2 — Bold+Cap**
Named game terms, card types, conditions, and declared actions that carry mechanical meaning but aren't countable. Write as **Term** in all card text — bold AND title case.

Everything else is plain prose. New terms: if it can have a number → likely Tier 1. If the table recognizes it as a named thing → Tier 2. Otherwise, lowercase.

---

## TIER 1 — EFFECT KEYWORDS

The only authorized pills. Do not create new pill terms without explicit session approval.

| Keyword | Color (bg / text) | Notes |
|---|---|---|
| `[Boost N]` | `#0F766E` / `#CCFBF1` teal | Always include the number: [Boost 2], [Boost 1] |
| `[Crit]` | `#CA8A04` / `#FEFCE8` gold | Success threshold reward |
| `[Resolve]` | `#166534` / `#DCFCE7` green | Replaces retired term Guard |
| `[Hit Die]` / `[Hit Dice]` | `#6B21A8` / `#EDE9FE` purple | Match singular vs. plural to usage |
| `[Toll]` | `#5B0F6B` / `#F3E8FF` dark purple | GM resource; accumulates on any failed roll |
| `[Aid]` | `#0F766E` / `#CCFBF1` teal | Same color as Boost |

**Retired — do not use:**
- `[Guard]` → use `[Resolve]`
- `[Luck Check]` → use **Luck Check** (Bold+Cap, no pill)
- `[Strong Roll]` → use `[Crit]`

---

## TIER 2 — BOLD+CAP TERMS

Write all of the following as **Term** whenever they appear in any card text.

### Card Types
**Act** · **React** · **Core** · **Instinct** · **Background** · **Bond** · **Ancestry** · **Flaw** · **Bane** *(retired, still in design writing)*

### Declared Actions & Mechanics
**Action** · **Reaction** *(planned, not yet on cards)* · **Draw** · **Discard** · **Shuffle** · **Cleanse** · **Luck Check**

### Scene Terms
**Scene**

### Conditions *(all Bold+Cap whenever they appear)*
**Rattled** · **Exposed** · **Rooted** · **Hidden** · **Bolstered** · **Sundered** · **Break**

### Class Economy Terms
**Rally** · **Notoriety** *(Rogue)* · **Performance** *(Bard)* · **Debt** *(Warlock)*

*Class economy terms for other classes will be added as those classes are designed.*

---

## SPECIAL RULES

| Term | Rule |
|---|---|
| GM | Always abbreviated — never write "Game Master" |
| beat | Lowercase — informal time language, not a game term |
| Pact | A card name, not a game term — no special formatting |
| Card-specific nouns | Bold+Cap on that card only (e.g., "Nature" on a Druid card) — do not add to this glossary unless the term becomes cross-card |

---

## CARD ANATOMY — SECTION NAMES & PURPOSES

Use these exact names when referring to card sections in design work.

### Ability Cards (Act / React / Core)

| Section | Purpose | Writing rule |
|---|---|---|
| **Flavor Text** | Evoke the emotional/fictional core | 2nd person, present tense, 1 sentence. Not on every card — only when the card has a distinct identity that earns framing |
| **Trigger** | Set the fictional gate for using the card | Italic conditional clause. Soft gate — fiction-first, not mechanical. Must fire in 4+ scene types |
| **Effect** | Main mechanical or fictional outcome | CRPG verb format for choose-one options. Hint at direction, never prescribe outcomes |
| **Crit** | Bonus for a critical success | Only when the card's fiction deeply earns it. 3–6 words per option, 2–3 options max |
| **Discard** | Condition or benefit for discarding the card | One short clause |

### Character Creation Cards

| Section | Card types | Purpose | Writing rule |
|---|---|---|---|
| **Flavor Text** | All except Instinct | Emotional core of the card | 2nd person, present tense, 1 sentence |
| **Universal Flavor** | Instinct only | Shared across all Instinct cards | Fixed text — the word in the header IS the personality |
| **Effect Line** | Instinct, Bond | What happens when revealed or activated | |
| **Trigger** | Background, Ancestry, Flaw | Fictional gate for activation | Same soft-gate rules as ability cards |
| **Body** | Background, Ancestry | Choose-one / luck-check / passive-question | Match the correct body type pattern for the card |
| **Origin Stem** | All character creation cards | Prompt a specific backstory memory | 1st person, past tense, incomplete sentence with `___`. Unique per card — never generic |
| **Writing Lines** | All character creation cards | Space for player to write their memory | Blank lines below Origin Stem |
| **Fill-in Stem** | Flaw only | Player sets their specific trigger at creation | Format A: `___ sets me off.` / Format B: `I won't back down when ___` |
| **Dismiss Condition** | Flaw only | How to remove the Flaw | Always two paths: act on it OR an ally **Cleanses** it |

---

## WRITING PRINCIPLES (priority order)

**1. Brevity.** If a word can be removed without losing meaning, remove it. Cards are read mid-play.

**2. Syntactic parallelism.** If two cards use the same construction, they must read the same way. "Gain [Boost 2] for the Action" on one card means you don't write "earn a [Boost 2] bonus" on another.

**3. User-centric.** Write for the player holding the card. "You" = direct and present. "Your character" = deliberate narrative distance (use intentionally, not by default).

**4. No ambiguity.** If a player could misread the card two ways, rewrite it. The GM should never need to resolve a wording dispute.

**5. No negation-passive.** Never: "you cannot," "you are immune," "you are not." Always reframe as an active state or advantage.

**6. "This Scene" not "the scene ahead."** The hand is who the character is *right now*.

**7. No designer-speak.** Never: "the fiction advances," "narratively," "mechanically speaking," "spotlight."

---

## TERM AUDIT CHECKLIST

Run this on every card before approval or Baserow push. Fix violations immediately.

- [ ] All Effect Keywords formatted as pills — not plain text (e.g., not "Boost 2" but `[Boost 2]`)
- [ ] All Bold+Cap terms actually bolded and title-cased
- [ ] "action" → **Action**, "scene" → **Scene** (no lowercase)
- [ ] No retired terms: no `[Guard]`, no `[Strong Roll]`, no `[Luck Check]` pill
- [ ] "GM" not "Game Master"
- [ ] "beat" lowercase
- [ ] Section names match canonical anatomy above
- [ ] Syntactic parallelism — compare phrasing to similar cards in the same deck
- [ ] Brevity pass — any words that can be cut?
- [ ] No negation-passive language
- [ ] No designer-speak
- [ ] "this scene" not "the scene ahead"

---

## KNOWN CARDS FLAGGED FOR UPDATE

Current cards using the old lowercase standard for terms now locked as Bold+Cap:

- **action → Action**: 11 current cards — update on next rework pass
- **scene → Scene**: 21 current cards — update on next rework pass

*(Legacy cards using "Strong Roll" are marked legacy status — do not update unless reviving a card.)*

---

## Changelog
- [June 2026] — Created. Term list vetted against 285 of 385 Baserow cards (page 3 not retrieved — Fighter and Bard decks may have additional terms to add on next session).
