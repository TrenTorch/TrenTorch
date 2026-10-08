---
name: research-shap-linear
title: 'SHAP: Linear Model Attributions'
tags: [research-papers, classical-ml, interpretability, shap]
difficulty: Beginner
---

## Statement

### The problem, from first principles

For a linear model with independent features, the Shapley value of a feature is its weight times how far its value is from the average. This gives a closed form that matches the exact computation, a useful check on the general method.

### From theory to code

Implement `linear_shap(w, x, mean)`, returning `w * (x - mean)` element-wise.

### Constraints

- `mean` is the average of each feature over background data.

### Hints

<details>
<summary>Hint 1</summary>

Subtract the means from the input, then multiply by the weights.

</details>

## Theory

### The simple version

A feature pushes the prediction up if its weight and its deviation from typical values have the same sign. Summing the terms gives back the full change from the average prediction.

### The formula

$$\phi_i = w_i\,(x_i - \mathbb{E}[x_i])$$

### How NumPy/PyTorch actually implements this

`shap.LinearExplainer` returns these values for a fitted linear model.

## Explanation

This is the result that connects SHAP to ordinary linear coefficients, and it is what the library uses for linear models.
