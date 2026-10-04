---
name: problem-10-low-rank-reconstruction
title: Low-Rank Reconstruction
tags: [maths-stats-for-ml, case-study, hard, svd., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(A, k)`. Reconstruct a matrix using its first k singular components. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Stripe is scenario context only; this is not an official Stripe interview question or endorsement.

### Example 1

**Input**

```python
solve([[3, 0], [0, 2]], 1)
```

**Output**

```text
[[3.0, 0.0], [0.0, 0.0]]
```

**Explanation.** Reconstruct a matrix using its first k singular components.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[0.0, 0.0], [3.0, 0.0]]
```

### Hint

multiply U[:,:k], diag(S[:k]), and Vt[:k,:]

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Low-Rank Reconstruction?

Reconstruct a matrix using its first k singular components. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Low-Rank Reconstruction supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **multiply U[:,:k], diag(S[:k]), and Vt[:k,:]**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `U[:, :k] * S[:k] @ Vt[:k]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[3,0],[0,2]],1)` returns `[[3.0, 0.0], [0.0, 0.0]]`. Reversing its observation rows returns `[[0.0, 0.0], [3.0, 0.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.svd`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `U[:, :k] * S[:k] @ Vt[:k]` after preparing the intermediates for Low-Rank Reconstruction. `np.asarray`, `np.linalg.svd` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
