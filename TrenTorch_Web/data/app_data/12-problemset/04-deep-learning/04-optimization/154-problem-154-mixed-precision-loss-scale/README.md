---
name: problem-154-mixed-precision-loss-scale
title: 'Mixed Precision Loss Scale'
tags: [problemset, dl-training-theory, numerical-stability]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'numerical stability'
hint: 'multiply before backward and divide before update'
tools: [NumPy]
---

## Statement

Scale a loss and unscale its associated gradients.

### Function signature

```python
def solve(loss, scaled_grads, scale):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve(2.0, [[8.0, 4.0]], 4.0)
```

**Output**

```text
(8.0, [[2.0, 1.0]])
```

**Example 2**

**Input**

```python
solve(0.5, [[-6.0]], 2.0)
```

**Output**

```text
(1.0, [[-3.0]])
```

## Theory

### Core idea

Multiply the loss by `scale` and divide every supplied scaled gradient by the same factor.

### Contract

The returned pair contains the scaled loss followed by the unscaled gradients.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
