---
name: evaluation-classification-log-loss
title: 'Log loss (cross-entropy)'
tags: [classical-ml, evaluation, classification, probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A classifier that outputs probabilities should be scored on those probabilities, not only on the hard label. Log loss punishes confident wrong answers heavily: predicting 0.99 for a true negative costs far more than predicting 0.6. It is the average negative log-likelihood of the true labels under the predicted probabilities.

Implement `log_loss(y_true, y_prob, eps=1e-15)` for binary labels, where `y_prob` is the predicted probability of class 1.

- Clip probabilities to `[eps, 1 - eps]` so `log(0)` never occurs.
- Return −mean(y log p + (1 − y) log(1 − p)).

### Constraints

- `y_true` values must be 0 or 1, and `y_prob` values must lie in `[0, 1]`. Otherwise raise `ValueError`.
- Inputs must have the same length and be non-empty.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.clip` the probabilities before taking logs.

</details>

<details>
<summary>Hint 2</summary>

Write the per-row loss as `-(y * log(p) + (1 - y) * log(1 - p))`, then take the mean.

</details>

## Theory

### The simple version

Log loss rewards calibrated confidence. Saying "50 percent" on everything scores ln 2, about 0.693. Certainty that turns out wrong costs without bound, which is why the probabilities are clipped.

### The formula

$$
\mathcal{L} = -\frac{1}{n}\sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i)\log(1 - p_i) \right]
$$

## Explanation

`log_loss` validates the labels and probabilities, clips the probabilities to a safe interval, and returns the mean of the per-row negative log-likelihood. The clip is what keeps a fully confident wrong prediction finite: it costs about 34.5 with the default epsilon, not infinity.
