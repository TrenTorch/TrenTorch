---
name: math-detecting-missing-values
title: Detecting and counting missing values in a dataset
tags: [data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Real datasets are never as clean as the small, hand-picked arrays this curriculum's Math & Statistics tracks used, a survey respondent skips a question, a sensor drops a reading, a merge between two tables leaves some rows without a match. Before anything else, `03-mse-gradient`, PCA, a Gaussian's MLE, all assume every entry of the data actually holds a real number, a single missing value silently poisons a mean, a covariance, a gradient, everywhere it touches.

The very first, unglamorous step of any real ML pipeline is knowing exactly where the gaps are, before deciding what to do about them (`02-imputing-missing-values`, the next question, is that "what to do about them" step). This question is purely about detection: finding missing entries reliably, a surprisingly easy thing to get subtly wrong.

### From theory to code

Theory names the standard representation for a missing numeric value (`np.nan`) and flags the single most common bug in detecting it (`== np.nan` never works, by design). Implement a boolean mask using the correct tool, then column-wise counts and fractions built directly from that mask.

Implement `missing_mask(x)`, `missing_count_per_column(x)` and `missing_fraction_per_column(x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 2D float array, `(num_rows, num_columns)`, missing values represented as `np.nan`.
- Use `np.isnan`, never `== np.nan` (Theory explains exactly why the latter silently fails).
- `missing_fraction_per_column` returns fractions in `[0.0, 1.0]`, one per column.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.isnan(x)` already returns a same-shaped boolean mask directly, no comparison operator needed.

</details>

<details>
<summary>Hint 2</summary>

Once you have the mask, `missing_count_per_column` is `.sum(axis=0)` (summing down each column, over all rows).

</details>

## Theory

### The simple version

Imagine a paper survey with some blank boxes, a respondent skipped a question, or the handwriting was illegible and got discarded. Before you can analyze the survey at all, you need to know exactly which boxes are blank, you can't compute "average age of respondents" correctly if some age entries are silently blank and you don't know it.

### The formula

Missing numeric values are conventionally represented as `np.nan` ("Not a Number"), a special floating-point value with one deeply counterintuitive property: it never equals anything, not even itself.

```text
np.nan == np.nan  ->  False  (!)
x == np.nan        ->  always False, for any x, silently
```

This is why `np.isnan(x)` exists as a dedicated function rather than relying on `==`: it's the only reliable way to ask "is this value NaN," checking the value's actual bit pattern rather than comparing it.

Once you have a boolean mask of where the missing values are, counting and fractioning are straightforward reductions:

```text
missing_count_per_column    = mask.sum(axis=0)             -- how many per column
missing_fraction_per_column = missing_count / num_rows      -- as a fraction of all rows
```

### How PyTorch actually implements this

`pandas.DataFrame.isna()` (the real-world tool most practitioners actually reach for before ever touching NumPy directly) is built on exactly this `np.isnan`-style check, extended to handle non-numeric missing markers too (`None`, `pd.NaT` for missing dates). PyTorch itself has no first-class "missing value" concept, tensors are expected to be fully populated by the time they reach a model, which is precisely why this detection-and-handling step (this question, plus `02-imputing-missing-values`) has to happen during data preparation, upstream of ever constructing a tensor, `torch.isnan(tensor)` exists mainly for debugging (catching NaN values that leaked in from a numerical instability during training, like a loss that diverged), not for handling genuinely missing input data.

## Explanation

`missing_mask` calls `np.isnan(x)` directly, the correct detection tool from Theory.

`missing_count_per_column` sums that mask along `axis=0` (down each column, across every row), giving one count per column.

`missing_fraction_per_column` divides that count by `x.shape[0]` (the total row count), turning raw counts into fractions.
