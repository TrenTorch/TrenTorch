---
name: research-shap-exact-shapley
title: 'SHAP: Exact Shapley Values'
tags: [research-papers, classical-ml, interpretability, shap]
difficulty: Advanced
---

## Statement

### The problem, from first principles

SHAP (Lundberg & Lee, 2017) explains a prediction by splitting it among the input features. The Shapley value of a feature is its average marginal contribution over every order in which features could be revealed, starting from a baseline.

### From theory to code

Implement `shapley_exact(f, x, baseline)`, which averages each feature's marginal contribution over all permutations.

### Constraints

- This is exact enumeration, so it is practical only for a few features.

### Hints

<details>
<summary>Hint 1</summary>

For each permutation, reveal features one at a time from the baseline and record how much each one changes the output. Average over permutations.

</details>

## Theory

### The simple version

Averaging over orderings is the only way to split the output fairly when features interact. The result also adds up to the full difference from the baseline, which the tests check.

### The formula

$$\phi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(|N| - |S| - 1)!}{|N|!}\big[f(S \cup \{i\}) - f(S)\big]$$

### How NumPy/PyTorch actually implements this

The `shap` library computes these values exactly for small models and approximates them for larger ones.

## Explanation

The permutation form is equivalent to the subset sum above, since each ordering corresponds to a chain of subsets.
