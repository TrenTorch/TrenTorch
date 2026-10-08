---
name: research-double-descent-min-norm
title: 'Deep Double Descent: The Minimum-Norm Interpolator'
tags: [research-papers, classical-ml, learning-theory, double-descent]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Deep double descent (Nakkiran et al., 2019) shows test error can rise and then fall again as models grow past the point where they fit the training data exactly. Past that point, gradient descent from zero converges to the minimum-norm interpolating solution, which this question computes directly.

### From theory to code

Implement `min_norm_solution(X, y)`, returning the least-norm `w` with `X w` closest to `y`, using the pseudo-inverse.

### Constraints

- Works when there are more features than samples, and when there are fewer.

### Hints

<details>
<summary>Hint 1</summary>

`np.linalg.pinv(X) @ y` gives the minimum-norm least-squares solution.

</details>

## Theory

### The simple version

When the system has many solutions, the pseudo-inverse picks the one with the smallest length. That choice is what implicit regularization of gradient descent tends to find.

### The formula

$$w^* = X^{+} y = \arg\min_w \lVert w \rVert_2 \text{ subject to } Xw = y \text{ (when } p > n\text{)}$$

### How NumPy/PyTorch actually implements this

`torch.linalg.pinv` and `np.linalg.lstsq` compute the same minimum-norm solution for underdetermined systems.

## Explanation

The pseudo-inverse is the unique solution in the row space of `X`, which is why its norm is smallest.
