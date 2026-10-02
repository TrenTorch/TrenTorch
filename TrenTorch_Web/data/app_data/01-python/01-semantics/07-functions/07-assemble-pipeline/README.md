---
name: python-functions-assemble-pipeline
title: 'Assemble: Build a Configurable Data-Processing Pipeline'
tags: [python-functions, python-args-kwargs]
difficulty: Advanced
---

## Statement

Implement a small configurable data-processing pipeline that combines function definitions, positional and keyword arguments, default parameters, `*args`, `**kwargs`, local state, scope, docstrings, and annotations.

## Theory

This problem combines the function concepts from this module into one task. The pipeline receives a sequence of numbers and applies a configurable sequence of transformations, using a signature equivalent to:

```python
def run_pipeline(values, *transformations, **options):
    ...
```

`transformations` receives a tuple of every positional transformation function; `options` receives a dictionary of keyword configuration. Supported options are `unique` (defaults to `False`) and `limit` (defaults to no limit); unknown options must raise `TypeError`.

Each input value passes through every transformation in order. With `unique=True`, a set tracks values already emitted while a list preserves output order (combining this module with the Sets module). With a positive `limit`, collection stops once that many output values have been produced; `limit=0` means an empty result.

No new theory beyond re-reading the relevant topics is required.

## Explanation

`run_pipeline` validates `options` by popping the two supported keys (`unique`, `limit`) and raising `TypeError` if anything remains — this is what makes an unrecognized option a hard error rather than a silently-ignored typo. The output list and the `seen` set (used only when `unique=True`) are both local variables created fresh inside the function body on every call, so nothing about one call's progress can leak into the next — exactly the "no global pipeline state" requirement the spec calls out. The `limit` check happens right after a value is actually appended to the result (not before), so it counts _output_ values post-uniqueness-filtering, matching the worked example where `limit=2` with one transformation yields the first two transformed values, not the first two input values.
