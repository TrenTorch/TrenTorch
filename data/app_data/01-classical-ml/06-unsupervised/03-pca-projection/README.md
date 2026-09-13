---
name: unsupervised-pca-projection
title: 'PCA: projection'
tags: [classical-ml, unsupervised, dimensionality-reduction, pca]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every model up to `06-unsupervised` has reduced data to a prediction or, in `01-kmeans-assignment`/`02-kmeans-centroid-update`, a cluster label. PCA does something different: it reduces the number of _features_. A dataset with 100 columns might genuinely only vary along a handful of independent directions, with the rest being noise, redundancy, or correlated combinations of the columns you already have. PCA finds those few directions of real variation and lets you re-express every point using just those, throwing away directions the data barely moves along.

"Direction of most variation" needs a precise definition before it's code: it's the axis along which, if you projected every point onto it, the spread of those projected values would be largest. Finding that axis by trial and error doesn't scale past 2 features; the tool that finds it exactly, for any number of features, is the Singular Value Decomposition.

### From theory to code

Implement `pca_fit(input, n_components)`, which centers the data and runs SVD on it, keeping the top `n_components` directions it returns, and `pca_transform(model, input)`, which projects new data onto those directions. Theory below explains why SVD's output rows are exactly the directions of decreasing variance and how a singular value converts into "how much variance this direction explains"; the code is a direct readout of that decomposition plus one bookkeeping fix (the sign convention) so the same input always produces the same components.

### Constraints

- `pca_fit(input, n_components)` returns a dict with:
  - `"mean"`: shape `(n_features,)`, the training data's mean.
  - `"components"`: shape `(n_components, n_features)`, unit vectors, ordered by decreasing variance explained.
  - `"explained_variance"`: shape `(n_components,)`, the variance of the centered data along each component.
- Sign convention: for each component row, its largest-magnitude entry must be positive (flip the whole row if it isn't).
- `pca_transform(model, input)` returns shape `(n_samples, n_components)`.
- `pca_transform` centers `input` using the _model's_ stored mean, never `input`'s own mean — it must work correctly on data the model wasn't fit on.
- `n_components <= n_features`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

SVD only tells you about variance _around the origin_. If you skip centering, the "directions of maximum variance" you get back partly describe how far the data sits from `(0, 0, ...)`, not how it varies around its own center.

</details>

<details>
<summary>Hint 2</summary>

`np.linalg.svd(centered, full_matrices=False)` returns three things. The one you want the top rows of is already sorted largest-variance-first — no separate sort needed, just a slice.

</details>

<details>
<summary>Hint 3</summary>

For the sign fix: `np.argmax(np.abs(components), axis=1)` gives you, per row, the column index of the biggest-magnitude entry. Read that entry's sign with `np.sign(...)`, then multiply the whole row by it — a row whose biggest entry is already positive gets multiplied by `+1` and is unchanged.

</details>

## Theory

### The simple version

Picture a cloud of points shaped like a cigar, long in one direction and thin in the others. If you had to describe each point using only one number, the most informative choice is its position along the cigar's long axis — that's where almost all the actual variation lives, and it's much more useful than picking one of the original x/y/z axes at random, which might cut across the cigar and capture almost nothing. PCA is the general procedure for finding that "long axis" (and the next-longest, and the next) for a cloud of any shape and any number of dimensions.

### The formula

Center the data first: `mean = input.mean(axis=0)`, `centered = input - mean`. Decompose it:

```
centered = U @ diag(S) @ Vt
```

The rows of `Vt` are, in order, the directions of decreasing variance — the top `n_components` rows are the principal components:

```
components = Vt[:n_components]
explained_variance = S[:n_components]**2 / (n_samples - 1)
```

`S[:n_components]**2 / (n_samples - 1)` is the ordinary sample-variance formula (`n - 1` denominator, Bessel's correction), just computed along a rotated axis instead of an original feature axis.

Projecting any point (training or new) onto the fitted components:

```
projected = (input - mean) @ components.T
```

`Vt`'s rows are only defined up to sign (`v` and `-v` span the same line), so a deterministic convention is applied: for each row, find its largest-magnitude entry and flip the row's sign, if needed, so that entry is positive.

### How PyTorch actually implements this

`torch.linalg.svd` computes the same decomposition `np.linalg.svd` does here, and PCA via SVD is a standard, general technique — not specific to any one library. `tests.py` bakes a real reference from scikit-learn's `sklearn.decomposition.PCA` (computed offline and hardcoded as `expected_components`/`expected_variance`), which follows the same sign-flip convention implemented here (`svd_flip`), so this solution's output is checked against real library output, not just internal consistency.

## Explanation

`pca_fit` centers first: `mean = input.mean(axis=0)`, `centered = input - mean` (solution.py lines 5-6) — as Theory notes, SVD's directions are meaningless without this step. `np.linalg.svd(centered, full_matrices=False)` (line 8) unpacks to `(_, singular_values, components_t)`; the left singular vectors (`U`) aren't needed at all, hence the `_`. `components = components_t[:n_components]` (line 9) keeps only the top rows — SVD already returns them ordered by singular value, largest first, so "most variance first" falls out without an extra sort.

The sign-fixing block (lines 13-15) is the one piece of bookkeeping SVD doesn't hand you for free: `max_abs_idx = np.argmax(np.abs(components), axis=1)` finds, per component row, the index of its biggest-magnitude coefficient; `signs = np.sign(components[np.arange(...), max_abs_idx])` reads whether that coefficient is currently positive or negative; `components = components * signs[:, np.newaxis]` multiplies each row by its own sign, flipping exactly the rows that need it. `test_sign_convention_makes_the_largest_magnitude_entry_positive` checks this directly.

`explained_variance = (singular_values[:n_components] ** 2) / (n_samples - 1)` (line 18) converts singular values to variances with the same denominator every other sample-variance computation in this curriculum uses.

`pca_transform` (line 24) is one line: `(input - model["mean"]) @ model["components"].T`. Using `model["mean"]` rather than recomputing `input.mean(axis=0)` is what makes transforming the exact training data reproduce the fit-time projection and lets new data land in that same coordinate system — `test_transform_uses_the_fitted_mean_not_the_new_datas_own_mean` targets a mutant that gets this wrong.
