---
name: at-playtest-analysis
description: Instinct RPG playtest post-processing — transcript to design checklist + Discord recap. Run after any playtest when Annie/Nathan provides session transcript(s) (p1 gameplay + p2 debrief, or single file). Triggers on "playtest analysis," "post-playtest," "process the transcript," "design checklist from playtest," or when new files appear under Playtest Info & Feedback/. Produces a tiered action checklist and a paste-ready Discord newsletter post.
---

# Instinct RPG — Playtest Post-Processing Analysis

Turn raw playtest transcript(s) into **two deliverables** Annie can ship from immediately:

1. **`[date] Playtest Analysis & Design Checklist.md`** — tiered design backlog + verification pass
2. **`[date] Discord Recap Post.md`** — story-first newsletter for the playgroup

**Agent runs end-to-end.** Do not hand scripts or partial summaries to Annie.

---

## Inputs

| Source | Use for |
|---|---|
| **Transcript p1** | Primer self-teaching, player Q&A, chargen, core gameplay, story beats, Nathan's on-the-fly rulings |
| **Transcript p2** | Debrief, reflections, design discussion, scope statements from Nathan |
| **Existing doctrine** (`design/`) | Map findings to real homes; don't invent rules |
| **Prior playtest checklist** (if any) | Continuity — what shipped vs what's still open |

Transcripts live under `Playtest Info & Feedback/[session folder]/`.

---

## Agent role

You are a **playtest analyst and design PM**, not a transcript summarizer.

- Apply **focus-group / usability-testing best practices** adapted for tabletop playtests: separate observation from interpretation; triangulate across speakers; weight recurring themes; flag contradictions; preserve dissent.
- **Nathan's statements = scope authority.** When the designer speaks, treat his goals, intent, and stated focus boundaries as accurate. Distinguish:
  - **Committed direction** — "I'm going to…" / "that's what I'm doing next"
  - **Scope lock** — "not this week" / "banish until Playtest N+"
  - **Brainstorm** — ideas tossed around without commitment → **Parked ideas** section
- **Infer Nathan's primary focus** for the next week from his debrief + repeated emphasis. Tier everything else Secondary or Tertiary. **Show inferences for verification** — Annie corrects before doctrine edits.
- **North star:** ship a DriveThruRPG-ready product that works for **players and GMs**. Every recommendation should trace to table feel, teachability, or production clarity.

---

## Deliverable 1 — Analysis & Design Checklist

**Filename:** `[Mon DD] Playtest Analysis & Design Checklist.md`  
**Session header:** date, players (player name → character → class), format (one-shot, player count, mid-session joins).

### Required section order

1. **HOW TO USE THIS DOCUMENT** — tiers, checkboxes, one-line purpose
2. **WHAT'S WORKING — DO NOT BREAK THESE** — strengths first; changes must enhance, not dismantle
3. **PRIMARY CHANGES — DO THIS BEFORE NEXT PLAYTEST** — high-confidence, often multi-player corroboration, clear fix; include **The problem** / **The fix** / **What to preserve** / downstream notes / draft card or rule language where useful
4. **SECONDARY CHANGES — NEXT SPRINT** — strong merit, not urgent for next session
5. **TERTIARY — GREAT IDEAS, DO NOT TOUCH YET** — real gold, explicit distraction ban
6. **PARKED IDEAS (UNRESOLVED BRAINSTORM)** — tossed in debrief, not committed; Nathan or table floated but no ship decision
7. **OPEN DESIGN QUESTIONS** — consciously unresolved; no fake answers
8. **ON-THE-FLY RULINGS & ERRATA** — mid-session GM calls that should become canon or be reverted
9. **PRIMER / TEACHABILITY NOTES** — what players taught themselves from the primer; what they asked each other; what's unclear
10. **AGENT INFERENCES — VERIFY WITH NATHAN** — bullet list: "I think your primary focus this week is X because…" Annie checks/corrects
11. **QUOTES TO REMEMBER** — attributed player voice; design-useful phrasing
12. **WHAT TO ACTUALLY DO [NEXT WORK BLOCK]** — ruthlessly narrowed numbered list (≈5–8 items max); "that's a week's work"

### Tiering rules

| Tier | Criteria |
|---|---|
| **Primary** | Multiple players OR Nathan committed in debrief; clear solution; blocks next playtest quality if ignored |
| **Secondary** | High design value; needs more design or a dedicated test |
| **Tertiary** | Future-scope; explicitly "banish from brain until Playtest N+" |
| **Parked** | Discussed, not decided; document so it isn't lost |

### Item anatomy (Primary / Secondary)

```markdown
### [ ] P# — Short title

**The problem:** …
**The fix:** …
**What to preserve:** … (optional)
**Draft language:** … (optional)
```

Use checkboxes `[ ]` throughout. Annie edits in place.

### Rhetoric filters (from Nathan's session-open framing)

Prefer player feedback shaped as:
- *"I was expecting X, but got Y — and that was good/bad"*
- *"It feels cool to Z" / "It doesn't feel great that A"*
- *"Follow the fun"* — would they run it again? Refer it? Pull it off the shelf for new people?

Deprioritize balance nitpicks at early playtest stages unless something breaks the session.

---

## Deliverable 2 — Discord Recap Post

**Filename:** `[Mon DD] Discord Recap Post.md`  
**Tone:** Entertaining, appreciative, players feel **heard**. Paste-ready — Annie adds personal open/close only.

### Required structure (order matters)

1. **Hook + thanks** — emoji-friendly, warm, acknowledges their time
2. **THE STORY (episode recap)** — BEFORE feedback:
   - Name every PC (player attribution when known)
   - TV-episode synopsis: major beats, funniest/wildest moments, climax
   - Character voice where possible
3. **WHAT WE DISCUSSED (design takeaways)** — distill debrief; attribute speakers when identifiable; **actionable takeaways** as bold talking points so feedback visibly shaped next steps
4. **Optional:** soft invite to Discord design channel / next playtest

Do **not** lead with rules changes — story first, then "you were heard."

Identify speakers from transcript; if ambiguous, note `[verify: speaker?]` or ask Annie one MC question.

---

## Workflow (sequencing)

1. **Read both transcript parts fully** (or note if debrief is embedded in p1)
2. **Extract observation ledger** (silent): story, rulings, player confusion, Nathan scope statements, tossed ideas
3. **Draft checklist** — strengths → tiers → parked → open → inferences → quotes → Monday list
4. **Draft Discord post** — story recap → feedback distilled
5. **Present to Annie** — link both files; highlight **AGENT INFERENCES** for verification
6. **After Annie confirms** — map Primary items to `design/` via `at-session-close`; do not edit doctrine from unverified inferences alone

---

## What NOT to do

- Don't dump a prose essay — checklist + paste-ready Discord only
- Don't collapse Parked and Tertiary — parked = undecided; tertiary = decided to defer
- Don't omit primer/teachability — self-teaching is a core test goal
- Don't treat player balance suggestions as Primary unless they match feel-level feedback or Nathan agrees
- Don't skip Nathan's on-the-fly rulings — they're often the real canon for that session

---

## Repo layout

```
Playtest Info & Feedback/
  June 20th (#2)/
    Jun 20 playtest and feedback p1.txt
    Jun 20 playtest and feedback p2.txt
    Jun 20 Playtest Analysis & Design Checklist.md
    Jun 20 Discord Recap Post.md
  June 30th (#3)/
    Instinct Playtest Jun 30 (p1).txt
    Instinct Playtest Jun 30 (p2).txt
    … (analysis outputs after processing)
```

---

## Related

- Player-facing tone (primer copy): `instinct-playtest-tone.mdc`
- Doctrine sync after verified changes: `at-session-close`
- Collaboration MC: `instinct-collaboration.mdc`
