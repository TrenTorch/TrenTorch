---
name: problem-31-stratified-split
title: 'Stratified Split'
tags: [problemset, data-stats-for-ds, sampling]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'sampling'
hint: 'split each class separately: shuffle its indices, floor(count * test_size) go to test'
tools: [NumPy]
---

## Statement

Split the indices of a label vector into a train set and a test set so that every class keeps (approximately) the same proportion in both. Within each class the indices are shuffled with `np.random.default_rng(seed)` and the first `int(count * test_size)` of them go to the test set.

Implement `solve(y, test_size=0.2, seed=0)`.

**Returns.** Return a tuple `(train_idx, test_idx)` of two sorted NumPy index arrays. Because of `int(...)` the number of test items per class is rounded **down**, so a class with fewer than $1/\text{test\_size}$ members contributes nothing to the test set.

### Examples

**Example 1**

Input:

```python
solve([0, 0, 0, 0, 1, 1, 1, 1], 0.5, 0)
```

Output:

```text
([1, 3, 4, 5], [0, 2, 6, 7])
```

**Example 2**

Input:

```python
solve([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], 0.25, 3)
```

Output:

```text
([0, 1, 2, 3, 4, 5, 8, 9], [6, 7])
```

## Theory

### The simple version

A plain random split can, by bad luck, put almost all of a rare class into the training set and none in the test set. A stratified split avoids that by splitting each class separately, so the class mix of the whole dataset is mirrored in both parts.

### The recipe

For every class $c$ with $n_c$ members: shuffle its indices, send $\lfloor n_c\cdot\text{test\_size}\rfloor$ of them to the test set and keep the rest for training. Finally merge the per-class pieces and sort them.

### Why it matters

- A plain random split can leave a rare class almost out of the test set, making its metrics meaningless.
- Splitting each class separately keeps the class mix of the full data in both parts.

### How it works

1. For each class, shuffle its indices with the seeded generator.
2. Send $\lfloor n_c\cdot\text{test\_size}\rfloor$ of them to the test set.
3. Merge the pieces and sort.

### Worked example

With eight samples, four per class, and `test_size=0.5`, each class sends $\lfloor4\cdot0.5\rfloor=2$ indices to the test set. That gives the split ([1, 3, 4, 5], [0, 2, 6, 7]): four train and four test indices, two of each class on each side.

## Explanation

The shuffle uses a single generator seeded once, so the result is reproducible for a given `seed` and class order (`np.unique` visits classes in sorted order). Flooring the test count is the simplest rule and guarantees the test set never exceeds the requested fraction; the price is that very small classes can end up absent from the test set.
