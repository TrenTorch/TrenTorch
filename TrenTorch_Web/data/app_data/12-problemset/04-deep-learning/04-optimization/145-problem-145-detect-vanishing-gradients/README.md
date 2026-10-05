---
name: problem-145-detect-vanishing-gradients
title: 'Detect Vanishing Gradients'
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'gradient stability'
hint: 'compare norms to threshold'
tools: [NumPy]
---

## Statement

Classify a gradient as vanishing when its Euclidean norm is below a threshold.

### Function signature

```python
def solve(grad, threshold):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([0.03, 0.04], 0.1)
```

**Output**

```text
True
```

**Example 2**

**Input**

```python
solve([0.3, 0.4], 0.1)
```

**Output**

```text
False
```

## Theory

### Core idea

Take the L2 norm of the gradient and compare it strictly with `threshold`.

### Contract

A norm equal to the threshold is not vanishing under this strict comparison.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
