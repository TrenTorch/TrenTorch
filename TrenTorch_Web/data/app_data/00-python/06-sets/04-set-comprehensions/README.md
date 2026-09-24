---
name: python-sets-comprehensions
title: Set Comprehensions
tags: [python-set-comprehensions]
difficulty: Intermediate
---

## Statement

Implement functions using set comprehensions to construct unique transformed values and filtered sets.

## Theory

A **set comprehension** creates a set from an iterable using a compact expression: `{expression for variable in iterable}`, equivalent to a loop that `.add()`s each result into a fresh set.

```python
{x * 2 for x in [1, 2, 3]}          # {2, 4, 6}
```

**Uniqueness still applies** — the comprehension may evaluate its expression many times, but equal results collapse into one element: `{x % 3 for x in range(10)}` is `{0, 1, 2}`.

**Filtering with `if`** works as in list comprehensions: `{expression for variable in iterable if condition}`.

```python
{x * x for x in values if x >= 0}
```

**Multiple loops** and nested iteration work the same way as list comprehensions too.

**The expression must produce a hashable value**, since it becomes a set element — `{[x] for x in values}` raises `TypeError` because a list can't be a set element.

**Where this matters later.** Set comprehensions provide a direct way to construct unique transformed data, the same expression-and-filter structure that appears in list comprehensions.

## Explanation

`squared_unique` squares every value inside the comprehension itself (`{x * x for x in values}`) rather than squaring first into a list and converting to a set afterward — the comprehension's own uniqueness guarantee handles duplicate squared results (e.g. `-2` and `2` both squaring to `4`) with no extra step. `positive_unique` filters with `if x > 0` *after* the `for`, matching the spec's own boundary (`0` is excluded, since it's neither positive nor negative but the requirement is specifically "positive").
