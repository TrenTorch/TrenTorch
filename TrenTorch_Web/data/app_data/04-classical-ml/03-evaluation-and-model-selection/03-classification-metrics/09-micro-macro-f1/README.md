---
name: evaluation-classification-micro-macro-f1
title: 'Micro and macro F1'
tags: [classical-ml, evaluation, classification, multiclass]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

With more than two classes, "the F1 score" is ambiguous. You can pool every decision together and compute one F1 (micro), which weights each row equally and so favors large classes. Or you can compute F1 for each class and average those (macro), which weights each class equally and so exposes a model that ignores a rare class.

Implement two functions for single-label multiclass predictions.

- `f1_micro(y_true, y_pred)`: pool TP, FP, and FN across all classes, then return 2·TP / (2·TP + FP + FN).
- `f1_macro(y_true, y_pred)`: for each label in the union of `y_true` and `y_pred`, compute its own F1 as 2·TP / (2·TP + FP + FN), using 0.0 when the denominator is zero, then return the mean.

### Constraints

- Inputs must have the same length and be non-empty, otherwise raise `ValueError`.
- Each class's counts come from one-vs-rest: a row is a false positive for class c when it is predicted c and its true label is not c.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

For single-label data, micro F1 reduces to a count of correct predictions over total rows. Check your micro result against that.

</details>

<details>
<summary>Hint 2</summary>

Loop over `np.union1d(y_true, y_pred)` for the macro version. Count TP, FP, and FN for each label with masks.

</details>

## Theory

### The simple version

Micro F1 asks "over all decisions, how good were we?" Macro F1 asks "averaged over classes, how good were we?" The two agree only when every class is equally common and equally well predicted.

### The formula

$$
F_1^{\text{micro}} = \frac{2\,\text{TP}}{2\,\text{TP} + \text{FP} + \text{FN}}, \qquad F_1^{\text{macro}} = \frac{1}{K}\sum_{c} F_{1,c}
$$

## Explanation

`f1_micro` sums the one-vs-rest counts over every label before applying the F1 formula, so it equals accuracy for single-label data. `f1_macro` applies the same formula per label and averages the results, with zero-denominator labels contributing 0.0 so a class that is never predicted is penalized rather than ignored.
