---
name: feature-selection-ista-sparse-coding
title: 'Sparse coding with ISTA'
tags: [classical-ml, feature-selection, sparse-learning, lasso, proximal-gradient]
difficulty: Advanced
---

## Statement

### Shrink small coefficients to exactly zero

Sparse coding asks for a coefficient vector `x` that reconstructs `y` from the dictionary `D` while keeping `x` sparse. It minimizes `0.5 * ||y - D x||^2 + lam * ||x||_1`. The L1 term is not differentiable at zero, so the iterative shrinkage-thresholding algorithm (ISTA) alternates a gradient step with a soft threshold.

Implement two functions.

- `soft_threshold(z, t)`: returns `sign(z) * max(|z| - t, 0)`, elementwise.
- `sparse_code(D, y, lam=0.1, iters=100)`: starts from `x = 0`. Each iteration:
  1. `g = D^T (D x - y)`
  2. `x = soft_threshold(x - step * g, step * lam)`

  The step is `1 / L`, where `L = ||D||_2^2` (the largest singular value squared). If `L` is zero, use a step of `1.0`.

Return `x` after `iters` iterations.

### Constraints

- `D` is 2-D with `n` rows, `y` has length `n`, otherwise raise `ValueError`.
- `lam < 0` or `iters < 0` raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

With `D` the identity and `x = 0`, the first iteration gives `soft_threshold(y, lam)` exactly.

</details>

## Theory

ISTA is proximal gradient descent on the lasso objective. The gradient step decreases the squared error when the step is at most `1/L`, and the soft threshold is the proximal operator of the L1 penalty, which is why coefficients snap to exactly zero instead of shrinking gradually. The same penalty appears in the lasso regression question, where coordinate descent solves it instead.

### Where this shows up in production

The solver under the lasso and under sparse coding when the dictionary is fixed and codes must be computed for many inputs, such as sparse feature extraction in vision pipelines or denoising in signal chains. Accelerated variants (FISTA) are the usual choice once the basic loop is in place.

### Using it to make decisions

Use it when you want a convex sparsity penalty and a single knob, lambda, that trades reconstruction error against the number of nonzero codes. Tune lambda against your latency and sparsity budget, and stop the loop on a change in the objective, not on a fixed count. If the dictionary is badly scaled, ISTA crawls, so normalise its columns before you start.

### Pros and cons

**Pros:** the problem is convex, the step size 1/L guarantees the objective never increases, each iteration is two matrix products, and the soft threshold gives exact zeros.

**Cons:** plain ISTA converges slowly, at about 1/k. Computing the step needs the spectral norm of D, which is expensive for very large dictionaries. Lambda needs tuning, and the result depends on the scaling of D.

## Explanation

The solution computes the spectral norm once, runs the proximal gradient loop, and applies `soft_threshold` after each gradient step. Because the step matches the Lipschitz constant, the objective never increases.
