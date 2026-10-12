---
name: problem-109-relu-activation
title: 'ReLU Activation'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'np.maximum(x, 0)'
tools: [NumPy]
---

## Statement

Apply the ReLU activation element-wise: $\max(0,x)$.

Implement `solve(x)`.

**Returns.** Return a NumPy array of the same shape: negative values become $0$, others are unchanged.

### Examples

**Example 1**

Input:

```python
solve([-2, 0, 3])
```

Output:

```text
[0, 0, 3]
```

**Example 2**

Input:

```python
solve([[-1.5, 2.5], [0.0, -0.1]])
```

Output:

```text
[[0.0, 2.5], [0.0, 0.0]]
```

## Theory

### The simple version

ReLU ("rectified linear unit") passes positive numbers through and replaces negatives with zero. It is cheap, does not saturate for positive inputs, and is the default hidden-layer activation in most modern networks.

### The formula

$$\operatorname{ReLU}(x)=\max(0,x)$$

### Why it matters

- Without a non-linearity, stacked linear layers collapse to one linear layer.
- ReLU is cheap and does not saturate for positive inputs.

### How it works

1. Compare each entry with $0$.
2. Keep the larger.

### Worked example

For $(-2,0,3)$ the negative value becomes $0$, zero stays $0$ and $3$ stays $3$: [0, 0, 3].

## Explanation

`np.maximum` compares each entry with $0$ independently, so any shape works. Its weakness is the "dying ReLU" problem: a unit whose input is always negative outputs $0$ and receives zero gradient, so it stops learning.
