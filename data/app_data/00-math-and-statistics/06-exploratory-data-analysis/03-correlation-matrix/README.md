---
name: math-correlation-matrix
title: Correlation matrix, and why correlation is not causation
tags: [data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-probability/03-covariance-correlation` computed correlation between exactly two variables. A real dataset has dozens or hundreds of features, and the practical question is never just "are A and B related," it's "which PAIRS, among everything I have, are related, and how strongly." Checking every pair by hand doesn't scale, you need the full grid at once: every feature's correlation with every other feature, in one table.

That table, the correlation matrix, is one of the very first things a practitioner looks at when exploring a new dataset: it surfaces redundant features (two columns measuring almost the same thing), hints at which features might matter for a prediction target, and, done carelessly, tempts a very common and genuinely dangerous misinterpretation this question's Theory section exists specifically to head off.

### From theory to code

Theory generalizes `03-probability/03-covariance-correlation`'s single-pair formula to every pair at once: a symmetric matrix with `1.0` on the diagonal (each feature trivially correlates perfectly with itself) and the pairwise correlation everywhere else. Implement the full matrix by looping over every unique pair once (exploiting symmetry), then a helper that finds the single strongest off-diagonal relationship.

Implement `correlation_matrix(x)` and `most_correlated_pair(corr_matrix)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `x` is `(num_samples, num_features)`; the result is `(num_features, num_features)`.
- The diagonal is always exactly `1.0`.
- The matrix must be symmetric: `result[i, j] == result[j, i]`.
- `most_correlated_pair` excludes the diagonal and compares by absolute value (a strong negative correlation counts as "strongly related" too).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Loop `i` from `0` to `num_features`, and `j` from `i+1` to `num_features` (only the upper triangle), filling both `[i, j]` and `[j, i]` at once, exploiting symmetry to do half the work.

</details>

<details>
<summary>Hint 2</summary>

`np.fill_diagonal` (on a copy) can zero out the diagonal before searching for the maximum absolute off-diagonal value, so the trivial `1.0`s never win.

</details>

## Theory

### The simple version

A city's ice cream sales and its drowning incidents both rise every summer, and fall every winter. Plot them against each other and you'll find a strong positive correlation. Does buying ice cream cause drowning? Obviously not, both are driven by a third factor entirely: hot weather. This is THE classic illustration of "correlation is not causation": a strong correlation between A and B tells you they tend to move together, it tells you NOTHING about whether A causes B, B causes A, or (as here) some unmeasured C causes both.

### The formula

For a dataset `x` with `k` features, the correlation matrix is:

```text
corr_matrix[i, j] = correlation(x[:, i], x[:, j])
```

- The diagonal is always `1.0` (`correlation(x, x) = 1` for any feature with itself).
- The matrix is symmetric: `corr_matrix[i, j] == corr_matrix[j, i]`.
- Every entry falls in `[-1, 1]`, exactly `03-probability/03-covariance-correlation`'s own guarantee, applied to every pair at once.

The correlation matrix is a genuinely useful, legitimate tool for spotting REDUNDANT features (two columns with correlation near `+1` or `-1` are carrying almost the same information, one might be safely dropped) and for a first-pass look at which features might relate to a prediction target. What it can NEVER legitimately support on its own is a causal claim: "feature A correlates strongly with the label" does not mean changing A would change the label, `04-data-leakage` (the very next question in this track) covers an especially dangerous version of this trap, a feature that correlates almost perfectly with the label not because it's predictive, but because it accidentally encodes the label itself.

### How PyTorch actually implements this

`torch.corrcoef` computes exactly this matrix in one call (the batched, all-pairs-at-once version of `torch.corrcoef`'s two-variable cousin), and it's a standard first step in exploratory data analysis before ever building a model: heavily correlated input features can make a linear model's weights unstable (near-duplicate features fighting each other during optimization, a symptom of the "positive-definite Hessian" question's own concerns about ill-conditioned optimization), which is part of why techniques like PCA (`06-unsupervised`) are often applied first, to decorrelate features entirely before training. None of this machinery, in PyTorch or anywhere else, can ever turn a correlation into a causal claim, that requires a fundamentally different kind of analysis (controlled experiments, causal inference methods) outside what a correlation matrix alone can ever tell you.

## Explanation

`correlation_matrix` starts from an identity matrix (the diagonal `1.0`s, per Theory), then loops over each unique pair of columns `(i, j)` with `i < j`, computing `correlation(x[:, i], x[:, j])` via the imported function and writing it into both `[i, j]` and `[j, i]`, exploiting symmetry to compute each pair only once.

`most_correlated_pair` zeroes out a copy of the diagonal (so the trivial `1.0`s never win), then finds the index of the largest absolute value in what remains, converting the flat index back into a `(row, col)` pair via `np.unravel_index`.
