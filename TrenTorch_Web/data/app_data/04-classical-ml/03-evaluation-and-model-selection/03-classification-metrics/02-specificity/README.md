---
name: evaluation-classification-specificity
title: 'Specificity: true negative rate'
tags: [classical-ml, evaluation, classification]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Recall answers "of the real positives, how many did we find?". Specificity answers the mirror question for the negative class: "of the real negatives, how many did we correctly leave alone?". A spam filter with high recall and low specificity catches spam but buries legitimate mail.

Implement `specificity(y_true, y_pred, positive=1)`. Treat `positive` as the positive class and everything else as negative. Return TN / (TN + FP).

### Constraints

- If there are no negative rows, return `0.0`.
- Inputs must have the same length, otherwise raise `ValueError`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Negative rows are `y_true != positive`. Among them, a prediction counts as a true negative when it is also not `positive`.

</details>

<details>
<summary>Hint 2</summary>

`np.mean(y_pred[neg] != positive)` over the negative rows gives the same ratio directly.

</details>

## Theory

### The simple version

Of everything that really is negative, what fraction did you correctly call negative? A model can be very specific by refusing to say positive at all, which is why specificity is always read next to recall.

### The formula

$$
\text{Specificity} = \frac{\text{TN}}{\text{TN} + \text{FP}}
$$

## Explanation

`specificity` builds a mask of the true negatives' rows, then takes the fraction of those rows where the prediction is also not the positive label. The zero-denominator guard returns `0.0` so a single-class dataset with no negatives does not divide by zero.
