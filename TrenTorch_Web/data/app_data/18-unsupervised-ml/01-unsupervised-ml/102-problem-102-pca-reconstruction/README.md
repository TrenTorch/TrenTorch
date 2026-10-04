---
name: problem-102-pca-reconstruction
title: PCA Reconstruction
tags: [unsupervised-ml, case-study, medium, pca., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(Z, components, k, mean)`. Reconstruct data from a low-dimensional projection. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** CRED is scenario context only; this is not an official CRED interview question or endorsement.

### Example 1

**Input**

```python
solve([[1], [2]], [[1, 0], [0, 1]], 1, [10, 20])
```

**Output**

```text
[[11, 20], [12, 20]]
```

**Explanation.** Reconstruct data from a low-dimensional projection.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[20, 12], [20, 11]]
```

### Hint

multiply scores by components and add the mean

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is PCA Reconstruction?

Reconstruct data from a low-dimensional projection. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

PCA Reconstruction supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **multiply scores by components and add the mean**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(Z) @ np.asarray(components)[:, :k].T + np.asarray(mean)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1],[2]],[[1,0],[0,1]],1,[10,20])` returns `[[11, 20], [12, 20]]`. Reversing its observation rows returns `[[20, 12], [20, 11]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(Z) @ np.asarray(components)[:, :k].T + np.asarray(mean)` after preparing the intermediates for PCA Reconstruction. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
