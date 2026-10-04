---
name: problem-146-detect-exploding-gradients
title: "Detect Exploding Gradients"
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-training|Optimization"
topic: "gradient stability"
hint: "compute norm and compare"
tools: [NumPy]
---

## Statement

Classify a gradient as exploding when its Euclidean norm is above a threshold.

### Function signature

```python
def solve(grad, threshold):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([3.0, 4.0], 4.0)
```

**Output**

```text
True
```

**Example 2**

**Input**

```python
solve([3.0, 4.0], 5.0)
```

**Output**

```text
False
```

## Theory

### Core idea

Take the L2 norm of the gradient and compare it strictly with `threshold`.

### Contract

A norm equal to the threshold is not exploding under this strict comparison.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
