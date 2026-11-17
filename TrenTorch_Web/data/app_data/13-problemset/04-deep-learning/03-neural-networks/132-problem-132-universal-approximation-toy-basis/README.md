---
name: problem-132-universal-approximation-toy-basis
title: 'Universal Approximation Toy Basis'
tags: [problemset, dl-core, universal-approximation]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'universal approximation'
hint: 'basis = max(x[:,None] - knots[None,:], 0); w = lstsq(basis, y); return basis@w, w'
tools: [NumPy]
---

## Statement

Fit a one-dimensional function with a fixed ReLU-hinge basis. Build the basis matrix $B_{ij}=\max(x_i-t_j,0)$ for the given `knots` $t_j$, solve the least-squares problem for the weights, and return both the fitted values and the weights.

Implement `solve(X, y, knots)`.

**Returns.** Return a tuple `(fitted, weights)`: the fitted values $Bw$ (length $n$) and the weights (length = number of knots). Rank-deficient bases use the minimum-norm least-squares solution (`np.linalg.lstsq`).

### Examples

**Example 1**

Input:

```python
solve([0, 1, 2], [0, 1, 2], [0])
```

Output:

```text
([0.0, 1.0, 2.0], [1.0])
```

**Example 2**

Input:

```python
solve([0, 1, 2], [0, 0, 1], [0])
```

Output:

```text
([0.0, 0.4, 0.8], [0.4])
```

## Theory

### The simple version

The universal approximation theorem says a network with one hidden layer of ReLUs can approximate any reasonable function. A ReLU hinge $\max(x-t,0)$ is a ramp that starts at the knot $t$; adding ramps with different knots and weights builds any piecewise-linear curve, and more knots give a finer approximation.

### The model

$$\hat f(x)=\sum_jw_j\max(x-t_j,0),\qquad w=\arg\min_w\|Bw-y\|_2^2$$

### Why it matters

- ReLU networks build piecewise-linear functions out of ramps.
- With the ramps fixed, only the weights are fitted, by linear least squares.

### How it works

1. Build columns $\max(x-t_j,0)$.
2. Solve the least-squares problem.
3. Return the fit and the weights.

### Worked example

With one knot at $0$ the column is $(0,1,2)$, identical to $y$, so the weight is $1$ and the fit is exact: ([0.0, 1.0, 2.0], [1.0]).

## Explanation

With the hidden ReLU units fixed (knots chosen in advance) only the output weights are learned, so fitting is ordinary linear least squares. In the first example the line $y=x$ is a single ramp with weight $1$. In the second the best single ramp through $(0,0),(1,0),(2,1)$ has weight $0.4$, a poor fit that more knots would improve.
