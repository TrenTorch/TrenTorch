---
name: agentic-learning-extract-lesson-from-failure
title: Extract Reusable Lessons From a Failed Run
tags: [agentic-systems, agent-learning, experience]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A failed run that just gets discarded teaches the system nothing. A cheap first step toward actually learning from it: recognize *which category* of failure this was, from a small, curated set of known patterns, and attach the lesson already written for that category — no model call needed, just pattern matching against categories a team has already identified and written guidance for.

### From theory to code

You're given `failed_step` (the text describing what the failed step reported) and `error_keywords`, an ordered mapping from a substring pattern to the lesson text for that failure category. Implement `extract_lesson(failed_step, error_keywords)`. Return the lesson for the **first** pattern (in `error_keywords`'s iteration/insertion order) that appears as a substring anywhere in `failed_step`. If no pattern matches, return the literal string `"No specific lesson identified -- investigate manually."`.

### Constraints

- `error_keywords` has 0 to 100 entries; matching is case-sensitive, plain substring.

### Hints

<details>
<summary>Hint 1</summary>

`dict` iteration in modern Python walks keys in insertion order, so a plain `for pattern, lesson in error_keywords.items():` loop already checks patterns in exactly the order the problem asks for — no need to sort or otherwise reorder anything.

</details>

<details>
<summary>Hint 2</summary>

Return the moment the first match is found. Don't collect every matching pattern's lesson and pick one afterward — the *first* match in dict order is the only one that matters.

</details>

## Theory

### The simple version

Walk a short list of known failure patterns, in the order they were defined, and return the lesson for the first one that shows up in the failure text. If none of the known patterns match, admit it honestly rather than guessing — a specific, wrong-sounding lesson is worse than an honest "needs a human to look at this."

### Why order-dependent, first-match matters here

Some failure texts could plausibly match more than one pattern (a generic "error" pattern and a more specific "timeout" pattern might both appear in the same message) — letting the more specific or more actionable pattern be checked first, by placing it earlier in `error_keywords`, is how a curator controls which lesson actually gets surfaced without needing any explicit priority field. The dict's own definition order *is* the priority order.

### How this shows up in real systems

This is a lightweight, deterministic stand-in for the "failure triage" step in a real learning loop: before reaching for an LLM to write a bespoke post-mortem for every single failure, a cheap keyword-based categorizer against a maintained list of known failure modes can handle the common cases for free, reserving the more expensive analysis for failures that don't match anything already known.

## Explanation

The function walks `error_keywords.items()` directly, relying on Python's guaranteed dict iteration order (insertion order) to check patterns in exactly the sequence they were defined in. For each pattern, a plain `in` substring check against `failed_step` decides a match, and the function returns that pattern's lesson immediately on the first hit — which is what makes the check order-sensitive rather than just "any match wins," since an earlier, more general pattern is deliberately allowed to take priority over a later, more specific one if that's how the dictionary was authored. If the loop exhausts every pattern without a match, the function falls through to the fixed fallback string rather than returning `None` or an empty string, keeping the return type consistently a real, readable message either way.
