---
name: evaluation-classification-matthews-correlation
title: 'Matthews correlation coefficient'
tags: [classical-ml, evaluation, classification, imbalance]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

F1 ignores true negatives entirely, so it can look good on a model that is mostly wrong about the negatives. The Matthews correlation coefficient (MCC) uses all four cells of the confusion matrix. It is the correlation between predictions and truth: +1 means perfect agreement, 0 means no better than chance, and -1 means every prediction is inverted.

Implement `matthews_corrcoef(y_true, y_pred, positive=1)` for binary labels.

MCC = (TP · TN − FP · FN) / sqrt((TP + FP)(TP + FN)(TN + FP)(TN + FN))

If any factor in the denominator is zero, return `0.0`.

### Constraints

- Inputs must have the same length, otherwise raise `ValueError`.
- Any label other than `positive` counts as negative.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Build the four counts from boolean masks on `positive`, using the same pattern as F-beta.

</details>

<details>
<summary>Hint 2</summary>

Compute the product of the four marginal sums under a single square root, and check for zero before dividing.

</details>

## Theory

### The simple version

MCC is the phi coefficient from a 2x2 table. It only reaches 1 when both rows and both columns of the table are perfectly diagonal, so a model cannot score well by exploiting imbalance.

### The formula

$$
\text{MCC} = \frac{\text{TP}\cdot\text{TN} - \text{FP}\cdot\text{FN}}{\sqrt{(\text{TP}+\text{FP})(\text{TP}+\text{FN})(\text{TN}+\text{FP})(\text{TN}+\text{FN})}}
$$

## Explanation

`matthews_corrcoef` counts the four confusion cells with masks, forms the numerator from the two diagonal products, and builds the denominator from the four marginal totals. Returning `0.0` on a zero marginal matches the convention that a constant predictor carries no correlation.
