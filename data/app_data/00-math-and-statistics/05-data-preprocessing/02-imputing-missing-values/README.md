---
name: math-imputing-missing-values
title: Imputing missing numeric values with a column mean/median
tags: [data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-detecting-missing-values` found the gaps. Now you need to fill them, most ML operations (a matrix multiply, a gradient computation, a distance calculation) simply cannot proceed with a `NaN` sitting in the middle of an array, it poisons every computation that touches it. The simplest reasonable fill-in value for a missing number is "whatever's typical for that column," and there are two natural choices for "typical": the mean, and the median.

The choice between them isn't arbitrary, it's the exact same distinction `02-summarizing-a-distribution` (the next track) makes between mean and median as measures of central tendency: one is sensitive to outliers, one isn't, and that sensitivity carries straight through into how good your imputed values end up being.

### From theory to code

Theory fills each missing value with its own COLUMN's mean or median, computed only from that column's actually-observed values (ignoring the missing ones, not accidentally treating them as zero). Implement both, reusing `01-detecting-missing-values`'s mask to find exactly where to write the fill-in values.

Implement `impute_with_mean(x)` and `impute_with_median(x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Neither function may mutate the input array `x`, work on a copy.
- Compute each column's mean/median from ONLY that column's non-missing values (`np.nanmean`/`np.nanmedian` do this automatically).
- A value's replacement must come from its OWN column, not some other column's statistic.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.nanmean(x, axis=0)` computes a length-`num_columns` array of column means, already ignoring NaNs, in one call.

</details>

<details>
<summary>Hint 2</summary>

`missing_mask(x)` (from `01-detecting-missing-values`) tells you exactly which positions to overwrite; `np.where(mask)` gives you the row and column index of each one.

</details>

## Theory

### The simple version

A survey has a few blank "age" answers. Before analyzing the data, you fill each blank with a reasonable stand-in, the AVERAGE age of everyone who DID answer, so the blank doesn't distort downstream calculations too badly. That's mean imputation. If one respondent accidentally wrote "999" for their age (a data-entry error), the average gets dragged upward by that single outlier, and every blank filled with that skewed mean inherits the distortion. The median doesn't have this problem, the "middle" value barely moves no matter how extreme a single outlier is.

### The formula

```text
impute_with_mean(x)[i, j]   = mean(x[:, j] excluding NaNs)     if x[i, j] is missing, else x[i, j]
impute_with_median(x)[i, j] = median(x[:, j] excluding NaNs)   if x[i, j] is missing, else x[i, j]
```

Mean imputation is the natural default: it preserves the column's overall average exactly (filling with the mean doesn't shift the mean). Median imputation is preferred when a column has outliers or a skewed distribution: `02-summarizing-a-distribution`'s comparison of mean vs median as central-tendency measures applies directly here, a single extreme value can drag a column's mean far from where "most" of its values actually sit, while the median stays robust.

Both are, importantly, a simplification: they assume "the typical value" is a reasonable guess for any missing entry, regardless of what else is known about that particular row. More sophisticated imputation strategies (not covered here) predict a missing value from a row's OTHER features instead, useful when a feature correlates strongly with others, but mean/median imputation remains the fast, simple default for a first pass.

### How PyTorch actually implements this

`sklearn.impute.SimpleImputer(strategy="mean")` (or `"median"`) is exactly this question, as a reusable, fit-then-transform pipeline stage: it learns each column's mean/median from a TRAINING set, then applies those SAME learned values to fill gaps in validation/test data too, never recomputing statistics from the test set itself (recomputing them would leak information about the test distribution into preprocessing, a subtle form of the data leakage `04-data-leakage`, later in this track, covers explicitly). PyTorch itself has no built-in imputation utilities, by the time data reaches a `Dataset`/`DataLoader`, it's expected to already be fully populated, exactly why this preprocessing step happens upstream, in the data pipeline, not inside the model.

## Explanation

`impute_with_mean` computes each column's mean via `np.nanmean(x, axis=0)` (already ignoring NaNs), finds every missing position via the imported `missing_mask`, and writes each missing position's own column's mean into it using fancy indexing (`np.where(mask)[1]` gives each missing entry's column index, used to look up the right mean via `np.take`).

`impute_with_median` follows the identical structure, substituting `np.nanmedian` for `np.nanmean`.
