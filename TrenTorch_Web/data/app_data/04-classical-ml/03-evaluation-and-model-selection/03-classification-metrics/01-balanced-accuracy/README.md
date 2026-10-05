---
name: evaluation-classification-balanced-accuracy
title: 'Balanced accuracy'
tags: [classical-ml, evaluation, classification, imbalance]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Accuracy rewards a model for guessing the majority class. If 95 percent of rows are negative, a model that always says negative scores 95 percent and catches nothing. Balanced accuracy averages the recall of each class, so every class counts equally no matter how many rows it has.

Implement `balanced_accuracy(y_true, y_pred)`. For each class present in `y_true`, compute the fraction of its rows that were predicted correctly, then return the mean of those fractions.

### Constraints

- `y_true` and `y_pred` have the same length, otherwise raise `ValueError`.
- Empty input raises `ValueError`.
- Classes that appear only in `y_pred` are ignored.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Loop over `np.unique(y_true)`. For each class, select the rows where `y_true == c` first.

</details>

<details>
<summary>Hint 2</summary>

Recall for class `c` is `np.mean(y_pred[mask] == c)`, where `mask` selects those rows.

</details>

## Theory

### The simple version

Score each class by how often you find its members, then average those scores. A rare class gets the same weight as a common one, so ignoring it costs as much as ignoring the common one.

### The formula

$$
\text{BA} = \frac{1}{K} \sum_{c=1}^{K} \frac{\text{TP}_c}{\text{TP}_c + \text{FN}_c}
$$

## Explanation

`balanced_accuracy` validates the inputs, loops over the classes present in the truth labels, computes per-class recall with a boolean mask, and returns their mean. Using the mask on the true labels, not the predictions, is what makes each class's rows define its own score.
