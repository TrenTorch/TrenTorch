---
name: research-xgboost-logistic-grads
title: 'XGBoost: Gradients and Hessians for Logistic Loss'
tags: [research-papers, classical-ml, boosting, xgboost]
difficulty: Beginner
---

## Statement

### The problem, from first principles

To use cross-entropy loss inside boosting, XGBoost needs the first and second derivatives of the loss with respect to each sample's raw score. For logistic loss those derivatives have a short closed form.

### From theory to code

Implement `xgb_logistic_grad_hess(y, p)`, returning the gradient `p - y` and the hessian `p (1 - p)`.

### Constraints

- `p` is a probability between 0 and 1.

### Hints

<details>
<summary>Hint 1</summary>

The gradient is the prediction error, and the hessian is the variance of a Bernoulli with probability `p`.

</details>

## Theory

### The simple version

The gradient pushes the score toward the label. The hessian is largest where the model is most uncertain, so those samples get the biggest leaf weights per unit of gradient.

### The formula

$$g_i = p_i - y_i, \qquad h_i = p_i(1 - p_i), \qquad p_i = \sigma(\hat{y}_i)$$

### How NumPy/PyTorch actually implements this

XGBoost's `binary:logistic` objective computes exactly these two arrays on every boosting round.

## Explanation

The formulas come from differentiating the log loss through the sigmoid, which gives an error term and a curvature term.
