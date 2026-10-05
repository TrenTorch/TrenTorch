---
name: manifold-pca-explained-variance-ratio
title: 'PCA explained variance ratio'
tags: [classical-ml, unsupervised, pca, dimensionality-reduction]
difficulty: Intermediate
---

## Statement

### How much variance does each component keep?

Before choosing how many principal components to keep, you need to know how much of the data's variance each one explains. Implement `explained_variance_ratio(X)`.

1. Center `X` by subtracting the column means.
2. Compute the singular values of the centered matrix with `np.linalg.svd`.
3. The variance along component i is s_i² / (n − 1). The ratio for component i is its variance divided by the total.
4. Return the ratios as a 1-D array sorted in descending order. They must sum to 1.

### Constraints

- `X` must have at least 2 rows, otherwise raise `ValueError`.
- If all columns are constant, return a zero array of length `min(n, d)`.
- Do not modify `X`.

### Hints

<details>
<summary>Hint 1</summary>

The squared singular values already come out in descending order.

</details>

## Theory

For centered data, the total variance equals the sum of squared singular values divided by n − 1. Each squared singular value is the variance captured by one principal direction, so the ratio is a direct share of total variance.

## Explanation

The solution centers the data, takes the SVD, and normalizes the squared singular values. Taking the SVD directly avoids forming the covariance matrix, which is more stable for wide or nearly collinear data.
