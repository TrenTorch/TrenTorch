---
name: eval-corrected-resampled-t
title: 'Corrected resampled t-test for repeated splits'
tags: [classical-ml, evaluation, statistics, nadeau-bengio, resampling]
difficulty: Advanced
---

## Statement

### Correct the variance for overlapping training sets

Repeated random splits (or repeated cross-validation) reuse training data, so the per-split differences are correlated. Nadeau and Bengio (2003) fix the variance by inflating it with the ratio of test to training size. For `k` repeats with differences `d_i`, the corrected statistic is

`t = mean(d) / sqrt((1/k + n_test / n_train) * var(d))`, with `var` using `k - 1`.

Implement `corrected_resampled_t(diffs, n_train, n_test)` and return `t` as a float.

### Constraints

- `diffs` is a 1-D array with `k >= 2` entries.
- `n_train > 0` and `n_test > 0`. Otherwise raise `ValueError`.
- Zero variance in `diffs` raises `ValueError`, since the statistic is undefined.
- Do not modify the input.

### Hints

<details>
<summary>Hint 1</summary>

Compute the correction factor `1/k + n_test/n_train` once. With `k = 3`, `n_train = 9`, and `n_test = 1`, it equals `4/9`.

</details>

## Theory

A naive paired test treats `k` repeated splits as independent. They are not: two splits share most of their training points, so their scores move together. The Nadeau-Bengio term `n_test / n_train` accounts for that overlap. It makes the test more conservative, which is the right direction, since the naive test over-rejects. A 10-fold cross-validation with correction is the common default in published comparisons, and the inflation factor for that setup is `1/10 + 1/9`.

### Where this shows up in production

Model comparison reports for teams that rely on repeated resampling use this test to decide whether a change is real. Using the uncorrected test for such reports is a frequent source of false wins, especially for small datasets where the test set is a large fraction of the data.

### Using it to make decisions

Use this test whenever your folds or repeats share training data, which is almost always. Report the corrected p-value alongside the effect size. If the corrected test says no difference while the naive test says yes, trust the corrected one and collect more data or a stronger baseline before claiming a win.

### Pros and cons

**Pros:** accounts for overlapping training sets with one line of arithmetic, works for any repeated-split protocol, and is far less likely to produce false positives than the naive test.

**Cons:** the correction is an approximation, it is conservative and so has lower power, and its exact behaviour depends on the split scheme, so it should not be applied blindly to every resampling design.

## Explanation

The solution computes the sample variance of the differences and inflates it by the correction factor before the t-style division. Keeping the correction in the denominator means the statistic shrinks toward zero as the test fraction grows, which matches the reason the correction exists.
