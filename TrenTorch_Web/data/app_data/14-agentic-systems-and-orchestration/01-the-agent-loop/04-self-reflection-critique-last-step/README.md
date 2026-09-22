---
name: agentic-loop-self-reflection-abandon
title: 'Self-Reflection: Critique the Last Step Before Continuing'
tags: [agentic-systems, agent-loop, reliability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

An agent that never looks back at its own last step will happily repeat a failing action forever, burning its step and time budgets on something that was never going to work. A minimal form of self-reflection is much cheaper than a full model-based critique: just watch for observations that look like failures, and give up once too many have happened _in a row_ — a single isolated failure is normal and worth retrying past, but a run of consecutive failures is a strong signal something is fundamentally broken, not just unlucky.

### From theory to code

You're given every step's observation text, in order, a list of `failure_keywords`, and a `max_consecutive_failures` threshold. Implement `find_abandon_point(observations, failure_keywords, max_consecutive_failures)`. An observation "looks like a failure" if it contains **any** of `failure_keywords` as a substring. Track a running count of _consecutive_ failure-looking observations — any success resets the count to zero. Return the 1-indexed step at which that running count first reaches `max_consecutive_failures`, or `None` if it never does.

### Constraints

- 1 to 200 observations; keyword matching is case-sensitive, plain substring (no regex).

### Hints

<details>
<summary>Hint 1</summary>

One running counter, reset to zero on any success and incremented on any failure, is the entire piece of state you need — no need to look backward at a window of previous observations each time.

</details>

<details>
<summary>Hint 2</summary>

`any(keyword in observation for keyword in failure_keywords)` checks "does this specific observation look like a failure" in one line — don't build a combined regex or loop-within-a-loop by hand.

</details>

## Theory

### The simple version

Walk the observations once, keeping a single counter of how many failure-looking ones have happened in a row. Every success resets that counter to zero — a run has to be _unbroken_ to count. The moment the counter reaches the threshold, that's the abandon point.

### Why consecutive, not total, failures

A run that fails once, recovers, fails once more, recovers again, and so on isn't actually stuck — it's making real progress overall, just with some noise along the way. A run that fails five times in an unbroken row almost certainly _is_ stuck: whatever's causing the failure hasn't changed between attempts, so there's no reason to expect the next attempt to behave any differently. Counting consecutive failures (not total failures across the whole run) is what correctly distinguishes "noisy but progressing" from "actually stuck."

### How this shows up in real systems

This is the cheapest possible circuit breaker: a single counter and a threshold, no model call needed to decide "should I keep going." Real agent frameworks layer a real reflection step (asking the model itself to critique its last action) on top of exactly this kind of cheap, deterministic guard — the guard catches the obvious "this is clearly broken" case fast and free, before ever spending a model call on a more nuanced judgment.

## Explanation

The function keeps one `consecutive` counter, initialized to zero, and walks `observations` with a 1-indexed loop. For each observation, `any(keyword in observation for keyword in failure_keywords)` checks whether it looks like a failure; if so, `consecutive` increments, otherwise it resets to zero — this reset is what makes the counter track an _unbroken_ run rather than a cumulative total. After updating the counter, the function checks whether it has reached `max_consecutive_failures` and returns the current step number immediately if so, which is what makes the returned step the _first_ point the threshold is hit, not the last. If the loop finishes without the counter ever reaching the threshold, `None` is returned.
