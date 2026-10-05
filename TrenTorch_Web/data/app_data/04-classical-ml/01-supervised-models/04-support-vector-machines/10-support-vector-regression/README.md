---
name: support-vector-machines-svr-gradient-descent
title: Support vector regression via gradient descent
tags: [classic-ml]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`Linear SVM via gradient descent on hinge loss` fits a classifier by minimizing hinge loss plus an L2 penalty. Support Vector Regression applies the same recipe to a real-valued target: swap hinge loss for the `Epsilon-insensitive loss` and keep the L2 penalty that keeps the weights small. Points inside the tube contribute no gradient, so only points outside it shape the fit.

Implement three functions with the exact signatures below. `epsilon_insensitive_loss` is imported from the previous question.

- `svr_objective(weight, bias, X, y, epsilon, lambda_reg)`: mean epsilon-insensitive loss of `X @ weight + bias` against `y`, plus `lambda_reg * ||weight||^2`.
- `svr_gradient(weight, bias, X, y, epsilon, lambda_reg)`: returns `(grad_weight, grad_bias)`.
- `train_linear_svr(X, y, lr=0.01, epochs=1000, epsilon=0.1, lambda_reg=0.0)`: plain gradient descent from zero weights and zero bias. Returns `(weight, bias)`.

### Constraints

- A residual inside the tube (`|prediction - target| <= epsilon`) contributes zero to the gradient.
- `svr_gradient` must match the true gradient of `svr_objective` away from the tube edges.
- Use the `sign` of the residual for points outside the tube.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Let `residual = X @ weight + bias - y`. The direction of the loss is `np.sign(residual)` where `np.abs(residual) > epsilon`, and zero elsewhere.

</details>

<details>
<summary>Hint 2</summary>

`grad_weight` is `X.T @ direction / n` plus `2 * lambda_reg * weight`, and `grad_bias` is `np.sum(direction) / n`.

</details>

## Theory

### The simple version

Each training point pulls the line toward itself only when it sits outside a band around the line. Points inside the band are ignored. Repeating that pull, one small step at a time, drives the line to the place where the band covers most of the data.

### The formula

$$
\text{svr\_objective} = \operatorname{mean}\left(\max(0, |r_i| - \varepsilon)\right) + \lambda \lVert w \rVert^2, \qquad r_i = x_i^\top w + b - y_i
$$

The gradient uses $s_i = \operatorname{sign}(r_i)$ for points outside the tube and $0$ inside it:

$$
\nabla_w = \frac{1}{n}\sum_i s_i\, x_i + 2\lambda w, \qquad \nabla_b = \frac{1}{n}\sum_i s_i
$$

## Explanation

`svr_gradient` builds the direction vector from the residuals, zeroing every point inside the tube, and averages it into the two gradient terms. `train_linear_svr` repeats that gradient step `epochs` times from zero, which is the same loop shape as the linear SVM question.
