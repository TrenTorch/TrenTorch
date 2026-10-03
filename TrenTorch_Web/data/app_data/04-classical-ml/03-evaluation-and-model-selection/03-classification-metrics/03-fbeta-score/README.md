---
name: evaluation-classification-fbeta-score
title: 'F-beta score'
tags: [classical-ml, evaluation, classification, precision, recall]
difficulty: Beginner
---

## Statement

### The problem, from first principles

F1 weighs precision and recall equally. Sometimes that is wrong: a cancer screen must not miss cases (recall matters more), while a fraud alert that blocks good customers must not be noisy (precision matters more). F-beta lets you choose. `beta > 1` leans toward recall and `beta < 1` leans toward precision. `beta = 1` gives F1.

Implement `fbeta_score(y_true, y_pred, beta=1.0, positive=1)` for binary labels.

- Precision P = TP / (TP + FP), or `0.0` when TP + FP is zero.
- Recall R = TP / (TP + FN), or `0.0` when TP + FN is zero.
- Return (1 + beta²) · P · R / (beta² · P + R), or `0.0` when the denominator is zero.

### Constraints

- `beta` must be greater than zero, otherwise raise `ValueError`.
- Inputs must have the same length.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute TP, FP, and FN from boolean masks on `positive`.

</details>

<details>
<summary>Hint 2</summary>

Compute `b2 = beta ** 2` once, then use the formula with `b2` in place of `beta ** 2`.

</details>

## Theory

### The simple version

F-beta is a weighted harmonic mean. Beta says how many times more important recall is than precision. Beta equal to one balances them, two counts recall four times as heavily in the denominator's weighting, and one half leans toward precision.

### The formula

$$
F_\beta = \frac{(1 + \beta^2)\, P\, R}{\beta^2 P + R}
$$

## Explanation

`fbeta_score` counts true positives, false positives, and false negatives with masks, derives precision and recall with zero-denominator guards, and applies the weighted harmonic mean. Guarding each ratio separately keeps the function defined on degenerate inputs such as a model that never predicts positive.
