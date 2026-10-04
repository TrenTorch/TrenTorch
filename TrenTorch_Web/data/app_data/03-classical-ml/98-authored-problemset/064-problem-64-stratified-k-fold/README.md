---
name: problem-64-stratified-k-fold
title: Stratified K-Fold
tags: [classical-ml, direct, easy, cross-validation.]
difficulty: Beginner
---

## Statement

Implement `solve(y, k)`. Generate folds preserving binary class ratios. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0, 0, 1, 1, 1, 0], 3)
```

**Output**

```text
[([1, 3, 4, 5], [0, 2]), ([0, 2, 4, 5], [1, 3]), ([0, 2, 1, 3], [4, 5])]
```

**Explanation.** Generate folds preserving binary class ratios.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[([2, 4, 3, 5], [0, 1]), ([0, 1, 3, 5], [2, 4]), ([0, 1, 2, 4], [3, 5])]
```

### Hint

distribute shuffled class indices round-robin across folds

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Stratified K-Fold?

Generate folds preserving binary class ratios. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Stratified K-Fold supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **distribute shuffled class indices round-robin across folds**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,0,1,1,1,0],3)` returns `[([1, 3, 4, 5], [0, 2]), ([0, 2, 4, 5], [1, 3]), ([0, 2, 1, 3], [4, 5])]`. Reversing its observation rows returns `[([2, 4, 3, 5], [0, 1]), ([0, 1, 3, 5], [2, 4]), ([0, 1, 2, 4], [3, 5])]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.array`, `np.array_split`, `np.asarray`, `np.concatenate`, `np.unique`, `np.where`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]` after preparing the intermediates for Stratified K-Fold. `np.array`, `np.array_split`, `np.asarray`, `np.concatenate`, `np.unique`, `np.where` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
