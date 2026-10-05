---
name: feature-selection-chi-square-statistic
title: 'Chi-square statistic for a categorical feature'
tags: [classical-ml, feature-selection, filter-methods, chi-square]
difficulty: Beginner
---

## Statement

### Does this category tell us anything about the label?

A filter method scores each feature on its own, before any model is trained. For a categorical feature, the chi-square statistic compares how often each (category, label) pair actually occurs with how often it would occur if the feature and the label were independent.

Implement `chi2_statistic(x, y)`.

- `x` and `y` are one-dimensional integer arrays of the same length (category and label).
- Build the contingency table `O` with one row per distinct category of `x` and one column per distinct label of `y`.
- Expected counts are `E[i, j] = row_total[i] * col_total[j] / N`.
- Return `sum((O - E) ** 2 / E)` as a Python float.

### Constraints

- If `x` and `y` differ in length, or are empty, raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

`np.unique(..., return_inverse=True)` gives you the row and column index of every sample, and `np.add.at` fills the table.

</details>

## Theory

Under independence the statistic follows a chi-square distribution with `(rows - 1)(cols - 1)` degrees of freedom. As a filter score, a larger value means the category and the label are more strongly associated. The score ignores the model, so it is cheap, but it cannot see interactions between features.

### Where this shows up in production

Feature screening jobs on warehouse tables with hundreds of categorical columns, such as referral source, device type or plan tier against a conversion label. It runs as the first pass before any model is trained, so the cost of the whole screen is one contingency table per column.

### Using it to make decisions

Use it to drop columns that look independent of the label before you spend compute on them. Do not use it to rank columns with very different numbers of categories, because high-cardinality columns inflate the statistic. Check the expected count in every cell: a common rule is at least 5, and below that the chi-square approximation is unreliable. When you test thousands of columns, correct the p-values for multiple comparisons, otherwise a few hundred columns will look significant by chance.

### Pros and cons

**Pros:** one pass over the data, model-free, easy to explain to a non-technical reviewer, works on categorical data without encoding.

**Cons:** it is univariate, so it misses interactions and redundancy between features. It needs numeric features to be binned first, and the binning choice changes the answer. It is biased toward columns with many levels.

## Explanation

The solution builds the observed table with `np.add.at`, computes the expected table from its margins, and sums the normalized squared differences.
