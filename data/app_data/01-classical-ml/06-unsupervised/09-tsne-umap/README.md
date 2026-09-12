---
name: unsupervised-tsne-umap
title: 'Note: t-SNE and UMAP, nonlinear dimensionality reduction for visualization'
tags: [classical-ml, unsupervised, dimensionality-reduction, visualization]
difficulty: Beginner
---

## Statement

Implement:

```python
def gaussian_affinities(input: np.ndarray, sigma: float) -> np.ndarray:
    """Returns shape (n_samples, n_samples): a row-normalized similarity
    distribution, p[i, i] = 0."""
```

- Reuse `01-knn`'s `pairwise_distances`.

## Theory

`03-pca-projection` reduces dimensionality by finding directions of maximum _variance_, a single global linear transformation applied identically everywhere. This works well when the data genuinely lies near a linear subspace, but many real datasets have structure PCA can't see: clusters that curve, spiral, or fold through high-dimensional space in ways no single set of straight-line directions captures.

**t-SNE** (t-distributed Stochastic Neighbor Embedding) targets exactly this case, for the specific purpose of 2D/3D visualization, not general-purpose feature reduction. Its core idea, in two stages:

1. In the original high-dimensional space, convert distances into a probability distribution over "how likely is point `j` to be `i`'s neighbor," a Gaussian centered on each point. This is `gaussian_affinities`, this question's implementation.
2. Place points in a low-dimensional space (2D, for a plot) and iteratively move them so that a _different_ similarity distribution computed there (t-SNE uses a heavier-tailed Student-t distribution here, the "t" in t-SNE, which resists crowding points together) matches the high-dimensional one as closely as possible.

Real t-SNE doesn't use one fixed `sigma` for the whole dataset the way this question does, it picks a different `sigma` per point via a search that targets a chosen **perplexity** (roughly, "how many effective neighbors should this point have"), so a point in a dense region gets a small `sigma` and a point in a sparse region gets a larger one. This question fixes `sigma` for one point to keep the implementation tractable, the affinity formula itself, converting squared distance into a normalized Gaussian similarity, is the real mechanism underneath.

**UMAP** (Uniform Manifold Approximation and Projection) is a newer, popular alternative built on different mathematical foundations (topology and manifold learning rather than probability matching), but it solves the same practical problem, project high-dimensional data into 2D for visualization while preserving local neighborhood structure, and in practice tends to run faster and preserve more of the data's global structure than t-SNE. Neither t-SNE nor UMAP is generally used as a preprocessing step before another model (unlike PCA), their output coordinates are for looking at, not for feeding into a classifier, the mapping isn't easily applied to new, unseen points the way `03-pca-projection`'s `pca_transform` is.

## Explanation

`gaussian_affinities` computes the full pairwise distance matrix (`pairwise_distances(input, input)`), squares it and negates it inside a Gaussian kernel, `exp(-distance^2 / (2*sigma^2))`, small distance gives a value near `1` (very similar), large distance decays toward `0`.

`np.fill_diagonal(unnormalized, 0.0)` rules out a point being counted as its own neighbor, without this, `p[i,i]` would always be the largest value in row `i` (distance `0` to itself), dominating every real neighbor relationship.

Dividing each row by its own sum (`row_sums = unnormalized.sum(axis=1, keepdims=True)`) turns each row into a genuine probability distribution over "which other point is `i`'s neighbor," summing to `1`, this is the actual `p_{j|i}` quantity real t-SNE computes (asymmetrized and further processed in the real algorithm, but this is the core building block).
