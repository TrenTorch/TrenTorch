---
name: research-xgboost-leaf-weight
title: 'XGBoost: The Optimal Leaf Weight'
tags: [research-papers, classical-ml, boosting, xgboost]
difficulty: Beginner
---

## Statement

### The problem, from first principles

XGBoost (Chen & Guestrin, 2016) fits each tree by minimizing a second-order approximation of the loss. For a leaf, the best prediction depends only on the summed gradients and hessians of the samples that fall into it.

### From theory to code

Implement `xgb_leaf_weight(G, H, lam)`, which returns the optimal leaf value `-G / (H + lam)`.

### Constraints

- `lam` is non-negative.

### Hints

<details>
<summary>Hint 1</summary>

Negate the gradient sum and divide by the hessian sum plus the regularizer.

</details>

## Theory

### The simple version

The leaf value is a Newton step: move against the gradient, scaled by the curvature. The regularizer `lam` keeps leaves with little curvature from taking huge steps.

### The formula

$$w^* = -\frac{\sum_{i \in I} g_i}{\sum_{i \in I} h_i + \lambda}$$

### How NumPy/PyTorch actually implements this

Gradient boosting libraries compute the same leaf value during tree construction.

## Explanation

This is the closed-form minimizer of the regularized second-order objective for a fixed tree structure.
