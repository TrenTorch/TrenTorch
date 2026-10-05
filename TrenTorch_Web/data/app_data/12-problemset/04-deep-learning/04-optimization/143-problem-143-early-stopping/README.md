---
name: problem-143-early-stopping
title: 'Early Stopping'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'reset patience on strict improvement'
tools: [NumPy]
---

## Statement

Determine whether validation has failed to improve for `patience` consecutive epochs.

### Function signature

```python
def solve(losses, patience):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([3.0, 2.0, 2.1, 2.2], 2)
```

**Output**

```text
True
```

**Example 2**

**Input**

```python
solve([3.0, 2.0, 1.0], 2)
```

**Output**

```text
False
```

## Theory

### Core idea

A strictly lower loss resets the counter; each other loss increments it. Return as soon as the counter reaches patience.

### Contract

An epoch ties the best loss counts as non-improving.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
