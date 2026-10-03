---
name: agentic-loop-detect-repeating-action
title: Detect a Repeating Action and Break the Loop
tags: [agentic-systems, agent-loop, reliability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A model stuck in a bad pattern doesn't always fail loudly — sometimes it just calls the exact same tool with the exact same arguments over and over, each time apparently confident this attempt will be different, never actually making progress. This looks completely different from the "consecutive failures" pattern in the earlier self-reflection question: the observations here might not look like failures at all (the tool might succeed every time!) — the problem is purely that the _same action_ keeps recurring, which is its own distinct signal that something's wrong.

### From theory to code

You're given every step's `(action, action_input)` pair, in order, a `window` size, and a `repeat_threshold`. Implement `detect_repeating_action(actions, window, repeat_threshold)`. Walk the steps in order. After each step, look at only the last `window` steps seen so far (fewer if not enough steps have happened yet) and count how many of them exactly match the action just taken. The moment that count reaches `repeat_threshold`, return the current 1-indexed step number. Return `None` if it never happens.

### Constraints

- 1 to 500 steps; `window >= 1`, `repeat_threshold >= 1`.

### Hints

<details>
<summary>Hint 1</summary>

A fixed-size sliding window is exactly what `collections.deque(maxlen=window)` gives you for free — appending past capacity automatically drops the oldest entry, so you never need to manually trim anything.

</details>

<details>
<summary>Hint 2</summary>

Count matches _within the current window only_, not across the whole history — a `deque` with `maxlen` set already only ever contains the most recent `window` items, so counting within it is automatically counting within the window.

</details>

## Theory

### The simple version

Keep a rolling buffer of the last `window` actions. Every time a new action comes in, add it to the buffer (automatically evicting the oldest one if the buffer's full) and count how many entries in that buffer are identical to the one just added. If that count reaches the threshold, the agent has been calling the same thing too often, too recently — time to break the loop.

### Why a sliding window instead of a lifetime total count

Two occurrences of the same action, once early in a long run and once much later, usually aren't a stuck loop — they're just the same reasonable action being called twice across a long, otherwise-progressing task. A sliding window captures "the same thing keeps happening _right now_," which is the actual signal worth reacting to, and specifically doesn't get triggered by a legitimately repeated action that's spread out over a long run with plenty of other, different actions in between.

### How this shows up in real systems

This is a standard agent-loop safety guard, complementary to (not a replacement for) the step/time budgets and the consecutive-failure check elsewhere in this track — it catches a genuinely different failure mode: an agent that isn't failing and isn't over budget, but is nonetheless not making progress because it's cycling through the same move.

## Explanation

A `deque` with `maxlen=window` is the entire piece of state: appending to it when it's already at capacity automatically drops the oldest entry, so the deque always holds exactly the most recent `window` actions (or fewer, early in the run) with no manual bookkeeping. After appending the current step's action, `recent.count(action)` counts how many of the entries currently in that window — including the one just added — exactly equal it; because tuples compare by value, `("search", "x")` only ever matches another `("search", "x")`, never a different input to the same action name. The moment that count reaches `repeat_threshold`, the function returns the current step number immediately, which is what makes it the _first_ point the pattern is detected rather than the last.
