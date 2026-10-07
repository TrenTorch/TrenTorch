---
name: problem-53-lasso-soft-threshold
title: 'Lasso Soft Threshold'
tags: [problemset, classical-ml, regularization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'sign(z) * max(|z| - lam, 0)'
tools: [NumPy]
---

## Statement

Apply the soft-thresholding operator used by one coordinate-descent step of the lasso: shrink the value `z` toward zero by `lam`, and set it to exactly zero if $|z|\le\lambda$.

Implement `solve(z,lam)`.

**Returns.** Return the shrunken value as a float (`0.0` when it is thresholded away). `lam` must be non-negative.

### Examples

**Example 1**

Input:

```python
solve(3.0, 1.0)
```

Output:

```text
2.0
```

**Example 2**

Input:

```python
solve(-2.5, 1.0)
```

Output:

```text
-1.5
```

**Example 3**

Input:

```python
solve(0.4, 1.0)
```

Output:

```text
0.0
```

## Theory

### The simple version

The lasso adds an L1 penalty that pulls coefficients toward zero and can set them _exactly_ to zero, which is what makes it select features. Each coordinate-descent step reduces to one tiny operation: move $z$ toward zero by $\lambda$, but never cross zero.

### The formula

$$S_\lambda(z)=\operatorname{sign}(z)\,\max(|z|-\lambda,\,0)$$

## Explanation

A value larger than $\lambda$ in magnitude keeps its sign and loses $\lambda$ of its size. A value inside $[-\lambda,\lambda]$ is killed entirely, which is the source of sparsity. This is the proximal operator of the L1 norm.
