---
name: unsupervised-tsne-umap
title: 'Note: t-SNE and UMAP, nonlinear dimensionality reduction for visualization'
tags: [classical-ml, unsupervised, dimensionality-reduction, visualization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`03-pca-projection` reduces dimensionality by finding directions of maximum *variance* — a single global linear transformation applied identically everywhere. This works well when the data genuinely lies near a linear subspace, but many real datasets have structure PCA can't see: clusters that curve, spiral, or fold through high-dimensional space in ways no single set of straight-line directions captures.

### From theory to code

Implement `gaussian_affinities(input, sigma)`, which converts pairwise distances into a row-normalized similarity distribution — the core building block t-SNE uses to describe "how likely is point `j` to be point `i`'s neighbor" before it ever attempts any low-dimensional placement. Reuse `01-knn`'s `pairwise_distances`.

### Constraints

- `input`: shape `(n_samples, n_features)`. Returns shape `(n_samples, n_samples)`.
- Each row sums to `1` (a genuine probability distribution per point).
- The diagonal is always exactly `0` — a point is never its own neighbor.
- `sigma` controls how sharply affinity falls off with distance.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`exp(-distance^2 / (2*sigma^2))` is a Gaussian kernel: small distance gives a value near `1`, large distance decays toward `0`. Compute this on the full pairwise distance matrix at once.

</details>

<details>
<summary>Hint 2</summary>

Zero the diagonal *before* normalizing each row — otherwise `p[i,i]` (distance `0` to itself, always the largest possible similarity) would dominate the row and crowd out every real neighbor relationship.

</details>

## Theory

### The simple version

**t-SNE** (t-distributed Stochastic Neighbor Embedding) targets exactly the case PCA can't handle, for the specific purpose of 2D/3D visualization, not general-purpose feature reduction. Its core idea, in two stages:

1. In the original high-dimensional space, convert distances into a probability distribution over "how likely is point `j` to be `i`'s neighbor," a Gaussian centered on each point. This is `gaussian_affinities`, this question's implementation.
2. Place points in a low-dimensional space (2D, for a plot) and iteratively move them so that a *different* similarity distribution computed there (t-SNE uses a heavier-tailed Student-t distribution here, the "t" in t-SNE, which resists crowding points together) matches the high-dimensional one as closely as possible.

### The formula

Real t-SNE doesn't use one fixed `sigma` for the whole dataset the way this question does — it picks a different `sigma` per point via a search that targets a chosen **perplexity** (roughly, "how many effective neighbors should this point have"), so a point in a dense region gets a small `sigma` and a point in a sparse region gets a larger one. This question fixes `sigma` for one point to keep the implementation tractable — the affinity formula itself, converting squared distance into a normalized Gaussian similarity, is the real mechanism underneath.

**UMAP** (Uniform Manifold Approximation and Projection) is a newer, popular alternative built on different mathematical foundations (topology and manifold learning rather than probability matching), but it solves the same practical problem — project high-dimensional data into 2D for visualization while preserving local neighborhood structure — and in practice tends to run faster and preserve more of the data's global structure than t-SNE. Neither t-SNE nor UMAP is generally used as a preprocessing step before another model (unlike PCA); their output coordinates are for looking at, not for feeding into a classifier — the mapping isn't easily applied to new, unseen points the way `03-pca-projection`'s `pca_transform` is.

### How PyTorch actually implements this

Context only, untested by your submission: this is a classical statistical technique, not a PyTorch operation — the real-world equivalents are scikit-learn's `TSNE` and the standalone `umap-learn` library, both of which build on the same neighbor-affinity idea this exercise's `gaussian_affinities` implements (though real t-SNE's per-point, perplexity-targeted `sigma` search adds a layer this exercise's fixed-`sigma` version doesn't attempt).

## Explanation

`gaussian_affinities` computes the full pairwise distance matrix (`pairwise_distances(input, input)`), squares it and negates it inside a Gaussian kernel, `exp(-distance^2 / (2*sigma^2))` — small distance gives a value near `1` (very similar), large distance decays toward `0`.

`np.fill_diagonal(unnormalized, 0.0)` rules out a point being counted as its own neighbor — without this, `p[i,i]` would always be the largest value in row `i` (distance `0` to itself), dominating every real neighbor relationship.

Dividing each row by its own sum (`row_sums = unnormalized.sum(axis=1, keepdims=True)`) turns each row into a genuine probability distribution over "which other point is `i`'s neighbor," summing to `1` — this is the actual `p_{j|i}` quantity real t-SNE computes (asymmetrized and further processed in the real algorithm, but this is the core building block).
