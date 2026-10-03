---
name: data-science-missingness-patterns
title: Missingness Patterns
tags: [data-science, data-cleaning]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-missing-values` finds the gaps in a dataset and fills them with a column average. That treats every gap the same, and the right treatment depends on why the value is missing. If a sensor drops readings at random, filling with the mean is harmless. If it drops readings mostly on hot days, the missing rows are systematically different from the rest, and filling them with the overall mean quietly biases every model trained on the result. This question builds the checks that tell those cases apart, and the indicator column that lets a model use the fact that a value was missing.

### From theory to code

Implement `missingness_rate_by_group(x, groups)`, the fraction of missing values within each group, then `mean_by_missingness(target, other)`, the average of another column split by whether the target is missing, then `likely_mechanism(target, other, threshold)`, a rough verdict on whether the gaps look random, then `add_missing_indicators(x)`, which appends a 0/1 flag column for every column that has gaps. The signatures and docstrings are already in the editor.

### Constraints

- Missing values are `np.nan`. `x`, `target` and `other` are float arrays; `groups` is a 1D array of any hashable labels with the same length as `x`.
- `missingness_rate_by_group` returns a dict mapping every label that appears in `groups` to the fraction of that group's entries that are missing. A group whose entries are all present has rate `0.0`.
- `mean_by_missingness` returns `(mean_when_observed, mean_when_missing)` as floats, where each is the mean of `other` over the rows where `target` is present or missing. `other` has no missing values. If either set of rows is empty, that mean is `nan`.
- `likely_mechanism` returns `"MCAR-like"` when the absolute gap between the two means, divided by the standard deviation of `other` over all rows, is below `threshold` and `"MAR-like"` otherwise. It returns `"MCAR-like"` when there are no missing values at all, and when `other` has zero standard deviation.
- `add_missing_indicators` returns a new 2D array: the original columns unchanged (with their `nan`), followed by one column of `1.0`/`0.0` flags for each original column that contains at least one missing value, in the original column order. Columns with no gaps get no flag. `x` must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

A boolean mask from `np.isnan` splits the rows of `other` into two groups. The two means being close is what "the gaps do not depend on `other`" looks like in the data.

</details>

<details>
<summary>Hint 2</summary>

Dividing the gap between the two means by the spread of `other` makes the comparison unit-free, so the same threshold works for a column measured in dollars or in degrees.

</details>

<details>
<summary>Hint 3</summary>

To build the indicators, find which columns have any missing value first, then stack their masks (converted to floats) to the right of the original array.

</details>

## Theory

### The simple version

Imagine a survey where some people skip the income question. If they skip it at random, the people who answered are a fair sample of everyone. If high earners are the ones who skip it, the answers you have are skewed low, and no amount of averaging fixes that. Looking at _who_ skipped, rather than just _how many_, is how you find out which situation you are in.

### The formula

Statisticians name three mechanisms, by what the chance of a value being missing depends on:

| Mechanism                               | Missing chance depends on | Effect of ignoring it                                |
| --------------------------------------- | ------------------------- | ---------------------------------------------------- |
| **MCAR** (completely at random)         | nothing                   | rows are a fair sample; mean fill is mostly harmless |
| **MAR** (at random given other columns) | other observed columns    | biased unless you use those columns                  |
| **MNAR** (not at random)                | the missing value itself  | biased and not fixable from the data alone           |

A quick diagnostic for MAR compares another column across the two groups. If `target` is missing independently of `other`, then

$$
\mathbb{E}[\text{other} \mid \text{target missing}] \approx \mathbb{E}[\text{other} \mid \text{target observed}]
$$

and the standardized gap

$$
d = \frac{\left| \bar{o}_{\text{obs}} - \bar{o}_{\text{miss}} \right|}{s_{\text{other}}}
$$

is small. A large $d$ means missingness tracks `other`, so the gaps are MAR-like.

### Why MNAR cannot be detected here

If high earners skip the income question _because_ they are high earners, the only column that could reveal it is income itself, and those values are exactly the ones that are gone. No comparison of observed data can prove MNAR or rule it out. It has to be argued from how the data was collected, which is why data documentation matters.

### Missing indicators

Sometimes the fact that a value is missing is itself informative: a loan applicant who leaves the income field blank behaves differently from one who fills it in. Appending a 0/1 flag column for each gappy column lets a model learn that, while the original column (after imputation) keeps its usual meaning. The flag costs one extra column and never throws information away.

### How NumPy/PyTorch actually implements this

`pandas.DataFrame.isna().groupby(...).mean()` computes the per-group missing rate in one line, and `pandas.isna` is `np.isnan` for mixed types. `sklearn.impute.SimpleImputer(add_indicator=True)` and `sklearn.impute.MissingIndicator` produce exactly the flag columns built here. `missingno` and similar libraries draw the nullity patterns visually. The statistical test of MCAR (Little's test) compares group means across all missingness patterns at once.

## Explanation

`missingness_rate_by_group` loops over the unique labels, takes the rows of `x` in each group and averages `np.isnan` over them, which is the fraction missing. `mean_by_missingness` builds the missing mask once and averages `other` over the rows where it is true and where it is false, returning `nan` for an empty side rather than raising. `likely_mechanism` turns the two means into the standardized gap `d` from Theory and compares it to `threshold`; the guards for no missing values and zero spread return `"MCAR-like"` because there is no evidence of dependence in either case. `add_missing_indicators` finds the columns with at least one `nan`, converts their masks to floats and uses `np.hstack` to append them after the untouched original columns, so the output never aliases or modifies `x`.
