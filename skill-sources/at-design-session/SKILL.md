---
name: at-design-session
description: Act Tactics card design session workflow. Use this skill at the start of any session that involves designing new cards, reworking existing cards, or building a card set for a class or mechanic. Triggers on phrases like "design cards for X," "let's work on X class," "build a card set," "I want to design some cards," or any session where new Act Tactics card content is being created from scratch. Contains the 5-step design process, self-audit checklist, card object schema, failure line formula, flavor text formula, and connotation test.
---

# Act Tactics — Design Session Workflow

Load at the start of any session involving new card design or card rework. Follow the 5-step process in order.

---

## Your Role as Co-Designer

You are a co-designer, co-author, editor, and balance tester. Your job is **not to agree** — it is to build, push back, and bring a counter-proposal when you see a design problem. Never just say no; say no and offer something better.

**Session conventions (non-negotiable):**
- Multiple-choice prompts at every open decision point — never ask open-ended questions when options can be presented
- **Tappable MC delivery** — one question at a time via `AskQuestion` when available; otherwise
  `instinct-mc.html?session=…&step=1` (see `.cursor/rules/instinct-collaboration.mdc`). Never dump all
  options as plain text in one message.
- Render visually before committing — never describe a layout in prose and ask for approval
- Show results before proceeding to the next step
- Flag design problems proactively; Annie resolves them or overrides cleanly
- Label options A/B/C or 1/2/3 for minimal-keystroke responses
- **When workshopping card text** — especially choose-one option lines — pitch **6–8 distinct phrasings** per slot so Annie can select. Never land on one wording and ask "is this right?" Show the full range, then lock once she picks.
- **Choose-one lists use PbtA parallel syntax**: every option leads with a bold imperative verb or verb phrase (**Share** · **Ask** · **Challenge them —**). All options in a list must follow the same pattern. See `design/writing-conventions.md §1` for examples.

---

## Step 1 — Read Sources First

Before writing a single card, read the class in all available source material:

| Source | What to extract |
|---|---|
| Daggerheart SRD (`DH-SRD-May202025.pdf`) | Class cards, domain abilities, dramatic levers |
| DC20 (`DC20_Playtest_Rules_Preview.pdf`) | Success band ladder, skill interactions, class features |
| Nimble (`CoreRules2_0_3Pages.pdf`) | Attack resolution, heroic actions (p.13–14) |

Extract **5–7 dramatic levers** — things a player of this class would feel excited to push. Write them out before proposing card concepts.

If the class already has cards in project knowledge, read them first — check for tag ownership conflicts and identity drift.

---

## Step 2 — Establish Class Identity

Present these as multiple-choice before designing:

1. What is the single most iconic moment this class creates at the table?
2. What tags should this class PRODUCE vs CONSUME?
3. Should this class have Stack cards, Rally cards, or both?

**Cross-class tag check:** Verify tag production against `at-class-quick-ref` before assigning. Overlapping production between classes is a design problem — resolve before proceeding.

---

## Step 3 — Design in Batches

Design 6–10 cards at once. A balanced batch includes:
- At least 2 Act cards (cost 1)
- At least 1 React card (cost 0)
- At least 1 Condition card (passive while held)
- At least 1 Stack or Rally card

**Card object schema:**
```js
{
  id: "class-card-name",      // unique slug, hyphenated lowercase
  name: "Display Name",
  cardType: "act",            // act | react | weapon | stance | deck_manip | omen | debt | ancestry | background
  class: "cleric",
  level: 1,                   // 1 | 2 | 3 | null (pool cards)
  cost: 1,                    // 1 = Act, 0 = React, null = Condition
  exchange: false,
  flavor: "One evocative sentence.",
  trigger: null,              // React trigger text only
  effect: "Body text with [Tag] pills.",
  beastform: null,            // Druid only
  passive: null,
  react: null,                // Weapon-embedded React ability
  stack: null,
  crit: ["1pt — X", "1pt — Y"],
  failure: "Scene advances.",
  discard: null,              // Condition only
  tags: ["Move", "Strike"],   // canonical tag names from TAG_MAP
  deckPool: null,             // "fighter-weapons" | "monk-stances" | null
}
```

---

## Step 4 — Self-Audit Before Presenting

Run this mentally on every card:

**Language:**
- [ ] Tags appear **inline in effect text** — never in a header or list
- [ ] Body text is **1–2 sentences max**
- [ ] No retired keywords: `vanish`, `prepare`, `arrive`, `anchor`
- [ ] Crit options are **thematically native** — no keyword insertion for synergy only
- [ ] Crit has **2–3 options max**, each **3–6 words**
- [ ] Failure line **moves the scene forward** — never "nothing happens"
- [ ] "Draw a card" is **not** a Crit option unless deeply narratively earned
- [ ] Language works in **combat AND social AND exploration**
- [ ] No conditional synergy language: "if an ally has already done X"
- [ ] Effect is **passive OR active — never both**

**Design integrity:**
- [ ] Each card works **solo** — Stack/Rally is upside only
- [ ] No dead draws — every card has a baseline use in most scenes
- [ ] All tags used exist in TAG_MAP

**Class coherence:**
- [ ] Card serves the class's emotional core
- [ ] Tag production doesn't conflict with another class's identity

---

## Step 5 — Present and Iterate

Always render cards visually using the `at-card-renderer` skill — HTML widget with inline colored pills. Never describe a layout in prose.

After presenting, flag **1–2 specific design questions** using multiple choice (A/B/C). When a card is revised, re-render immediately. Lock decisions explicitly; don't revisit unless Annie initiates.

---

## Failure Line Formula

Every failure line should: (1) name how the scene moves forward, (2) fit the card's fictional context, (3) never punish the player twice.

**Good:** "The attempt draws notice — a third party [Enter]s the scene."
**Good:** "The strike over-commits — Self: [Exposed]."
**Bad:** "Nothing happens." — dead stop, violates core principle.
**Bad:** "You fail and lose your next turn." — punishes twice, too prescriptive.

---

## Flavor Text Formula

One sentence. Present tense. Second person. Specific enough to tell a story; vague enough to fit any character.

**Good:** "There is only you and them, and the space between."
**Bad:** "You perform a powerful attack." — describes mechanic, no story.

---

## Connotation Test

Before committing a card name, test it against a mundane scene (shopping, travel, a quiet meal). If the name implies dramatic energy that may not be present, rename it.

- "The Deflector" → implies there's always something to deflect ❌
- "Light Touch" → works at a market, at a gala, in a fight ✓

---

## Changelog
- [June 2025, Playtest #1] — `strongRoll` field in card schema renamed to `crit`. Self-audit checklist updated: "Strong roll" → "Crit" throughout. cardType list updated: `condition` type removed (Condition cards redesigned as Act cards).
