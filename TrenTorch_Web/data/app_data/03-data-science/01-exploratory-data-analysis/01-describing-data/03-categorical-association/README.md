---
name: data-science-categorical-association
title: Categorical Association
tags: [data-science, eda, statistics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-correlation-matrix` measures how two numeric columns move together. It cannot say anything about two categorical columns such as device type and subscription plan, because there is no order and no arithmetic to correlate. The tool for them starts from a **contingency table**: a grid counting how many rows fall in each combination of the two categories. If the two columns are unrelated, the counts in the grid follow a predictable pattern, and how far the real counts depart from that pattern is a measure of association. This question builds the table, the departure measure (the chi-square statistic) and a normalized strength score between 0 and 1.

### From theory to code

Implement `contingency_table(a, b)`, which counts the rows in every combination of categories, then `expected_counts(table)`, the counts that independence would predict, then `chi_square_statistic(table)`, the total departure from them, then `cramers_v(table)`, the departure rescaled to a 0-to-1 strength. The signatures and docstrings are already in the editor.

### Constraints

- `a` and `b` are 1D arrays of hashable labels of the same length. `contingency_table` returns an integer 2D array whose rows are the sorted unique labels of `a` and whose columns are the sorted unique labels of `b`, with entry `(i, j)` the number of rows where `a` is the `i`-th label and `b` is the `j`-th.
- `expected_counts(table)` returns a float array of the same shape where entry `(i, j)` is `row_total_i * column_total_j / grand_total`.
- `chi_square_statistic(table)` returns the sum over all cells of `(observed - expected) ** 2 / expected` as a float. Cells with expected count `0` are skipped.
- `cramers_v(table)` returns `sqrt(chi2 / (n * min(r - 1, c - 1)))` for a table with `r` rows, `c` columns and grand total `n`. It returns `0.0` when `min(r - 1, c - 1)` is `0` or `n` is `0`.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

If rows and columns are independent, the share of each row total that lands in a column equals that column's share of the grand total, which is exactly what `row_total * column_total / grand_total` encodes.

</details>

<details>
<summary>Hint 2</summary>

Chi-square grows with the sample size even when the strength of the relationship stays the same. Dividing by `n` and by the number of free rows or columns is what makes Cramer's V comparable across datasets.

</details>

<details>
<summary>Hint 3</summary>

Building the table is two `np.unique(..., return_inverse=True)` calls followed by `np.add.at` on a zero array.

</details>

## Theory

### The simple version

If device type has nothing to do with plan choice, then a plan with 30% of the customers should hold about 30% of the phone users, 30% of the laptop users and 30% of the tablet users. Real counts will wobble around that. A relationship shows up as counts that miss the pattern by more than wobble: one plan holding 60% of the phone users and 10% of the laptop users. The chi-square statistic adds up all those misses, scaled so that a miss on a small cell counts for more.

### The formula

Given observed counts $O_{ij}$ with row totals $R_i$, column totals $C_j$ and grand total $n$, independence predicts

$$
E_{ij} = \frac{R_i\,C_j}{n}
$$

and the **chi-square statistic** is the total scaled departure:

$$
\chi^2 = \sum_{i,j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}
$$

**Cramer's V** rescales it to the range $[0, 1]$:

$$
V = \sqrt{\frac{\chi^2}{n\,\min(r - 1,\; c - 1)}}
$$

- $V = 0$ means the counts match independence exactly and $V = 1$ means one column determines the other.
- The statistic has $(r - 1)(c - 1)$ degrees of freedom. Comparing $\chi^2$ to the chi-square distribution with that many degrees gives a p-value for the hypothesis of independence.

### What association does & does not say

A large $V$ says the two columns are related, not why. It carries no direction (V is always non-negative) and no causal claim, the same caution as for correlation. It is also sensitive to tiny cells: when expected counts fall below about 5 the chi-square approximation becomes unreliable, and rare categories are usually merged first.

### Use in feature work

Cramer's V between each categorical feature and the label is a quick relevance filter, as absolute correlation is for numeric features in `06-feature-selection`. Between two features it flags redundancy, so one of a near-duplicate pair can be dropped.

### How NumPy/PyTorch actually implements this

`pandas.crosstab(a, b)` builds the contingency table in one call. `scipy.stats.chi2_contingency(table)` returns the statistic, the p-value, the degrees of freedom and the expected counts, and `scipy.stats.contingency.association(table, method='cramer')` computes Cramer's V directly. With `correction=False` the statistic matches the plain formula used here; by default SciPy applies Yates' correction to 2 by 2 tables.

## Explanation

`contingency_table` maps each label to its sorted-unique index with `np.unique(..., return_inverse=True)` and accumulates one count per row into a zero matrix with `np.add.at`, which gives the table with sorted row and column labels. `expected_counts` is the outer product of the row totals and column totals divided by the grand total. `chi_square_statistic` sums `(O - E)^2 / E` over every cell whose expected count is positive, avoiding a division by zero for an empty row or column. `cramers_v` divides that statistic by `n` times the smaller of `rows - 1` and `columns - 1` and takes the square root, returning zero for a degenerate table where there is no variation to measure.
