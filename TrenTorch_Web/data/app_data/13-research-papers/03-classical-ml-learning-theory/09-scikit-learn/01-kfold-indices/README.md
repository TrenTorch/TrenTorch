---
name: research-sklearn-kfold
title: 'Scikit-learn: K-Fold Cross-Validation Splits'
tags: [research-papers, classical-ml, tooling, validation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Scikit-learn (Pedregosa et al., 2011) makes model selection reproducible with cross-validation utilities. K-fold splits the data into k parts; each part serves once as the test set while the others train the model.

### From theory to code

Implement `kfold_indices(n, k)`, returning the train and test indices for each of the k folds.

### Constraints

- Use contiguous folds from `np.array_split`.

### Hints

<details>
<summary>Hint 1</summary>

Split `arange(n)` into k parts, then for each part use it as the test set and the rest as train.

</details>

## Theory

### The simple version

Every sample is tested exactly once, so the average score uses all the data for evaluation without any leakage between training and test.

### The formula

$$\bigcup_{i=1}^{k} \text{test}_i = \{0, \ldots, n-1\}, \qquad \text{test}_i \cap \text{test}_j = \emptyset$$

### How NumPy/PyTorch actually implements this

`sklearn.model_selection.KFold(n_splits=k).split(X)` yields the same index pairs.

## Explanation

The split logic is the core of `sklearn.model_selection.KFold` without shuffling.
