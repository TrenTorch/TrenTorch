---
name: python-looping-statements
title: Looping Statements
tags: [python-core, control-flow, loops]
difficulty: Intermediate
---

## Statement

Implement functions that use `while` and `for` loops, along with `break`, `continue` and the loop `else` clause, demonstrating exactly when each construct changes control flow. Also replicate by hand what a `for` loop does internally.

## Theory

### while loops

A `while` loop repeatedly runs its indented block for as long as its condition evaluates to truthy. The condition is re-checked before every iteration, including the first.

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

### for loops

A `for` loop iterates directly over the elements of an iterable (a list, string, tuple, dict, set, or range), assigning each element in turn to the loop variable.

```python
for item in [10, 20, 30]:
    print(item)
```

A `for` loop asks the collection for elements one at a time, in order, and stops automatically once the collection is exhausted. You never track an index or a stopping condition yourself, unlike a `while` loop. Under the hood it is built on `iter()` and `next()`, which are covered fully in the Iteration Internals module.

`enumerate()` pairs each element with its position. The `for` loop unpacks each `(index, value)` tuple directly into two loop variables:

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)
# 0 a
# 1 b
# 2 c
```

Iterating over a dictionary yields its keys only:

```python
d = {"a": 1, "b": 2}
for key in d:
    print(key)     # "a", then "b"
```

To get keys and values together, use `.items()` (covered in the Dictionaries module).

### break & continue

Both loop types support `break` and `continue`.

**`break`** exits the loop entirely. No further condition checks or iterations happen, and execution continues at the first statement after the loop.

**`continue`** skips to the next iteration, abandoning the rest of the current iteration's code without exiting the loop.

```python
count = 0
while count < 10:
    count += 1
    if count == 3:
        continue      # skip printing 3, but keep looping
    if count == 6:
        break         # stop the loop entirely once count hits 6
    print(count)
# prints: 1 2 4 5
```

### The loop else clause

Both `while` and `for` accept an `else` block. It runs only if the loop finished normally, meaning the condition became falsy on its own or the iterable ran out. It does **not** run if the loop was exited via `break`.

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

This is most useful for search-style loops: did I find what I was looking for (break early), or did I search through everything without finding it (loop else)?

## Explanation

`countdown_with_skip` uses `continue` for the one value that must be excluded, rather than wrapping the whole append in an `if`/`else`, so the loop mirrors "skip this one case, otherwise proceed". `find_first_negative` pairs `break` (found it, stop early) with the loop's own `else` (searched everything, found nothing) instead of a sentinel value or a flag variable, which is the search-loop pattern the loop `else` clause exists for.

`sum_with_index` uses `enumerate()` because the required output keys are the indices, which is the case `enumerate()` exists for. `manual_iteration_trace` calls `iter()` once to get an iterator, then calls `next()` repeatedly inside its own `while True:` loop, catching `StopIteration` to detect exhaustion. This is the lower-level mechanism a `for` loop hides, made explicit to demystify it ahead of the Iteration Internals module.
