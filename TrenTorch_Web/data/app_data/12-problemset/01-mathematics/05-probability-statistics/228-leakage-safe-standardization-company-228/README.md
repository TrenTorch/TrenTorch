---
name: leakage-safe-standardization-company-228
title: 'leakage-safe-standardization — Myntra case'
tags: [problemset, data-stats-for-ds, data-cleaning, myntra]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Myntra'
hint: 'mean/std from train only; (x - mean) / std for both (std 0 -> 1)'
tools: [NumPy]
---

## Statement

Myntra-inspired recommendation experiment is preparing a feature for train and validation data while avoiding information leakage. You need to fit the standardization statistics on the training portion only and apply those same statistics to the validation portion.

Standardise the training matrix and the validation matrix using **only the training statistics**: the column means and population standard deviations of `train` (a zero standard deviation is replaced by 1). Apply the same means and scales to both matrices.

Implement `solve(train, val)`.

**Returns.** Return a tuple `(train_scaled, val_scaled)` of float NumPy matrices.

Standardise the training matrix and the validation matrix using **only the training statistics**: the column means and population standard deviations of `train` (a zero standard deviation is replaced by 1). Apply the same means and scales to both matrices.

Implement `solve(train, val)`.

**Returns.** Return a tuple `(train_scaled, val_scaled)` of float NumPy matrices.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4]], [[100, 6]])
```

Output:

```text
([[-1.0, -1.0], [1.0, 1.0]], [[98.0, 3.0]])
```

**Example 2**

Input:

```python
solve([[5.0, 1.0], [5.0, 3.0]], [[7.0, 2.0]])
```

Output:

```text
([[0.0, -1.0], [0.0, 1.0]], [[2.0, 0.0]])
```

## Theory

### The simple version

If you standardise using the mean and spread of the _whole_ dataset, the validation rows influence the transform that is applied to the training rows, so information leaks from validation into training and the validation score becomes optimistic. The leak-free way is to learn the transform from the training data only and then just apply it to everything else.

### The recipe

$$\mu,\sigma\ \text{from train only};\qquad \tilde x=\frac{x-\mu}{\sigma}\ \text{for both train and validation}$$

### Why it matters

- If the validation rows influence the mean and spread used for scaling, information leaks and the validation score becomes optimistic.
- Fitting the scaler on training data only mimics what happens in production.

### How it works

1. Compute the column means and standard deviations of the training matrix only (a zero standard deviation becomes $1$).
2. Apply those same numbers to the training and the validation matrix.

### Worked example

The training columns have means $(2,3)$ and standard deviations $(1,1)$. The training rows become $(-1,-1)$ and $(1,1)$. The validation row $(100,6)$ becomes $(98,3)$ with the same numbers, so it stays visibly far outside the training range: ([[-1.0, -1.0], [1.0, 1.0]], [[98.0, 3.0]]).

## Explanation

In the first example the training columns have means $(2,3)$ and standard deviations $(1,1)$, so the validation row $(100,6)$ becomes $(98,3)$; it is far outside the training range and is _not_ squashed back to look normal. A constant training column (second example, first column) has $\sigma=0$, replaced by $1$, so it is simply centred.
