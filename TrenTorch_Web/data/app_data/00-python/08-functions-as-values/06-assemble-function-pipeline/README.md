---
name: python-functions-as-values-assemble-pipeline
title: "Assemble: Build a Configurable Function Pipeline"
tags: [python-functions-as-values, python-closures, python-decorators]
difficulty: Advanced
---

## Statement

Build a small configurable transformation pipeline using functions as values, higher-order functions, closures, lambdas, and a decorator.

## Theory

This problem combines the major ideas from this module. A pipeline receives a value and passes it through a sequence of functions in order:

```python
pipeline = make_pipeline(lambda x: x + 2, lambda x: x * 3)
pipeline(4)   # (4 + 2) * 3 = 18
```

The pipeline stores the supplied transformations rather than calling them immediately — the returned pipeline is itself a function, retaining its own transformation list via closure, so two calls to `make_pipeline` with different transformations never interfere with each other. A pipeline with no transformations returns its input unchanged. The pipeline is additionally wrapped with a decorator that counts how many times it's been called, without changing the actual result.

No single feature solves this alone — the point is how functions-as-objects, closures, `*args`, and decorators compose together.

## Explanation

`make_pipeline` builds one inner function that folds `value` through every transformation in `transformations` (the exact tuple `*transformations` collected, iterated in order) — a plain `for` loop, since each step's output must become the next step's input, and there's no way to express that dependency in a comprehension. That inner function is then wrapped by the same call-counting decorator pattern as the standalone decorators topic (a `.calls` attribute on the returned callable, initialized once per `make_pipeline` call) — so the count is private to each pipeline instance, exactly like two independently created counters from the closures topic never share state. Because the decorator's wrapper simply returns whatever the inner pipeline function returns (or lets its exception propagate, since nothing catches one), the call-count bookkeeping can never mask a transformation that raises or silently substitute a different result.
