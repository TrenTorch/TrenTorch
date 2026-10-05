---
name: eval-auc-rank-statistic
title: 'AUC as the Mann-Whitney rank statistic'
tags: [classical-ml, evaluation, auc, roc, mann-whitney, ranking]
difficulty: Intermediate
---

## Statement

### Compute ROC AUC from ranks, with ties averaged

The area under the ROC curve equals the probability that a randomly chosen positive example scores higher than a randomly chosen negative one, with ties counting one half. That is the Mann-Whitney U statistic divided by the number of pairs. If `R_pos` is the sum of the positives' ranks (ascending, ties averaged), then

`AUC = (R_pos - n_pos (n_pos + 1) / 2) / (n_pos * n_neg)`.

Implement `auc_rank(scores, labels)` with `labels` in `{0, 1}`. Return the AUC as a float.

### Constraints

- `scores` and `labels` are 1-D arrays of equal length.
- `labels` holds only `0` and `1`. Otherwise raise `ValueError`.
- Both classes must be present. Otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Rank the scores ascending. Average the ranks of tied scores, then sum the ranks of the positive examples.

</details>

## Theory

The rank form makes AUC a statement about pairs, so it does not depend on any threshold and does not depend on score calibration: any monotone transformation of the scores leaves AUC unchanged. That is a strength for comparing models, but it hides calibration, so a model can have a high AUC and still output probabilities that are badly wrong. AUC also weights all thresholds equally, which is often not what the business cares about.

### Where this shows up in production

AUC is a standard gate for ranking models in fraud, churn, and lead-scoring pipelines. Because it is threshold-free, teams often use it to choose a model and then pick the operating threshold separately, using a cost curve or a precision target.

### Using it to make decisions

Use AUC to compare models whose score ordering is what matters, such as ranking candidates for review. Do not use it alone when the operating point is fixed or when prevalence is very low, since AUC can look high while precision at the usable threshold is poor. Pair it with precision-recall at the expected base rate, and check calibration separately if the score is shown to users or used as a probability.

### Pros and cons

**Pros:** threshold-free, invariant to monotone score transforms, and computed exactly from ranks in `O(n log n)`.

**Cons:** says nothing about calibration, weights every threshold equally, is insensitive to class imbalance in the way that matters operationally, and can look strong for a model that ranks well but is useless at the threshold you deploy.

## Explanation

The solution averages tied ranks, sums the positive ranks, and subtracts the minimum possible positive rank sum before dividing by the number of positive-negative pairs. This is the same arithmetic as the Mann-Whitney U test, so the value matches the probability interpretation exactly.
