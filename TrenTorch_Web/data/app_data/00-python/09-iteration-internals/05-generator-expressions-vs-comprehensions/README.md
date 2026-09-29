---
name: python-iteration-generator-expressions-vs-comprehensions
title: Generator Expressions vs List Comprehensions
tags: [python-lazy-evaluation]
difficulty: Intermediate
---

## Statement

Implement functions that choose between a list comprehension and a generator expression depending on whether the task requires immediate materialization or lazy iteration.

## Theory

A **list comprehension**, `[x * 2 for x in values]`, immediately builds the whole list — every element exists in memory once the expression finishes.

A **generator expression**, `(x * 2 for x in values)`, produces values on demand instead. Creating one does no transformation work at all; work happens as the generator is consumed.

```python
def process(x):
    print("processing", x)
    return x * 2

[process(x) for x in values]     # process() runs for every x right now
(process(x) for x in values)     # nothing runs yet
```

**Memory.** A list comprehension needs space proportional to the input size, $O(N)$. A generator expression needs only enough state to produce the next value — but "lazy" doesn't mean "zero memory": it still retains the underlying iterable and its own execution state.

**When to use each.** A list when you need a concrete, indexable, multi-pass result. A generator expression when values are consumed once, the input/output is large, or downstream processing can happen incrementally.

**Where this matters later.** Large ML datasets are often processed incrementally rather than converted into full intermediate Python lists — this is the direct bridge to that habit.

## Explanation

`eager_double` uses `[x * 2 for x in values]` — square brackets, forcing full materialization before the function returns, exactly what the spec requires. `lazy_double` and `lazy_positive` use the parenthesized form instead, `(x * 2 for x in values)` / `(x for x in values if x > 0)` — the only syntactic difference between the two forms, but the one that determines whether the transformation runs immediately or on demand.
