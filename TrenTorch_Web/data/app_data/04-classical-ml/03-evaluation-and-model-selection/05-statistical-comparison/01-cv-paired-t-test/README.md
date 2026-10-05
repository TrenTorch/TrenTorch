---
name: eval-paired-t-statistic
title: 'Paired t-test on cross-validation folds'
tags: [classical-ml, evaluation, statistics, paired-t-test, cross-validation]
difficulty: Intermediate
---

## Statement

### Test whether two models differ on the same folds

Given per-fold scores of two models evaluated on the same folds, the paired t-test looks at the per-fold differences `d_i = a_i - b_i`. The statistic is

`t = mean(d) / (sd(d) / sqrt(n))`, with `sd` using `n - 1` in the denominator.

Implement `paired_t_statistic(a, b)` and return `t` as a float.

### Constraints

- `a` and `b` are 1-D arrays of the same length `n >= 2`. Otherwise raise `ValueError`.
- If the differences have zero spread, the statistic is undefined, so raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Compute `d = a - b` first, then use `np.std(d, ddof=1)`.

</details>

## Theory

Pairing removes fold-to-fold variation that both models share, such as an unusually hard split, so the test looks only at how much the models differ. The statistic follows a t distribution with `n - 1` degrees of freedom under the null of equal means. Its main weakness is that cross-validation folds share training data, so the differences are not independent, which inflates the chance of a false positive. The corrected resampled test in the next question addresses that.

### Where this shows up in production

Paired t-tests are a common gate in model promotion: a candidate model must beat the incumbent on the same folds before it replaces it. They also appear in offline evaluation dashboards that report whether a change in a ranking metric is larger than fold noise.

### Using it to make decisions

Use the paired test to decide whether a difference is worth a deployment, and prefer effect size with a confidence interval over a bare p-value. Use identical folds for both models, otherwise the pairing is meaningless. Be wary of small `n`: five folds give little power, so a null result does not prove the models are equal. For cross-validation specifically, read the corrected test as the more honest default.

### Pros and cons

**Pros:** simple, widely understood, works on any paired score (accuracy, AUC, error), and removes shared fold effects.

**Cons:** folds overlap in training data, so the independence assumption is violated, the test has low power with few folds, and it says nothing about practical significance on its own.

## Explanation

The solution forms the differences once, takes their mean, and divides by the standard error computed with the sample standard deviation. Raising on zero spread avoids a division by zero that would otherwise look like an infinitely significant result.
