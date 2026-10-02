---
name: python-iteration-assemble-lazy-pipeline
title: 'Assemble: Build a Lazy Data-Processing Pipeline'
tags: [python-iteration, python-generators]
difficulty: Advanced
---

## Statement

Build a lazy processing pipeline that accepts an iterable, applies a sequence of transformations and filters, and produces results only as the pipeline is consumed.

## Theory

This problem combines the major ideas from this module: iterable vs iterator, `iter()`/`next()`, `StopIteration`, generators and `yield`, `map()`, `filter()`, and lazy execution.

The critical requirement is laziness: if the caller requests only one result, only the work necessary to produce that one result should happen — no converting the source to a list, no building an intermediate list of transformed values.

```text
request next value
      |
      v
consume only enough input
      |
      v
transform -> filter -> rejected: continue / accepted: yield
```

A generator function is the natural implementation, since `yield` provides exactly the pause-and-resume behavior a lazy pipeline needs, and it automatically becomes exhausted (raising `StopIteration`) once the underlying source is exhausted.

## Explanation

`build_pipeline` is itself a generator function — a plain `for value in source:` loop that applies every transformation to `value` in order, then checks every predicate, and only calls `yield value` if all of them passed. Because it's a generator, none of this runs until the caller actually asks for the next value: creating the pipeline consumes nothing, and requesting one result pulls exactly one value from `source`, transforms and tests only that one value, and stops there — the source is never converted to a list, and no intermediate stage's full output is ever materialized.
