---
name: evaluation-classification-hamming-loss
title: 'Hamming loss for multilabel'
tags: [classical-ml, evaluation, classification, multilabel]
difficulty: Beginner
---

## Statement

### The problem, from first principles

In multilabel classification one example can carry several tags at once: a photo may be both "beach" and "sunset". Exact-match accuracy counts a row as right only if every tag is right, which is harsh. Hamming loss counts the fraction of individual label slots that are wrong, so partial credit is given for getting most tags right.

Implement `hamming_loss(y_true, y_pred)`. Both inputs are either 1-D label vectors (single-label) or 2-D binary matrices of shape `(n_samples, n_labels)`. Return the fraction of entries where they differ.

### Constraints

- The two inputs must have the same shape, otherwise raise `ValueError`.
- Empty input raises `ValueError`.
- The result lies in `[0, 1]`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`y_true != y_pred` gives a boolean array of the same shape, whether it is 1-D or 2-D.

</details>

<details>
<summary>Hint 2</summary>

`np.mean` over that boolean array counts the wrong slots out of the total, which is the answer.

</details>

## Theory

### The simple version

Count the boxes you ticked wrong, out of all the boxes. Getting two of three tags right on every row scores 1/3 loss, even though no row is fully correct.

### The formula

$$
\text{HL} = \frac{1}{n\,L} \sum_{i=1}^{n} \sum_{j=1}^{L} \mathbf{1}[\hat{y}_{ij} \neq y_{ij}]
$$

## Explanation

`hamming_loss` checks that the shapes match, compares every entry at once with `!=`, and returns the mean. Working on the full array rather than looping over rows keeps the same code path for single-label vectors and multilabel matrices.
