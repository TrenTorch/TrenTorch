---
name: evaluation-cost-sensitive-error
title: Cost-sensitive error rate
tags: [classical-ml, evaluation, cost-sensitive]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Error rate treats every mistake as equal. In practice a missed disease costs far more than a false alarm. A cost matrix states what each kind of mistake costs, and the cost-sensitive error is the average cost per sample.

### From theory to code

Implement `cost_sensitive_error(y_true, y_pred, cost_matrix)`, returning the mean cost over all samples.

### Constraints

- `y_true` and `y_pred` are integer class arrays of equal length.
- `cost_matrix[i][j]` is the cost of predicting `j` when the truth is `i`; correct predictions normally cost 0.
- Return a Python `float`; return `0.0` for empty input.

### Hints

Open one at a time. Each gives away a little more than the last.

<details><summary>Hint 1</summary>

NumPy fancy indexing looks up one cost per sample: `cost_matrix[y_true, y_pred]`.

</details>

<details><summary>Hint 2</summary>

Average that vector.

</details>

## Theory

### The simple version

Instead of counting mistakes, add up what they cost. With a 0/1 cost matrix this is exactly the ordinary error rate.

### The formula

$$\text{cost} = \frac{1}{n}\sum_{k=1}^{n} C\big[y_k,\ \hat{y}_k\big]$$

### How libraries implement this

scikit-learn has no built-in cost-matrix metric for classification; it is usually written as a custom scorer for `make_scorer`.

## Explanation

Indexing the matrix with two integer arrays picks the right cell for every sample in one vectorised step, so no loop is needed.
