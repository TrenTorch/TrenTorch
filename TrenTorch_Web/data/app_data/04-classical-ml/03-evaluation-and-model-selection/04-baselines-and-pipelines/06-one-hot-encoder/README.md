---
name: evaluation-one-hot-encoder
title: One-hot encoder with fitted categories
tags: [classical-ml, preprocessing, categorical-features]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A model cannot multiply a weight by the word "red", so categorical features must become numbers. One-hot encoding gives each category its own column: a row holds a `1` in its category's column and `0` everywhere else. The category list must be learned from training data, and an unseen category at prediction time should be reported, not silently encoded as all zeros.

Implement two functions.

- `one_hot_fit(values)`: returns the sorted list of distinct values, which fixes the column order.
- `one_hot_transform(values, categories)`: returns a float matrix of shape `(len(values), len(categories))`. Column `j` corresponds to `categories[j]`. A value not in `categories` raises `ValueError`.

### Constraints

- Empty input returns an array of shape `(0, len(categories))`.
- Each row of a valid output sums to exactly `1`.
- The categories passed to `one_hot_transform` define the column order, even if they are not sorted.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Build a dictionary from category to column index once, then look each value up.

</details>

<details>
<summary>Hint 2</summary>

Set one cell per row with `out[row, index] = 1.0`.

</details>

## Theory

### The simple version

Make one yes-or-no column per category. Exactly one of those columns is on for each row. The encoding loses no information, but it grows wider with every new category, and a category never seen during training has no column to turn on.

### The formula

For a value $v$ and fitted categories $c_1, \dots, c_k$, the encoded row is

$$
e_j = \begin{cases} 1 & \text{if } v = c_j \\ 0 & \text{otherwise} \end{cases}
$$

## Explanation

`one_hot_fit` sorts the distinct values so the column order is fixed and reproducible. `one_hot_transform` maps each category to its index, sets one cell per row, and raises a clear error for anything outside the fitted list.
