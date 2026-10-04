---
name: problem-31-stratified-split
title: Stratified Split
tags: [data-stats-for-ds, case-study, medium, sampling., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(y, test_size=0.2, seed=0)`. Split indices into train and test while preserving class proportions. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Lyft is scenario context only; this is not an official Lyft interview question or endorsement.

### Example 1

**Input**

```python
solve([0, 0, 0, 0, 1, 1, 1, 1], 0.25, 7)
```

**Output**

```text
([1, 2, 3, 4, 5, 6], [0, 7])
```

**Explanation.** Split indices into train and test while preserving class proportions.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([0, 1, 2, 3, 4, 5, 6, 7], [])
```

### Hint

shuffle indices within each class then allocate each class separately

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Stratified Split?

Split indices into train and test while preserving class proportions. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Stratified Split supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **shuffle indices within each class then allocate each class separately**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(np.array(sorted(train)), np.array(sorted(test)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,0,0,0,1,1,1,1],.25,7)` returns `([1, 2, 3, 4, 5, 6], [0, 7])`. Reversing its observation rows returns `([0, 1, 2, 3, 4, 5, 6, 7], [])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.array`, `np.asarray`, `np.random.default_rng`, `np.unique`, `np.where`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(np.array(sorted(train)), np.array(sorted(test)))` after preparing the intermediates for Stratified Split. `np.array`, `np.asarray`, `np.random.default_rng`, `np.unique`, `np.where` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
