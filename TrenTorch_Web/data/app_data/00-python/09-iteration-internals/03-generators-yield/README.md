---
name: python-iteration-generators-yield
title: Generators and yield
tags: [python-generators]
difficulty: Intermediate
---

## Statement

Implement generators that produce values lazily using `yield`.

## Theory

A **generator** is a special iterator: a function containing `yield` produces a sequence of values one at a time without constructing the whole sequence first.

```python
def count_up_to(limit):
    value = 0
    while value < limit:
        yield value
        value += 1
```

Calling `count_up_to(3)` does **not** run the body — it returns a generator object, paused before any code runs. Each `next()` call resumes execution until the next `yield`, produces that value, and pauses again; local variables (like `value`) are retained across calls. When the function body finally runs off the end, the generator is exhausted and further `next()` calls raise `StopIteration`.

**`yield` vs `return`.** `return` ends a function immediately. `yield` pauses a generator so it can resume later — a generator can have many `yield`s, each one a pause point.

**Generators are lazy** — `numbers()` returning `yield 1; yield 2; yield 3` doesn't produce all three values on the call; values come out only as the generator is consumed. This matters for memory: a generator over a million values needs storage for only the current position, not all million at once.

**A generator is an iterator** — `iter(generator) is generator`, so it works directly in a `for` loop.

**Where this matters later.** Generators are central to lazy data processing: streaming datasets, large-file processing, and ML preprocessing where loading everything into memory at once is undesirable.

## Explanation

`generate_range` uses a `while` loop with `yield value` per iteration rather than building a list and yielding from it — the whole point is that no sequence is ever materialized, matching how `range()`'s own values are produced. `generate_until` breaks out of its loop (via `return`, ending the generator) the moment it sees a value greater than `limit`, _before_ yielding that value and _before_ looking at anything after it — the spec's "no later values should be consumed" only holds if the generator stops pulling from `values` the instant it decides to stop, not after scanning ahead.
