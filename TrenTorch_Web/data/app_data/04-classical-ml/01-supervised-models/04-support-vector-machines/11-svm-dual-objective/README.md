---
name: svm-dual-objective
title: 'The SVM dual objective'
tags: [classical-ml, svm, dual, kernel, optimization]
difficulty: Advanced
---

## Statement

### Score a set of dual variables and check they are legal

The soft-margin SVM can be solved in its dual form, where one variable `alpha_i` per training point carries the whole solution. The dual objective to maximize is `W(alpha) = sum(alpha) - 0.5 * sum_ij alpha_i alpha_j y_i y_j K_ij`, with labels `y_i` in `{-1, +1}` and kernel matrix `K`.

Implement two functions.

- `dual_objective(alpha, y, K)`: returns `W(alpha)` as a float. `alpha` and `y` have length `n` and `K` is an `n` by `n` kernel matrix.
- `is_dual_feasible(alpha, y, C, tol=1e-9)`: returns `True` when every `alpha_i` lies in `[0, C]` (within `tol`) and `sum(alpha_i * y_i)` is zero (within `tol`). Otherwise it returns `False`.

### Constraints

- `alpha` and `y` must have length `n`, and `K` must be `n` by `n`. Otherwise raise `ValueError`.
- `C < 0` raises `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

With `ay = alpha * y`, the quadratic term is `ay @ K @ ay`.

</details>

## Theory

Lagrangian duality turns the margin problem into a problem over `alpha`. Only points with `alpha_i > 0` affect the predictor, and those points are the support vectors. The data enters only through the kernel values `K_ij`, so any positive semidefinite kernel can replace the inner product. When `K` is positive semidefinite, `W` is concave, and the feasible set is a box with one linear equality. That structure is why the sequential minimal optimization (SMO) method can solve the problem two variables at a time.

### Where this shows up in production

Kernel SVMs are the classical solver behind libsvm and the `SVC` class in scikit-learn. At serving time the decision function sums kernel values against the support vectors only, so latency depends on how many `alpha_i` are nonzero. Teams use kernel SVMs for text and bioinformatics classification at tens of thousands of examples, where the kernel matrix still fits in memory.

### Using it to make decisions

Use the dual when the training set is small or medium and the decision boundary is clearly nonlinear. Watch the support vector count after training. If a noisy dataset produces a support vector for most points, serving gets slow, and a smaller `C` or a linear model is the fix. For millions of rows the `n` by `n` kernel matrix is out of reach, so switch to a linear model or to an approximate feature map.

### Pros and cons

**Pros:** the problem is convex, the solution is global, the predictor is sparse in the training points, and the kernel trick lets you model nonlinear structure without writing features by hand.

**Cons:** training memory and time grow with `n` squared or worse. The number of support vectors can grow with label noise, which makes inference slow. The dual gives no probabilities, so you need a calibration step, and the search over `C` and kernel parameters is expensive.

## Explanation

The objective is one linear term and one quadratic form built from the labels and the kernel. The feasibility check tests the two constraints of the dual, the box on each `alpha_i` and the balance equation on the signed sum. The check uses a small tolerance because solvers return values like `1e-12` past a bound.
