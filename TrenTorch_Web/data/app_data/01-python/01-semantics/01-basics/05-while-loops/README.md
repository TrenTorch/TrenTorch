---
name: python-while-loops
title: while Loops, break, continue, and Loop else
tags: [python-core, control-flow, loops]
difficulty: Intermediate
---

## Statement

Implement functions that use `while`, `break`, `continue`, and the loop `else` clause correctly, demonstrating exactly when each construct changes control flow.

## Theory

A `while` loop repeatedly runs its indented block for as long as its condition evaluates to truthy. The condition is re-checked before every single iteration, including the first.

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

**`break`** immediately exits the loop entirely — no further condition checks, no further iterations, execution continues at the first statement after the loop.

**`continue`** immediately skips to the next condition check, abandoning the rest of the current iteration's code but not exiting the loop itself.

```python
count = 0
while count < 10:
    count += 1
    if count == 3:
        continue      # skip printing 3, but keep looping
    if count == 6:
        break          # stop the loop entirely once count hits 6
    print(count)
# prints: 1 2 4 5
```

**The loop `else` clause** is a feature specific to Python's loop constructs (both `while` and `for`) that has no equivalent in an `if` statement's `else`. The `else` block attached to a loop runs only if the loop finished normally — meaning its condition eventually became falsy on its own — and does **not** run if the loop was exited via `break`.

```python
count = 0
while count < 5:
    if count == 100:     # never true here
        break
    count += 1
else:
    print("loop finished normally")     # this WILL run
```

```python
count = 0
while count < 5:
    if count == 3:
        break
    count += 1
else:
    print("loop finished normally")     # this will NOT run, because break fired
```

This is most useful for search-style loops: "did I find what I was looking for (break early), or did I search through everything without finding it (loop else)?"

## Explanation

`countdown_with_skip` uses `continue` for the one value that must be excluded rather than an `if`/`else` wrapping the whole append, so the loop's structure directly mirrors "skip this one case, otherwise proceed" instead of inverting the condition. `find_first_negative` pairs `break` (found it, stop early) with the loop's own `else` (searched everything, found nothing) rather than a sentinel value or a flag variable — exactly the search-loop pattern the theory calls out as the loop `else` clause's real use case.
