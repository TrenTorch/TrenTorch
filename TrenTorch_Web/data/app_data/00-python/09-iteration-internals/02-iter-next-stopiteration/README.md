---
name: python-iteration-iter-next-stopiteration
title: "iter(), next(), and StopIteration"
tags: [python-iteration]
difficulty: Intermediate
---

## Statement

Implement functions that manually consume iterators using `iter()` and `next()`, including correctly detecting the end of iteration through `StopIteration`.

## Theory

`iter(values)` obtains an iterator; `next(iterator)` asks it for its next value, advancing its internal state each time:

```python
iterator = iter([10, 20, 30])
next(iterator)  # 10
next(iterator)  # 20
next(iterator)  # 30
next(iterator)  # raises StopIteration
```

`StopIteration` is a signal, not an ordinary value — it's what a `for` loop catches internally so the exception never surfaces to normal iteration code.

**`next(iterator, default)`** returns `default` instead of raising when the iterator is exhausted:

```python
iterator = iter([10])
next(iterator, None)   # 10
next(iterator, None)   # None
```

**Don't confuse exhaustion with a falsy value.** An iterator can legitimately produce `None`, `0`, `False`, or `""` as real values — iteration only ends when `StopIteration` is actually raised, so checking `if value is None` is never a correct way to detect exhaustion.

**Where this matters later.** This explains how generators and lazy pipelines actually execute, and helps when debugging a data source that appears to "disappear" because an iterator was already consumed.

## Explanation

`consume_iterator` and `take_first` both use a `try`/`except StopIteration` loop around `next()` rather than a `for` loop, per the exercise's own constraint — this is the manual version of exactly what a `for` loop does internally. `next_or_default` calls `next(iterator, default)` directly (the two-argument form) rather than a `try`/`except`, which is the built-in's own way of expressing "give me a sentinel instead of raising" — and since it returns whatever `next()` actually produced, a real falsy value like `0` or `None` from the iterator is never mistaken for the sentinel.
