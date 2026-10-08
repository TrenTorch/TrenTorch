---
name: problem-145-detect-vanishing-gradients
title: 'Detect Vanishing Gradients'
tags: [problemset, dl-training-theory, gradient-stability]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'gradient stability'
hint: 'norm(grad) < threshold'
tools: [NumPy]
---

## Statement

Report whether a gradient is **vanishing**: its Euclidean norm is strictly smaller than `threshold`.

Implement `solve(grad, threshold)`.

**Returns.** Return a Python `bool`.

### Examples

**Example 1**

Input:

```python
solve([0.03, 0.04], 0.1)
```

Output:

```text
True
```

**Example 2**

Input:

```python
solve([0.3, 0.4], 0.1)
```

Output:

```text
False
```

**Example 3**

Input:

```python
solve([0.06, 0.08], 0.1)
```

Output:

```text
False
```

## Theory

### The simple version

In deep networks the gradient is a product of many factors. If those are mostly smaller than 1 it shrinks exponentially going backwards, so the early layers barely learn. A tiny gradient norm is the practical symptom.

### The test

$$\text{vanishing}\iff\|g\|_2<\tau$$

### Why it matters

- When gradients shrink toward zero the early layers stop learning.
- The norm is a simple health check.

### How it works

1. Compute the Euclidean norm.
2. Compare it (strictly less than) with the threshold.

### Worked example

$\|(0.03,0.04)\|=\sqrt{0.0009+0.0016}=0.05$, below $0.1$, so the result is True.

## Explanation

The first example has norm $0.05<0.1$, so it vanishes; the second has norm $0.5$. A norm exactly equal to the threshold (third example, $0.1$) is _not_ flagged because the comparison is strict. Remedies include ReLU activations, residual connections and good initialisation.
