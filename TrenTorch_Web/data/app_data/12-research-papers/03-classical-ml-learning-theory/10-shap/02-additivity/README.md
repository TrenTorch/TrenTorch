---
name: research-shap-additivity
title: 'SHAP: Checking Additivity'
tags: [research-papers, classical-ml, interpretability, shap]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

SHAP values must add up to the difference between the prediction and the baseline prediction. This check is the efficiency property of Shapley values, and it is a quick way to catch a bug in an attribution method.

### From theory to code

Implement `additivity_gap(phi, f_x, f_base)`, returning the sum of the attributions minus the output difference.

### Constraints

- Returns a Python float.

### Hints

<details>
<summary>Hint 1</summary>

Sum the attributions and subtract `f_x - f_base`.

</details>

## Theory

### The simple version

A non-zero gap means the explanation does not account for the full prediction. For exact Shapley values the gap is zero up to floating-point error.

### The formula

$$\sum_i \phi_i = f(x) - \mathbb{E}[f]$$

### How NumPy/PyTorch actually implements this

The `shap` library's checks compare the sum of values with the model output in the same way.

## Explanation

The efficiency axiom is what makes the attributions a decomposition rather than a set of unrelated scores.
