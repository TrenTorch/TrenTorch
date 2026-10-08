---
name: stratified-split-company-227
title: 'stratified-split — Booking.com case'
tags: [problemset, data-stats-for-ds, sampling-methods, booking-com]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Booking.com'
hint: 'per class: shuffle indices, first round(count*fraction) go to validation; sort the results'
tools: [NumPy]
---

## Statement

Booking.com-inspired experimentation pipeline needs training and validation sets whose class proportions remain stable when the dataset is split. You need to construct a deterministic stratified split so rare outcome classes are represented in both partitions.

Split the sample indices into training and validation sets so that each class is split in (nearly) the same proportion. For every class, the indices of that class are shuffled with `np.random.default_rng(seed)` (classes are visited in sorted order, one generator for all of them), and `round(count * val_fraction)` of them go to validation. Python's `round` rounds halves to the nearest even integer.

Implement `solve(y,val_fraction,seed=0)`.

**Returns.** Return a tuple `(train_idx, val_idx)` of sorted NumPy index arrays. A class so small that its rounded validation count is 0 contributes only to training.

Split the sample indices into training and validation sets so that each class is split in (nearly) the same proportion. For every class, the indices of that class are shuffled with `np.random.default_rng(seed)` (classes are visited in sorted order, one generator for all of them), and `round(count * val_fraction)` of them go to validation. Python's `round` rounds halves to the nearest even integer.

Implement `solve(y,val_fraction,seed=0)`.

**Returns.** Return a tuple `(train_idx, val_idx)` of sorted NumPy index arrays. A class so small that its rounded validation count is 0 contributes only to training.

### Examples

**Example 1**

Input:

```python
solve([0, 0, 0, 1, 1, 1], 1/3)
```

Output:

```text
([0, 1, 3, 4], [2, 5])
```

**Example 2**

Input:

```python
solve([0, 0, 0, 0, 1, 1], 0.5, seed=3)
```

Output:

```text
([0, 1, 4], [2, 3, 5])
```

## Theory

### The simple version

If a rare class is only 5% of the data, a purely random split can leave it almost out of the validation set. Stratifying means splitting each class separately, so validation reflects the class mix of the whole dataset and metrics for rare classes are stable.

### The recipe

For each class $c$: shuffle its $n_c$ indices; the first $\operatorname{round}(n_c\cdot f)$ go to validation, the rest to training. Merge the pieces and sort them.

### Why it matters

- A random split can leave a rare class almost absent from validation and make its metrics meaningless.
- Splitting each class separately keeps the class mix of the whole dataset in both parts.

### How it works

1. For each class, shuffle its indices with the seeded generator.
2. Send $\operatorname{round}(n_c\cdot f)$ of them to validation.
3. Merge the pieces and sort.

### Worked example

Each class has $3$ samples and $f=1/3$, so $\operatorname{round}(1)=1$ sample per class goes to validation: one from class $0$ and one from class $1$. The split is ([0, 1, 3, 4], [2, 5]).

## Explanation

With 3 samples per class and $f=1/3$, each class sends exactly one sample to validation (first example). The shuffle order depends on the seed, which is what makes the split reproducible. Rounding (not flooring) is the convention here: $n_c=2$ with $f=0.25$ rounds $0.5$ to $0$ (banker's rounding), while $n_c=2$ with $f=0.75$ gives $2$.
