---
name: problem-139-cosine-lr-schedule
title: 'Cosine LR Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'use half-cosine interpolation'
tools: [NumPy]
---

## Statement

Compute the cosine-decayed learning rate between `lr0` and `min_lr`.

### Function signature

```python
def solve(lr0, min_lr, t, T):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(5.0, 1.0, 0, 10)
```

**Output**

```text
5.0
```

**Example 2**

**Input**

```python
solve(5.0, 1.0, 10, 10)
```

**Output**

```text
1.0
```

## Theory

### Core idea

Interpolate with a half-cosine across `T` steps; values before zero or after `T` are clamped to the schedule endpoints.

### Contract

`lr_t = min_lr + 0.5 * (lr0 - min_lr) * (1 + cos(pi * t / T))`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
