---
name: evaluation-classification-brier-score
title: 'Brier score'
tags: [classical-ml, evaluation, classification, calibration]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Log loss is sharp about confident mistakes, and sometimes that sharpness is more than you want. The Brier score is the mean squared error between the predicted probability and the 0/1 outcome. It is bounded between 0 and 1, so a single extreme miss cannot dominate it the way it can in log loss.

Implement `brier_score(y_true, y_prob)` for binary labels, where `y_prob` is the predicted probability of class 1.

Return mean((p − y)²).

### Constraints

- `y_true` values must be 0 or 1, and `y_prob` values must lie in `[0, 1]`. Otherwise raise `ValueError`.
- Inputs must have the same length and be non-empty.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Subtract the labels from the probabilities element by element, then square.

</details>

<details>
<summary>Hint 2</summary>

`np.mean` of the squared differences is the whole answer.

</details>

## Theory

### The simple version

Brier score is just squared error on probabilities. Predicting 0.5 always gives 0.25. Perfect certainty that is always right gives 0. Confident and wrong gives 1.

### The formula

$$
\text{BS} = \frac{1}{n} \sum_{i=1}^{n} (p_i - y_i)^2
$$

## Explanation

`brier_score` checks the labels and probabilities, then returns the mean squared difference. Because the squared difference of a probability and a 0/1 label never exceeds 1, the score stays in `[0, 1]`.
