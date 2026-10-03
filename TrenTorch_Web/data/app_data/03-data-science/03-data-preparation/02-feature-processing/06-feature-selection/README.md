---
name: data-science-feature-selection
title: Feature Selection
tags: [data-science, feature-selection]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`05-feature-engineering` adds columns. Past some point more columns hurt: a feature that never changes carries no information, two features that move together carry the same information twice, and a pile of noisy features gives a model more ways to fit chance patterns in the training set. Feature selection removes columns before any model is trained, using cheap statistics of the data itself. This question builds three of the standard filters: drop columns that barely vary, drop one of each pair of near-duplicate columns, and keep only the columns most related to the label.

### From theory to code

Implement `variance_threshold(x, threshold)`, which finds the columns that vary enough, then `drop_correlated(x, threshold)`, which removes redundant columns, then `select_k_best(x, y, k)`, which ranks columns by how strongly they relate to the label. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 2D float array `(rows, columns)` with no missing values. `y` is a 1D float array with one entry per row.
- `variance_threshold` returns a boolean array of length `columns`, `True` where the column's population variance is strictly greater than `threshold`.
- `drop_correlated` returns the sorted list of column indices to keep. It scans columns left to right and keeps a column unless its absolute Pearson correlation with some already-kept column is strictly greater than `threshold`. A constant column has undefined correlation, which counts as `0`, so it is never dropped by this rule.
- `select_k_best` returns an integer array of the `k` column indices with the highest absolute Pearson correlation with `y`, ordered from strongest to weakest. Ties go to the lower column index. A constant column scores `0`. `k` is at most the number of columns.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

Correlation of two columns is the covariance divided by the product of the standard deviations. Compute the standard deviations once and treat a zero standard deviation as a correlation of zero instead of dividing by it.

</details>

<details>
<summary>Hint 2</summary>

For `drop_correlated`, the order of the scan decides which of two correlated columns survives: the earlier one always does.

</details>

<details>
<summary>Hint 3</summary>

`np.argsort` on the negated scores is stable, so equal scores keep their original column order, which is exactly the tie rule.

</details>

## Theory

### The simple version

Packing for a trip, you leave out the item you never use (it varies in no way that matters), one of two items that do the same job (a redundant pair) and the things unrelated to where you are going (not predictive of the goal). What is left is lighter to carry and loses nothing you needed. Feature selection is that packing list for a dataset, built from statistics rather than judgment.

### The formula

**Variance filter.** A column with population variance $\sigma_j^2 \le \tau$ is dropped, because a column that is nearly constant cannot help tell rows apart.

**Redundancy filter.** The Pearson correlation of columns $a$ and $b$ is

$$
r_{ab} = \frac{\operatorname{cov}(a, b)}{\sigma_a\,\sigma_b}
$$

and a column is dropped when $|r|$ with an already-kept column exceeds a threshold.

**Relevance filter.** Score each column by its absolute correlation with the label,

$$
\text{score}_j = \left| r_{x_j, y} \right|
$$

and keep the $k$ highest scores.

- All three are **filters**: they look at the data alone, not at a model, so they are fast and model-agnostic.
- Correlation only sees straight-line relationships. A feature related to the label through a curve can score near zero and be wrongly dropped.

### Filters, wrappers & embedded methods

Filters like these are the cheap first pass. **Wrapper** methods (forward selection, recursive feature elimination) train a model on candidate subsets and keep what scores best, which is more accurate and far more expensive. **Embedded** methods, such as an L1 penalty that drives weights to exactly zero or the importances of a tree ensemble, select features as a side effect of training.

### Selection belongs inside the training split

Scores that use the label, like the relevance filter, must be computed from the training rows only. Selecting the best features on the whole dataset and then splitting leaks information about the test labels into the choice of features, the same mistake as in `04-data-leakage`.

### How NumPy/PyTorch actually implements this

`sklearn.feature_selection.VarianceThreshold` is the variance filter, and `SelectKBest(score_func=f_regression, k=k)` ranks by a statistic that is a monotonic function of the squared correlation, so it picks the same columns. `np.corrcoef(x, rowvar=False)` gives the whole correlation matrix at once, which is the usual way to find redundant pairs. `sklearn.feature_selection.RFE` and `SelectFromModel` are the wrapper and embedded versions.

## Explanation

`variance_threshold` is `x.var(axis=0) > threshold`, using the population variance. `drop_correlated` standardizes the columns once, with a zero-standard-deviation column given a safe divisor so its correlations come out as zero, then walks the columns in order and keeps a column only if its absolute correlation with every previously kept column is at most the threshold. `select_k_best` computes the absolute correlation of every column with `y` the same way, and `np.argsort` of the negated scores with `kind="stable"` returns the strongest first with ties resolved toward lower indices; the first `k` are returned.
