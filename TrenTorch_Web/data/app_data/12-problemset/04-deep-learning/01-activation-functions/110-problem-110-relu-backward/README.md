---
name: problem-110-relu-backward
title: 'ReLU Backward'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: '(x > 0) as float'
tools: [NumPy]
---

## Statement

Compute the derivative mask of ReLU: $1$ where the input is strictly positive and $0$ elsewhere (including at $0$).

Implement `solve(x)`.

**Returns.** Return a float NumPy array of `0.0` and `1.0` with the same shape as `x`.

### Examples

**Example 1**

Input:

```python
solve([-2, 0, 3])
```

Output:

```text
[0.0, 0.0, 1.0]
```

**Example 2**

Input:

```python
solve([[1.0, -1.0], [0.5, 0.0]])
```

Output:

```text
[[1.0, 0.0], [1.0, 0.0]]
```

## Theory

### The simple version

During backpropagation the gradient flowing into a ReLU is multiplied by the ReLU's derivative: $1$ where the unit was active and $0$ where it was off. The mask therefore either lets the gradient through unchanged or blocks it.

### The formula

$$\operatorname{ReLU}'(x)=\begin{cases}1&x>0\\0&x\le0\end{cases}$$

### Why it matters

- Backpropagation multiplies the gradient by the activation's derivative.
- For ReLU that derivative is a simple on/off mask.

### How it works

1. Mark entries greater than $0$ with $1$.
2. All other entries get $0$.

### Worked example

For $(-2,0,3)$ only $3$ is positive, so the mask is [0.0, 0.0, 1.0].

## Explanation

ReLU is not differentiable at exactly $0$; any value in $[0,1]$ is a valid subgradient and the common convention is $0$, which is what the strict `>` comparison gives.
