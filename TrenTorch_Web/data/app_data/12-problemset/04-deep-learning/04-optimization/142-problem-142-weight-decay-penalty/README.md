---
name: problem-142-weight-decay-penalty
title: 'Weight Decay Penalty'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'lam * sum(w**2)'
tools: [NumPy]
---

## Statement

Compute the L2 weight-decay penalty $\lambda\sum_i w_i^2$ of a weight vector (there is no factor $\tfrac12$).

Implement `solve(w,lam)`.

**Returns.** Return a non-negative float.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], 0.1)
```

Output:

```text
1.4
```

**Example 2**

Input:

```python
solve([0.0, 0.0], 5.0)
```

Output:

```text
0.0
```

## Theory

### The simple version

L2 regularisation adds a penalty proportional to the squared size of the weights to the loss. The optimiser then prefers small weights, which means smoother functions that overfit less. $\lambda$ sets how much the penalty matters relative to the data loss.

### The formula

$$R(w)=\lambda\sum_iw_i^2=\lambda\|w\|_2^2,\qquad \nabla R=2\lambda w$$

## Explanation

The squared norm of $(1,2,3)$ is $14$, so the penalty is $0.1\cdot14=1.4$. The gradient $2\lambda w$ shrinks each weight a little on every step, which is why this is called weight _decay_.
