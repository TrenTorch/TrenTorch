---
name: distance-mahalanobis
title: 'Mahalanobis distance'
tags: [classical-ml, distance, mahalanobis, covariance, anomaly-detection]
difficulty: Intermediate
---

## Statement

### Measure distance in units of the data's own spread

The Mahalanobis distance between `x` and `y` under a covariance matrix `S` is `sqrt((x - y)^T S^-1 (x - y))`. It is Euclidean distance after whitening the data, so it accounts for feature scales and for correlations between features.

Implement `mahalanobis(x, y, cov)`.

- `x` and `y` are 1-D arrays of length `d`. `cov` is a `d` by `d` matrix.
- `cov` must be symmetric and positive definite. Check this with a Cholesky factorization, and return the distance as a float.

### Constraints

- `x` and `y` must have length `d`, and `cov` must be `d` by `d`. Otherwise raise `ValueError`.
- A `cov` that is not symmetric raises `ValueError`.
- A `cov` that is not positive definite raises `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

If `cov = L L^T` is the Cholesky factorization, then `z = L^-1 (x - y)` is the whitened difference, and the distance is `||z||`.

</details>

## Theory

Mahalanobis distance is the Euclidean distance in whitened coordinates, so it measures how many standard deviations apart two points are along each principal direction of the covariance. Because it uses the covariance, two points can be equally far in Euclidean terms but very different in Mahalanobis terms, if they sit on different sides of a correlated cloud. For a Gaussian, the squared distance from the mean follows a chi-square distribution with `d` degrees of freedom, which gives a principled cut-off.

### Where this shows up in production

Mahalanobis distance is a standard outlier score in multivariate process monitoring, where a factory or a data pipeline tracks several correlated sensors and raises an alert when a reading is far from normal. It is also used in fraud and intrusion detection on correlated transaction features, and in drift checks that compare a new batch against a reference covariance.

### Using it to make decisions

Use it when the features are correlated and roughly elliptical, and when the reference data is clean. Estimate the covariance on normal data only, and use shrinkage, such as Ledoit-Wolf, when the sample count is small relative to the feature count. Set the alert threshold from the chi-square quantile for the number of features, then check the false alarm rate on held-out normal data before deploying.

### Pros and cons

**Pros:** it handles correlated features and different scales together, the threshold has a clear statistical meaning, and the computation is one solve.

**Cons:** the covariance estimate is unstable when features are nearly collinear or the sample is small, and it is distorted by outliers in the reference set. It assumes an ellipsoidal shape, so multimodal or heavy-tailed data give misleading scores.

## Explanation

The solution checks shapes and symmetry, takes a Cholesky factor as the positive definiteness test, solves a triangular system for the whitened difference, and returns its norm. Using the factor directly avoids forming the inverse, which is slower and less accurate.
