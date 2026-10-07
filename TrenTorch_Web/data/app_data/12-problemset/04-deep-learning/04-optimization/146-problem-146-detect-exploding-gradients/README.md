---
name: problem-146-detect-exploding-gradients
title: 'Detect Exploding Gradients'
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'gradient stability'
hint: 'norm(grad) > threshold'
tools: [NumPy]
---

## Statement

Report whether a gradient is **exploding**: its Euclidean norm is strictly larger than `threshold`.

Implement `solve(grad, threshold)`.

**Returns.** Return a Python `bool`.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0], 4.0)
```

Output:

```text
True
```

**Example 2**

Input:

```python
solve([3.0, 4.0], 5.0)
```

Output:

```text
False
```

## Theory

### The simple version

If the factors multiplied during backpropagation are mostly larger than 1, the gradient grows exponentially instead and the weights jump to huge values, often ending in `NaN`. A very large gradient norm is the warning sign, and gradient clipping is the standard cure.

### The test

$$\text{exploding}\iff\|g\|_2>\tau$$

## Explanation

The vector $(3,4)$ has norm $5$. That is above $4$ (first example) but equal to $5$ (second example), and equality does not count because the comparison is strict.
