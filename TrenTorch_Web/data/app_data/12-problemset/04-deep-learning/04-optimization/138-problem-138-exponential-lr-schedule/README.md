---
name: problem-138-exponential-lr-schedule
title: 'Exponential LR Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'lr_t=lr0*gamma^t'
tools: [NumPy]
---

## Statement

Compute an exponentially decayed learning rate.

### Function signature

```python
def solve(lr0, gamma, t):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(5.0, 0.1, 2)
```

**Output**

```text
0.05
```

**Example 2**

**Input**

```python
solve(3.0, 0.5, 0)
```

**Output**

```text
3.0
```

## Theory

### Core idea

Raise the multiplicative decay factor to the current step and multiply by the initial learning rate.

### Contract

`lr_t = lr0 * gamma ** t`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
