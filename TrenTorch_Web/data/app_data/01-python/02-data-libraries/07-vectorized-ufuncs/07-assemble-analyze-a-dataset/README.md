---
name: numpy-assemble-analyze-a-dataset
title: 'Assemble: Analyze a Dataset Using Vectorized Operations Only'
tags: [numpy-core]
difficulty: Advanced
---

## Statement

Implement a single function that combines every topic in this module — element-wise arithmetic, ufuncs, boolean conditions, aggregations, and axis-specific aggregation — into one realistic dataset analysis task, written entirely without explicit Python loops.

## Theory

This problem introduces no new concepts. It combines every topic covered in this module into one function, matching the "assemble" pattern used elsewhere on TrenTorch.

Specifically, this requires:

- Using element-wise arithmetic and a ufunc together to transform raw data.
- Building a combined boolean condition to identify a subset of the data.
- Computing both whole-array and per-axis aggregations.
- Doing all of this without a single explicit Python `for` loop over the array's elements.

Re-read the earlier topics in this module if a specific requirement below is unclear.

## Explanation

`transformed = np.sqrt(np.abs(data))` chains two ufuncs. `valid_mask = (transformed > lower_bound) & (transformed < upper_bound)` is a combined boolean condition. `valid_count = valid_mask.sum()` counts `True` values directly (booleans sum as 0/1). `feature_means = transformed.mean(axis=0)` aggregates down each column (across samples); `sample_maxes = transformed.max(axis=1)` aggregates across each row (across features). Every step is a single vectorized expression — no explicit loop anywhere.
