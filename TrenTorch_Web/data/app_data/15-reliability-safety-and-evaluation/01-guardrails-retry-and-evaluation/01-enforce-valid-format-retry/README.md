---
name: agentic-guardrails-enforce-format-retry
title: Enforce a Valid Output Format With Retry
tags: [agentic-systems, guardrails, reliability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

*Force Valid JSON Output With Retry on Parse Failure* enforced JSON syntax specifically. Plenty of structured-output needs are simpler than that: a classifier that must output exactly one of a small, fixed set of labels, a router that must output exactly one of a known set of destinations. The failure mode here isn't "malformed syntax" — it's "the model said something that isn't one of the allowed values at all," and the fix is the same retry-loop shape with a different validity check.

### From theory to code

You're given `max_retries`, the model's raw output text for each `attempts`, and `allowed_values` — the closed set of exactly-valid output strings. Implement `enforce_format_with_retry(max_retries, attempts, allowed_values)`. Try attempt 1, then 2, ... up to at most `max_retries + 1` total attempts or `len(attempts)` attempts, whichever is fewer, stopping at the first attempt whose **stripped** text is exactly one of `allowed_values`.

Return `"SUCCESS i"` (1-indexed) for the first valid attempt, or `"FAILURE t"` where `t` is the number of attempts actually tried.

### Constraints

- 0 to 20 for `max_retries`; 1 to 20 attempts logged; matching is case-sensitive, exact (after stripping leading/trailing whitespace).

### Hints

<details>
<summary>Hint 1</summary>

This is the exact same retry-loop shape as *Force Valid JSON Output With Retry on Parse Failure* and *Retry a Malformed Tool Call With Model-Guided Correction* — compute the attempt bound once, scan up to it, stop on the first success. Only the validity check itself changes.

</details>

<details>
<summary>Hint 2</summary>

`attempts[i].strip() in allowed_values` is the entire validity check — a model's raw text output often has incidental leading/trailing whitespace or a trailing newline that shouldn't count against it.

</details>

## Theory

### The simple version

Validity here is pure set membership: is this exact (stripped) string one of the small number of things we said was allowed? No syntax to parse, no structure to check — just a lookup. The retry loop wrapped around that check is identical in shape to every other bounded-retry problem in this curriculum.

### Why a closed-set check instead of a "looks like a valid label" heuristic

A classifier or router with a small, known set of legal outputs benefits from the strictest possible check precisely because there's no ambiguity about what's valid — unlike free-form text, where "close enough" might be a reasonable bar, a wrong label routed to the wrong downstream handler is a real bug, not a stylistic imperfection. Exact set membership is both the simplest possible check to implement and the correct one for this kind of closed-vocabulary output.

### How this shows up in real systems

Any system with a model that's supposed to choose from a small, fixed menu (a classification label, an intent category, a routing destination) needs exactly this kind of validation-with-retry, and it's dramatically cheaper to implement and reason about than syntax validation, since it's a single set lookup rather than a parser.

## Explanation

The attempt bound is computed once as `min(len(attempts), max_retries + 1)`, exactly mirroring the other retry-loop problems in this curriculum. Each attempt within that bound is checked with `attempts[i].strip() in allowed_values` — stripping first so incidental whitespace never causes an otherwise-correct label to be rejected, then a direct set membership test that's exact and case-sensitive with no partial-match leniency. The loop returns `"SUCCESS i"` immediately on the first attempt that passes, or `"FAILURE t"` with the same bound used for the scan if none do.
