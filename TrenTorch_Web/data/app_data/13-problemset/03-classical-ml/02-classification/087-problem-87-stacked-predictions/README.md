---
name: problem-87-stacked-predictions
title: 'Stacked Predictions'
tags: [problemset, classical-ml-trees-ensembles, stacking]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'stacking'
hint: 'np.column_stack the model prediction vectors'
tools: [NumPy]
---

## Statement

Build the meta-feature matrix used to train the second-level model in stacking. `predictions` is a list with one prediction vector per base model, each of length `n_samples`.

Implement `solve(predictions)`.

**Returns.** Return a NumPy array of shape `(n_samples, n_models)` where column $j$ holds the predictions of base model $j$.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[[1.0, 3.0], [2.0, 4.0]]
```

**Example 2**

Input:

```python
solve([[0.1, 0.9, 0.5], [0.2, 0.8, 0.4], [0.0, 1.0, 0.6]])
```

Output:

```text
[[0.1, 0.2, 0.0], [0.9, 0.8, 1.0], [0.5, 0.4, 0.6]]
```

## Theory

### The simple version

Stacking uses the predictions of several base models as the _inputs_ of a final model, which learns how much to trust each one. To feed that model, the predictions have to be arranged so that each row is one sample and each column is one base model.

### The layout

$$Z_{ij}=\hat y^{(j)}_i,\qquad Z\in\mathbb R^{n\times M}$$

### Why it matters

- Stacking trains a second-level model on the predictions of base models.
- It needs one row per sample and one column per base model.

### How it works

1. Take the list of per-model prediction vectors.
2. Place them side by side as columns.

### Worked example

Two models predicting $(1,2)$ and $(3,4)$ become a matrix whose columns are those vectors: rows $(1,3)$ and $(2,4)$, i.e. [[1.0, 3.0], [2.0, 4.0]].

## Explanation

This is a transpose of the list-of-vectors layout. In a real pipeline the base predictions should come from cross-validation (out-of-fold), otherwise the second-level model sees overly optimistic inputs.
