---
name: unsupervised-pca-projection
title: 'PCA: projection'
tags: [classical-ml, unsupervised, dimensionality-reduction, pca]
difficulty: Intermediate
---

## Statement

Implement:

```python
def pca_fit(input: np.ndarray, n_components: int) -> dict: ...
def pca_transform(model: dict, input: np.ndarray) -> np.ndarray: ...
```

- `pca_transform` centers `input` using the _model's_ stored mean, not `input`'s own mean, `pca_transform` is meant to work on new data too, which shouldn't shift the projection's coordinate system.

## Theory

Every model so far reduces data to a prediction or a cluster assignment. PCA (Principal Component Analysis) does something different: it reduces the _number of features_, finding a small set of new directions in feature space that capture as much of the data's spread (variance) as possible, while throwing away the rest.

The key idea: after centering the data (subtracting the mean, so it's centered at the origin), the directions of maximum variance are exactly the directions Singular Value Decomposition (SVD) finds automatically. Decomposing the centered data matrix as `U @ diag(S) @ Vt`, the rows of `Vt` (called the right singular vectors) are, in order, the directions along which the data varies most, second-most, and so on. `n_components` of them, kept in that order, are PCA's "principal components."

```text
centered data
   ↓ SVD: centered = U @ diag(S) @ Vt
top n_components rows of Vt
   ↓ these ARE the principal components
project new data: (data - mean) @ components.T
```

`explained_variance`, `singular_value^2 / (n_samples - 1)`, is literally the variance of the (centered) data measured along that one direction, the same sample-variance formula used everywhere else, just computed along a rotated axis instead of an original feature axis. This is what "explains X% of the variance" means in a PCA plot: this one direction alone accounts for that much of the data's total spread.

SVD leaves one loose end: `Vt`'s rows are only defined up to a sign, `v` and `-v` are equally valid principal directions (they span the same line). Left unresolved, running PCA twice on the same data could give visibly "flipped" components for no real reason. Fixing a sign convention, make each component's largest-magnitude coefficient positive, removes that arbitrariness.

## Explanation

`pca_fit` centers `input` first (`mean = input.mean(axis=0)`, `centered = input - mean`), the SVD's directions are meaningless without centering, they'd otherwise partly describe "how far the data sits from the origin" instead of purely "how the data varies around its own center."

`np.linalg.svd(centered, full_matrices=False)` returns `(_, singular_values, components_t)`, `components_t[:n_components]` keeps only the top `n_components` rows, SVD already returns them sorted by singular value (largest first), so the "most variance first" ordering falls out for free.

The sign-fixing loop finds, per component row, the index of its largest-magnitude entry (`np.argmax(np.abs(components), axis=1)`), reads that entry's sign, and multiplies the whole row by it, flipping the row exactly when needed to make that one entry positive, leaving it unchanged otherwise.

`explained_variance = singular_values[:n_components]**2 / (n_samples - 1)` turns singular values into variances, the same `n-1` denominator (Bessel's correction) any sample variance uses.

`pca_transform` is one matrix multiply, `(input - model["mean"]) @ model["components"].T`, centering with the _stored_ mean (not `input`'s own), so that transforming the exact training data reproduces the projection PCA was fit on, and transforming new data lands in that same coordinate system.
