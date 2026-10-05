---
name: evaluation-classification-cohens-kappa
title: "Cohen's kappa"
tags: [classical-ml, evaluation, classification, agreement]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Raw agreement can mislead. Two annotators who label 90 percent of items "not spam" will agree about 80 percent of the time just by chance. Cohen's kappa measures agreement beyond chance: it compares observed agreement with the agreement you would expect if both sides labeled independently with their own class frequencies.

Implement `cohens_kappa(y_true, y_pred)` for any number of classes.

- Observed agreement p_o is the fraction of rows where the two labelings match.
- Expected agreement p_e sums, over each class, the product of the two labelings' marginal fractions.
- Return (p_o − p_e) / (1 − p_e). If p_e equals 1, both labelings are the same constant, so return `1.0`.

### Constraints

- Inputs must have the same length and be non-empty, otherwise raise `ValueError`.
- The result is symmetric in its two arguments.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Use `np.unique` on the concatenation of both arrays so both marginals share one label set.

</details>

<details>
<summary>Hint 2</summary>

For each label `c`, the marginal fraction in `y_true` is `np.mean(y_true == c)`. Multiply it by the same fraction from `y_pred` and sum over labels.

</details>

## Theory

### The simple version

Kappa asks how much better than luck the two labelers agree. A value near 0 means they agree no more than chance, and 1 means perfect agreement beyond chance.

### The formula

$$
\kappa = \frac{p_o - p_e}{1 - p_e}, \qquad p_e = \sum_c \hat{P}_{\text{true}}(c)\, \hat{P}_{\text{pred}}(c)
$$

## Explanation

`cohens_kappa` builds the shared label set, computes observed agreement directly, and sums the product of marginal fractions for expected agreement. The `p_e == 1` branch handles the degenerate case where both sides always use the same single label, where the usual formula divides by zero.
