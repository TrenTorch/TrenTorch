---
name: math-missing-values
title: 'Detecting & Imputing Missing Values'
tags: [data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

**Detecting missing values**

Real datasets are never as clean as the small, hand-picked arrays this curriculum's Math & Statistics tracks used, a survey respondent skips a question, a sensor drops a reading, a merge between two tables leaves some rows without a match. Before anything else, `03-mse-gradient`, PCA, a Gaussian's MLE, all assume every entry of the data actually holds a real number, a single missing value silently poisons a mean, a covariance, a gradient, everywhere it touches.

The very first, unglamorous step of any real ML pipeline is knowing exactly where the gaps are, before deciding what to do about them (`02-imputing-missing-values`, the next question, is that "what to do about them" step). This question is purely about detection: finding missing entries reliably, a surprisingly easy thing to get subtly wrong.

**Imputing missing values**

`01-detecting-missing-values` found the gaps. Now you need to fill them, most ML operations (a matrix multiply, a gradient computation, a distance calculation) simply cannot proceed with a `NaN` sitting in the middle of an array, it poisons every computation that touches it. The simplest reasonable fill-in value for a missing number is "whatever's typical for that column," and there are two natural choices for "typical": the mean, and the median.

The choice between them isn't arbitrary, it's the exact same distinction `02-summarizing-a-distribution` (the next track) makes between mean and median as measures of central tendency: one is sensitive to outliers, one isn't, and that sensitivity carries straight through into how good your imputed values end up being.

### From theory to code

**Detecting missing values**

Theory names the standard representation for a missing numeric value (`np.nan`) and flags the single most common bug in detecting it (`== np.nan` never works, by design). Implement a boolean mask using the correct tool, then column-wise counts and fractions built directly from that mask.

Implement `missing_mask(x)`, `missing_count_per_column(x)` and `missing_fraction_per_column(x)` against that reasoning. The signatures and docstrings are already in the editor.

**Imputing missing values**

Theory fills each missing value with its own COLUMN's mean or median, computed only from that column's actually-observed values (ignoring the missing ones, not accidentally treating them as zero). Implement both, reusing `01-detecting-missing-values`'s mask to find exactly where to write the fill-in values.

Implement `impute_with_mean(x)` and `impute_with_median(x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

**Detecting missing values**

- `x` is a 2D float array, `(num_rows, num_columns)`, missing values represented as `np.nan`.
- Use `np.isnan`, never `== np.nan` (Theory explains exactly why the latter silently fails).
- `missing_fraction_per_column` returns fractions in `[0.0, 1.0]`, one per column.

**Imputing missing values**

- Neither function may mutate the input array `x`, work on a copy.
- Compute each column's mean/median from ONLY that column's non-missing values (`np.nanmean`/`np.nanmedian` do this automatically).
- A value's replacement must come from its OWN column, not some other column's statistic.

### Hints

**Detecting missing values**

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.isnan(x)` already returns a same-shaped boolean mask directly, no comparison operator needed.

</details>

<details>
<summary>Hint 2</summary>

Once you have the mask, `missing_count_per_column` is `.sum(axis=0)` (summing down each column, over all rows).

</details>

**Imputing missing values**

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

**Detecting missing values**

Imagine a paper survey with some blank boxes, a respondent skipped a question, or the handwriting was illegible and got discarded. Before you can analyze the survey at all, you need to know exactly which boxes are blank, you can't compute "average age of respondents" correctly if some age entries are silently blank and you don't know it.

**Imputing missing values**

A survey has a few blank "age" answers. Before analyzing the data, you fill each blank with a reasonable stand-in, the AVERAGE age of everyone who DID answer, so the blank doesn't distort downstream calculations too badly. That's mean imputation. If one respondent accidentally wrote "999" for their age (a data-entry error), the average gets dragged upward by that single outlier, and every blank filled with that skewed mean inherits the distortion. The median doesn't have this problem, the "middle" value barely moves no matter how extreme a single outlier is.

### The formula

**Detecting missing values**

Missing numeric values are conventionally represented as `np.nan` ("Not a Number"), a special floating-point value with one deeply counterintuitive property: it never equals anything, not even itself.

```text
np.nan == np.nan  ->  False  (!)
x == np.nan        ->  always False, for any x, silently
```

This is why `np.isnan(x)` exists as a dedicated function rather than relying on `==`: it's the only reliable way to ask "is this value NaN," checking the value's actual bit pattern rather than comparing it.

Once you have a boolean mask of where the missing values are, counting and fractioning are straightforward reductions:

$$
\text{missing\_count}_j = \sum_i \text{mask}_{ij} \qquad \text{missing\_fraction}_j = \frac{\text{missing\_count}_j}{\text{num\_rows}}
$$

**Imputing missing values**

$$
\text{impute\_with\_mean}(x)_{ij} =
\begin{cases}
\operatorname{mean}\big(x_{:,j} \setminus \text{NaN}\big) & \text{if } x_{ij} \text{ is missing} \\
x_{ij} & \text{otherwise}
\end{cases}
$$

$$
\text{impute\_with\_median}(x)_{ij} =
\begin{cases}
\operatorname{median}\big(x_{:,j} \setminus \text{NaN}\big) & \text{if } x_{ij} \text{ is missing} \\
x_{ij} & \text{otherwise}
\end{cases}
$$

Mean imputation is the natural default: it preserves the column's overall average exactly (filling with the mean doesn't shift the mean). Median imputation is preferred when a column has outliers or a skewed distribution: `02-summarizing-a-distribution`'s comparison of mean vs median as central-tendency measures applies directly here, a single extreme value can drag a column's mean far from where "most" of its values actually sit, while the median stays robust.

Both are, importantly, a simplification: they assume "the typical value" is a reasonable guess for any missing entry, regardless of what else is known about that particular row. More sophisticated imputation strategies (not covered here) predict a missing value from a row's OTHER features instead, useful when a feature correlates strongly with others, but mean/median imputation remains the fast, simple default for a first pass.

### Try it live

**Detecting missing values**

<div class="tt-widget" data-widget="math-detecting-missing-values"></div>

**Imputing missing values**

<div class="tt-widget" data-widget="math-imputing-missing-values"></div>

### How NumPy/PyTorch actually implements this

**Detecting missing values**

`pandas.DataFrame.isna()` (the real-world tool most practitioners actually reach for before ever touching NumPy directly) is built on exactly this `np.isnan`-style check, extended to handle non-numeric missing markers too (`None`, `pd.NaT` for missing dates). PyTorch itself has no first-class "missing value" concept, tensors are expected to be fully populated by the time they reach a model, which is precisely why this detection-and-handling step (this question, plus `02-imputing-missing-values`) has to happen during data preparation, upstream of ever constructing a tensor, `torch.isnan(tensor)` exists mainly for debugging (catching NaN values that leaked in from a numerical instability during training, like a loss that diverged), not for handling genuinely missing input data.

**Imputing missing values**

`sklearn.impute.SimpleImputer(strategy="mean")` (or `"median"`) is exactly this question, as a reusable, fit-then-transform pipeline stage: it learns each column's mean/median from a TRAINING set, then applies those SAME learned values to fill gaps in validation/test data too, never recomputing statistics from the test set itself (recomputing them would leak information about the test distribution into preprocessing, a subtle form of the data leakage `04-data-leakage`, later in this track, covers explicitly). PyTorch itself has no built-in imputation utilities, by the time data reaches a `Dataset`/`DataLoader`, it's expected to already be fully populated, exactly why this preprocessing step happens upstream, in the data pipeline, not inside the model.

## Explanation

**Detecting missing values.** `missing_mask` calls `np.isnan(x)` directly, the correct detection tool from Theory.

`missing_count_per_column` sums that mask along `axis=0` (down each column, across every row), giving one count per column.

`missing_fraction_per_column` divides that count by `x.shape[0]` (the total row count), turning raw counts into fractions.

**Imputing missing values.** `impute_with_mean` computes each column's mean via `np.nanmean(x, axis=0)` (already ignoring NaNs), finds every missing position via the imported `missing_mask`, and writes each missing position's own column's mean into it using fancy indexing (`np.where(mask)[1]` gives each missing entry's column index, used to look up the right mean via `np.take`).

`impute_with_median` follows the identical structure, substituting `np.nanmedian` for `np.nanmean`.
