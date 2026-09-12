---
name: math-outlier-detection
title: Detecting outliers with IQR and z-score
tags: [data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`02-imputing-missing-values` assumed missing values are cleanly flagged as `NaN`, easy. Bad data is rarely that considerate: a sensor briefly malfunctions and reports a temperature of 9999, a data-entry error turns "$50,000" into "$50,000,000", nothing marks these as wrong, they're just numbers sitting in the dataset, quietly distorting every mean, variance, and gradient that touches them. Before you can trust a model built on real data, you need a systematic way to flag "this number looks implausible," not just eyeball a scatter plot and hope.

Two standard, complementary tools do this: the IQR method (based on percentiles, robust to extreme values) and the z-score method (based on standard deviations, but with a real weakness this question makes visible). Understanding both, and where each one fails, is a genuinely practical skill for any real dataset.

### From theory to code

Theory gives both detection rules directly: IQR flags anything outside a fixed multiple of the interquartile range beyond Q1/Q3, z-score flags anything more than a fixed number of standard deviations from the mean.

Implement `detect_outliers_iqr(x, k=1.5)` and `detect_outliers_zscore(x, threshold=3.0)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Both functions return a boolean mask, same shape as `x`, `True` where a value is flagged.
- `detect_outliers_iqr` uses `np.percentile` for Q1 (25th) and Q3 (75th).
- `detect_outliers_zscore` uses the population std (`np.std`'s default `ddof=0`).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.percentile(x, 25)` and `np.percentile(x, 75)` give Q1 and Q3 directly, `IQR = Q3 - Q1`.

</details>

<details>
<summary>Hint 2</summary>

Both functions boil down to one comparison against two computed bounds (IQR) or one computed statistic (z-score), `|value| > threshold`-style logic.

</details>

## Theory

### The simple version

Line up a class's exam scores from lowest to highest. Most scores cluster somewhere in the "reasonable middle", the IQR method marks anything far below or above that middle range as suspicious, using percentiles, which don't care how extreme the most extreme values are, only their rank. The z-score method instead asks "how many standard deviations from the average is this," which sounds similar, but has a real weakness: a single wild outlier inflates the average AND the standard deviation it's being measured against, sometimes hiding itself in the very statistic meant to catch it.

### The formula

**IQR (Interquartile Range) method**: flag anything outside a fixed multiple of the spread between the 25th and 75th percentiles.

```text
Q1, Q3 = 25th percentile, 75th percentile
IQR = Q3 - Q1
outlier if x < Q1 - k*IQR  or  x > Q3 + k*IQR      (k = 1.5, by convention)
```

**Z-score method**: flag anything more than `threshold` standard deviations from the mean.

```text
z = (x - mean(x)) / std(x)
outlier if |z| > threshold      (threshold = 3.0, by convention)
```

The two methods have a real, practical difference worth internalizing: IQR is based on percentiles (ranks), which barely move even if the most extreme value gets even more extreme, robust by construction. Z-score is based on mean and std, both of which are themselves dragged by outliers (`02-expectation-variance`'s own vocabulary), so a single sufficiently extreme outlier can inflate the standard deviation enough to make its OWN z-score fall back under the threshold, a real failure mode called "masking." This is exactly why `02-imputing-missing-values`'s Theory section already flagged median as the outlier-robust alternative to mean, the same robustness distinction shows up here between IQR (percentile-based, robust) and z-score (mean/std-based, not).

### How PyTorch actually implements this

Outlier detection itself lives entirely in the data-preparation stage, before any tensor is built, `pandas`/`scipy` (via `scipy.stats.zscore` and quantile-based methods on a `DataFrame`) are the real tools practitioners reach for, not PyTorch. But the CONSEQUENCE of skipped outlier detection shows up directly inside training: an unflagged extreme value inflates `03-mse-gradient`'s gradient magnitude for the batch it's in (squared error grows quadratically with how wrong a single prediction is), which is exactly the failure mode `06-gradient-clipping` (Optimizers track) exists to contain after the fact, capping gradient norms rather than preventing the bad value from ever entering training in the first place. Catching outliers here, during data preparation, is the cheaper, earlier fix.

## Explanation

`detect_outliers_iqr` computes Q1 and Q3 via `np.percentile`, derives `IQR = Q3 - Q1`, and flags any value below `Q1 - k*IQR` or above `Q3 + k*IQR`, exactly the rule from Theory.

`detect_outliers_zscore` computes each value's z-score, `(x - mean(x)) / std(x)`, and flags any value whose absolute z-score exceeds `threshold`.
