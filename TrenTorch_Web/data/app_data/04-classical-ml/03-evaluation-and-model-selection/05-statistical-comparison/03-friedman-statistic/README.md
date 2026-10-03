---
name: eval-friedman-statistic
title: 'Friedman test for comparing several classifiers'
tags: [classical-ml, evaluation, statistics, friedman-test, ranks]
difficulty: Advanced
---

## Statement

### Compare k models across N datasets by rank

When you compare more than two models over several datasets, pairwise t-tests inflate the error rate. The Friedman test (Demsar, 2006) ranks the models within each dataset, then tests whether the average ranks differ.

Given a `(N, k)` score matrix where higher is better, rank each row from 1 (best) to `k` (worst), with tied scores receiving the average of their ranks. Let `R_j` be the sum of algorithm `j`'s ranks over the `N` datasets. Then

`chi2_F = 12 / (N k (k + 1)) * sum_j R_j^2 - 3 N (k + 1)`.

Implement `friedman_statistic(scores)` and return `chi2_F` as a float.

### Constraints

- `scores` is 2-D with `N >= 1` rows and `k >= 2` columns. Otherwise raise `ValueError`.
- Any non-finite score raises `ValueError`.
- Do not modify the input.

### Hints

<details>
<summary>Hint 1</summary>

Use `scipy.stats.rankdata` only if you are sure it is available. Otherwise, a rank per row with ties averaged is enough: for each row, sort and average the positions of equal values.

</details>

## Theory

The Friedman statistic is approximately chi-square with `k - 1` degrees of freedom under the null that all algorithms have the same average rank. Ranking removes the scale of each dataset, so a dataset where accuracies span 0.5 to 0.99 does not dominate one where they span 0.80 to 0.82. Ties are common in practice, so average ranks matter; giving ties arbitrary ranks biases the statistic. The test only says that some difference exists, and the post-hoc Nemenyi test in the next question says which pairs differ.

### Where this shows up in production

Benchmark suites that choose a default algorithm across many datasets use this test to decide whether the ranking is meaningful. Model-selection frameworks that compare a family of candidates on a set of tasks use it to avoid cherry-picking one winning dataset.

### Using it to make decisions

Use the Friedman test when you have at least about five datasets and three or more models. Report the mean rank for each model along with the statistic, since the rank table is the thing a reader can act on. If the test rejects, follow up with a post-hoc test; if it does not, the honest conclusion is that the models are indistinguishable on this benchmark.

### Pros and cons

**Pros:** robust to different score scales, makes no normality assumption, and handles any number of models in one test.

**Cons:** it only uses ranks, so it ignores the size of the gaps, it needs several datasets to have power, and the chi-square approximation is weak for small `N` and `k`.

## Explanation

The solution ranks each row with ties averaged, sums ranks per column, and applies the rank-sum form of the statistic. Using rank sums rather than means keeps the arithmetic close to the formula in the statement, which makes the hand check easier.
