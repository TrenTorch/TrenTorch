---
name: problem-140-warmup-schedule
title: 'Warmup Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'piecewise warmup then cosine'
tools: [NumPy]
---

## Statement

Linearly warm up a learning rate, then decay it with a half-cosine.

### Function signature

```python
def solve(lr0, min_lr, t, warmup, T):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(1.0, 0.1, 0, 2, 6)
```

**Output**

```text
0.5
```

**Example 2**

**Input**

```python
solve(1.0, 0.1, 2, 2, 6)
```

**Output**

```text
1.0
```

## Theory

### Core idea

For steps before `warmup`, increase linearly; thereafter use the cosine schedule from `lr0` to `min_lr` through step `T`.

### Contract

During warmup `lr_t = lr0 * (t + 1) / warmup`; afterwards use the cosine-decay expression.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
