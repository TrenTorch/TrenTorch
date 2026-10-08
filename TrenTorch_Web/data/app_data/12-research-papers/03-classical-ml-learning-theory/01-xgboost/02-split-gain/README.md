---
name: research-xgboost-split-gain
title: 'XGBoost: The Split Gain'
tags: [research-papers, classical-ml, boosting, xgboost]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

XGBoost chooses splits by how much they reduce the regularized objective. The gain compares the score of the two children against the score of the parent, then subtracts a penalty for adding a leaf.

### From theory to code

Implement `xgb_split_gain(GL, HL, GR, HR, lam, gamma)`, returning the gain of a split minus `gamma`.

### Constraints

- The parent sums are the children sums added together.

### Hints

<details>
<summary>Hint 1</summary>

Compute each child's score `G^2 / (H + lam)`, subtract the parent's score, halve the result, then subtract `gamma`.

</details>

## Theory

### The simple version

A split is worth making when the children separate large gradients better than the parent does. The penalty `gamma` discourages splits that only help a little.

### The formula

$$\mathcal{G} = \frac{1}{2}\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma$$

### How NumPy/PyTorch actually implements this

The same expression is evaluated for every candidate threshold during histogram-based split search.

## Explanation

The gain is the objective reduction in the paper's split-finding algorithm, with the leaf weights already optimized.
