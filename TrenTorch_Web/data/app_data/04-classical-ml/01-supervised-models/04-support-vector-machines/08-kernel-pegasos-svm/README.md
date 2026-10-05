---
name: support-vector-machines-kernel-pegasos
title: Kernel SVM with Pegasos
tags: [classic-ml]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Linear SVM via gradient descent on hinge loss` trains a weight vector directly, which only works while the decision boundary is a hyperplane in the original feature space. A kernel SVM never forms that weight vector. Instead it keeps one coefficient per training point, and the decision function is a kernel-weighted vote of those points. Any kernel from the previous four questions can drive it.

Pegasos is a stochastic sub-gradient method for the SVM objective. Here it runs in a deterministic form: at step `t` it visits training point `i = (t - 1) mod n`, checks whether that point violates the margin under the current model, and if it does, increments that point's coefficient. The coefficient counts how many times the point has caused an update, so the final vector is a list of non-negative integers.

Given a precomputed Gram matrix `K` of shape `(n, n)`, labels `y` in `{-1, +1}`, a regularization strength `lam`, and a number of iterations `T`, return the coefficient vector `alpha` of shape `(n,)`.

### Constraints

- Return a float array of shape `(n,)`.
- At each step `t` from `1` to `T`, let `i = (t - 1) % n` and compute the decision value `decision = sum_j alpha_j * y_j * K[j, i] / (lam * t)`.
- If `y_i * decision < 1`, increase `alpha_i` by `1`. Otherwise leave every coefficient unchanged.
- The model's prediction for a new point with kernel row `k` is `sign(sum_j alpha_j * y_j * k_j)`, which the tests use directly.
- `iterations = 0` returns all zeros.
- Do not modify `K` or `y`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`(alpha * y) @ K[:, i]` computes the numerator of the decision value in one line.

</details>

<details>
<summary>Hint 2</summary>

Check the margin before updating. A point that is already comfortably correct must not change its coefficient, which is what keeps the number of support points small.

</details>

## Theory

### The simple version

The kernel SVM asks each training point, one at a time, whether the current model gets it right with a comfortable margin. If not, that point gets a vote added to its coefficient. Points that are already correct never get a vote, so after enough passes the coefficients are nonzero only for the points that matter, the support vectors.

### The formula

With Gram matrix $K$, the decision function is

$$
f(x) = \frac{1}{\lambda t} \sum_j \alpha_j\, y_j\, k(x_j, x)
$$

where the $\frac{1}{\lambda t}$ scale comes from the Pegasos step size. The hinge-loss sub-gradient step for a violating point $i$ at step $t$ adds one unit to its coefficient, and a point is violating when $y_i f(x_i) < 1$.

The scale does not change the sign of $f$, so the prediction only depends on the sum. It does change which points violate the margin, so the scale stays in the update rule.

## Explanation

`kernel_pegasos` loops over `t` from `1` to `iterations`, picks the point `(t - 1) % n`, and computes its decision value from the current coefficients and column `K[:, i]`. It increments that coefficient only when the margin is violated, which is the update rule from Constraints. The loop is deterministic, so the same inputs always give the same coefficients.
