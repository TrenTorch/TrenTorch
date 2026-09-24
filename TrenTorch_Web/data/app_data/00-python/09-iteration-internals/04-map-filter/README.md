---
name: python-iteration-map-filter
title: map() and filter()
tags: [python-map-filter]
difficulty: Intermediate
---

## Statement

Implement functions using `map()` and `filter()` to transform and select values lazily.

## Theory

`map(function, iterable)` applies `function` to every item, lazily — it returns a lazy iterator-like object, not a list, and calls `function` only as the result is consumed:

```python
result = map(square, [1, 2, 3])
list(result)   # [1, 4, 9] -- materialized on demand
```

`map` receives the function object itself (`square`, not `square(values)`) — it calls the function on individual elements as they're requested.

`filter(predicate, iterable)` keeps only elements for which `predicate` returns a truthy value:

```python
list(filter(is_even, [1, 2, 3, 4]))   # [2, 4]
```

**`map` transforms, `filter` selects**, and they compose: `filter(is_even, map(square, values))` transforms first, then selects from the transformed values.

**One-time consumption.** The result of `map()`/`filter()` is consumed as it's iterated — calling `list(mapped)` a second time returns `[]`, since the underlying iterator is already exhausted.

**Where this matters later.** `map`/`filter` show how higher-order functions and lazy iteration combine into processing pipelines, the same shape as transformations over batches of data in ML systems.

## Explanation

`squared` and `keep_positive` return the `map`/`filter` objects directly rather than wrapping them in `list(...)` — the spec explicitly asks for a *lazy* object, and calling `list()` inside the function would defeat that, forcing the caller to materialize instead of choosing to. `transform_and_filter` composes `filter(predicate, map(transform, values))` in that exact nesting — `map` is the innermost stage since transformation must happen before the predicate ever sees a value, matching the spec's own required order.
