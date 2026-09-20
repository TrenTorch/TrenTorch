---
name: agentic-guardrails-llm-judge-harness
title: An LLM-as-Judge Harness for Agent Transcripts
tags: [agentic-systems, guardrails, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A real LLM-as-judge sends the whole transcript to a model with a scoring rubric and asks it to grade the run. To make this exercise deterministic and checkable without touching a model — the same philosophy as the `accuracy(r)` simulator in *Reproduce "Lost in the Middle" and Compare Orderings* — you're given a *deterministic* stand-in: a rubric of text patterns, each worth some number of points (positive or negative), and the job is computing the score a judge following that exact rubric mechanically would produce.

### From theory to code

You're given `transcript` (`(role, text)` turns making up one agent run, in order) and `rubric` (a substring pattern mapped to a point value, which may be negative). Implement `score_transcript(transcript, rubric)`. For each turn's text, add every rubric pattern's point value to a running total if that pattern appears anywhere in that turn's text — each pattern counts **at most once per turn**, even if it appears multiple times within that turn's text.

Return the total score across the whole transcript.

### Constraints

- 0 to 200 turns; 0 to 50 rubric patterns; matching is case-sensitive, plain substring.

### Hints

<details>
<summary>Hint 1</summary>

For each turn, loop over every rubric pattern once and check `pattern in text` — a plain `in` check naturally only tells you "does it appear," not "how many times," which is exactly the "at most once per turn" rule this problem wants.

</details>

<details>
<summary>Hint 2</summary>

Negative point values need no special handling — `total += points` works identically whether `points` is positive or negative, since addition already does the right thing either way.

</details>

## Theory

### The simple version

Walk every turn, and for every rubric pattern, add its points to a running total if that pattern shows up anywhere in that turn's text. Repeat for every turn. The total at the end is the transcript's score.

### Why "at most once per turn," not "once per occurrence"

A rubric pattern like `"error"` showing up three times in one turn's text usually signals the same underlying problem repeated in the model's own phrasing, not three independent failures — counting it once per turn (rather than once per occurrence) keeps the score reflecting *how many distinct problems this turn had*, not *how verbosely the model happened to restate the same one*.

### How this shows up in real systems

A deterministic, pattern-based rubric like this one is often the *first* evaluation layer teams build before investing in a real model-based judge — it's free to run, completely reproducible, and good enough to catch obvious cases (an apology, an explicit error message, a completion signal) while a genuine LLM judge is reserved for the more nuanced quality judgments a keyword rubric can't capture.

## Explanation

The function walks `transcript` with a nested loop: for each turn, it checks every rubric pattern with a plain `in` substring test against that turn's text, adding the pattern's point value to a running `total` on a match. Because the inner loop runs once per `(turn, pattern)` pair — not once per occurrence of the pattern within the text — a pattern appearing multiple times in one turn's text still only ever contributes its points once for that turn, which is exactly the "at most once per turn" rule. Negative point values need no special-casing, since `total += points` correctly decreases the total for a negative `points` value the same way it increases it for a positive one.
