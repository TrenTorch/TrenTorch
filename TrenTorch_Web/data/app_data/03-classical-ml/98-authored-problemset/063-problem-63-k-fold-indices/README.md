---
name: problem-63-k-fold-indices
title: K-Fold Indices
tags: [classical-ml, case-study, easy, cross-validation., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(n, k)`. Generate deterministic k-fold train/test index pairs. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Spotify is scenario context only; this is not an official Spotify interview question or endorsement.

### Example 1

**Input**

```python
solve(7, 3)
```

**Output**

```text
[([3, 4, 5, 6], [0, 1, 2]), ([0, 1, 2, 5, 6], [3, 4]), ([0, 1, 2, 3, 4], [5, 6])]
```

**Explanation.** Generate deterministic k-fold train/test index pairs.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[([3, 4, 5, 6], [0, 1, 2]), ([0, 1, 2, 5, 6], [3, 4]), ([0, 1, 2, 3, 4], [5, 6])]
```

### Hint

partition indices as evenly as possible

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is K-Fold Indices?

Generate deterministic k-fold train/test index pairs. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

K-Fold Indices supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **partition indices as evenly as possible**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `[(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(7,3)` returns `[([3, 4, 5, 6], [0, 1, 2]), ([0, 1, 2, 5, 6], [3, 4]), ([0, 1, 2, 3, 4], [5, 6])]`. Reversing its observation rows returns `[([3, 4, 5, 6], [0, 1, 2]), ([0, 1, 2, 5, 6], [3, 4]), ([0, 1, 2, 3, 4], [5, 6])]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.arange`, `np.array_split`, `np.concatenate`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `[(np.concatenate([f for j, f in enumerate(folds) if j != i]), folds[i]) for i in range(k)]` after preparing the intermediates for K-Fold Indices. `np.arange`, `np.array_split`, `np.concatenate` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
