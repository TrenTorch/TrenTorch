---
name: problem-82-xgboost-style-leaf-weight
title: 'XGBoost-Style Leaf Weight'
tags: [problemset, classical-ml-trees-ensembles, regularized-boosting]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'regularized boosting'
hint: '-G / (H + lam)'
tools: [NumPy]
---

## Statement

Compute the optimal leaf weight in XGBoost-style gradient boosting from the sum of gradients `G`, the sum of Hessians `H` of the samples in the leaf, and the L2 regularisation strength `lam`.

Implement `solve(G,H,lam)`.

**Returns.** Return the weight as a float, $w^*=-G/(H+\lambda)$.

### Examples

**Example 1**

Input:

```python
solve(-4.0, 3.0, 1.0)
```

Output:

```text
1.0
```

**Example 2**

Input:

```python
solve(2.0, 1.0, 3.0)
```

Output:

```text
-0.5
```

## Theory

### The simple version

XGBoost approximates the loss around the current prediction with a quadratic. For one leaf the best constant to add is the minimum of that quadratic. The regulariser $\lambda$ in the denominator shrinks the leaf value, especially for leaves with little curvature (few samples).

### The derivation

Minimising $Gw+\tfrac12(H+\lambda)w^2$ over $w$ gives

$$w^*=-\frac{G}{H+\lambda}$$

## Explanation

The sign is opposite to the summed gradient, which is steepest descent. Larger $\lambda$ pulls $w^*$ toward $0$. The Hessian sum $H$ acts as a confidence: leaves backed by many samples are shrunk less.
