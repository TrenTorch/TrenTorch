---
name: research-sklearn-standard-scale
title: 'Scikit-learn: Standardizing Features'
tags: [research-papers, classical-ml, tooling, preprocessing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Many models, such as linear models and neural networks, train better when features are on similar scales. Standardization centers each feature and divides by its spread, so no feature dominates just because of its units.

### From theory to code

Implement `standard_scale(X)`, which centers each column and scales it to unit standard deviation.

### Constraints

- A constant column has standard deviation 0; return zeros for it.

### Hints

<details>
<summary>Hint 1</summary>

Compute the column means and standard deviations, guard zero deviations, then transform.

</details>

## Theory

### The simple version

After standardization, each feature has the same spread, so gradient-based and distance-based methods treat them comparably.

### The formula

$$z_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}$$

### How NumPy/PyTorch actually implements this

`sklearn.preprocessing.StandardScaler` fits and applies the same transform.

## Explanation

The mean and standard deviation come from the data passed in, which is why a real pipeline must fit them on training data only.
