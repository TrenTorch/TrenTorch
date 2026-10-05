---
name: evaluation-mcnemar-test
title: McNemar's test for comparing two classifiers
tags: [classical-ml, evaluation, hypothesis-testing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Two classifiers evaluated on the same test set will each get some samples right and wrong. Samples both get right, or both get wrong, say nothing about which is better; only the samples where they _disagree_ matter. McNemar's test asks whether the disagreements lean one way more than chance would explain.

### From theory to code

Implement `mcnemar_statistic(y_true, pred_a, pred_b)` and return the continuity-corrected chi-square statistic computed from the two disagreement counts.

### Constraints

- All three inputs are one-dimensional arrays of equal length.
- Let `b` be the number of samples only A got right and `c` the number only B got right.
- Return `max(|b - c| - 1, 0)**2 / (b + c)` as a Python `float`, or `0.0` when `b + c == 0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

Build two boolean arrays, `a_correct` and `b_correct`, by comparing each prediction to `y_true`.

</details>

<details><summary>Hint 2</summary>

`b` counts `a_correct & ~b_correct`; `c` counts `~a_correct & b_correct`.

</details>

## Theory

### The simple version

If A and B were equally good, the disagreements would split about evenly. The statistic grows as the split becomes lopsided. With one degree of freedom, a value above about 3.84 is significant at the 5% level.

### The formula

$$\chi^2 = \frac{\big(\max(|b - c| - 1,\, 0)\big)^2}{b + c}$$

Under the null hypothesis that both classifiers have the same error rate, this follows a chi-square distribution with 1 degree of freedom.

### How libraries implement this

`statsmodels.stats.contingency_tables.mcnemar` computes the same quantity (and an exact binomial variant for small counts).

## Explanation

Only the off-diagonal cells of the 2x2 agreement table matter, so two boolean masks and two sums are enough. The `max(..., 0)` stops the continuity correction from turning a perfectly even split into a positive statistic.
