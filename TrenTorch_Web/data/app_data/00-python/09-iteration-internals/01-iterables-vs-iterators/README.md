---
name: python-iteration-iterables-vs-iterators
title: Iterables vs Iterators
tags: [python-iteration]
difficulty: Beginner
---

## Statement

Implement functions that distinguish between an iterable and an iterator and inspect how Python obtains an iterator from an iterable.

## Theory

An **iterable** is an object that can provide an iterator. An **iterator** is an object that produces values one at a time while keeping track of where it currently is.

```python
values = [10, 20, 30]
iterator = iter(values)
```

The list is the collection; it isn't itself responsible for remembering position. `iter(values)` creates a separate iterator object that has a current position. Common built-in iterables: `list`, `tuple`, `str`, `dict`, `set`, `range`.

**Iterators are themselves iterable** — `iter(iterator) is iterator` is `True`, which is exactly what lets an iterator work naturally with a `for` loop.

**Separate `iter()` calls give separate state.** `a = iter(values); b = iter(values)` are two distinct iterator objects — advancing `a` never advances `b`.

**A simplified model of `for`:**

```python
iterator = iter(values)
while True:
    try:
        value = next(iterator)
    except StopIteration:
        break
    process(value)
```

**Where this matters later.** Understanding the collection-vs-iterator-state distinction makes generators, `map`, `filter`, and lazy pipelines much easier to reason about.

## Explanation

`is_iterator` checks `iter(obj) is obj` directly — the exact property the theory names as what defines an iterator (its own `iter()` returns itself), rather than checking `type(obj)` against a fixed list of iterator classes, which would miss custom iterators. `independent_iterators` calls `iter(values)` twice, producing two genuinely separate objects each with their own position, rather than calling it once and returning the same object twice.
