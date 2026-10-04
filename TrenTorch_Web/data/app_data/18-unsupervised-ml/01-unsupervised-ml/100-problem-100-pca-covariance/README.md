---
name: problem-100-pca-covariance
title: PCA Covariance
tags: [unsupervised-ml, direct, easy, pca.]
difficulty: Beginner
---

## Statement

Implement `solve(X)`. Compute the sample covariance matrix. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4], [5, 8]])
```

**Output**

```text
[[4.0, 6.0], [6.0, 9.333333333333332]]
```

**Explanation.** Compute the sample covariance matrix.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[4.0, 6.0], [6.0, 9.333333333333332]]
```

### Hint

center X and divide XᵀX by n-1

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is PCA Covariance?

Compute the sample covariance matrix. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

PCA Covariance supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **center X and divide XᵀX by n-1**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `Z.T @ Z / (len(X) - 1)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4],[5,8]],)` returns `[[4.0, 6.0], [6.0, 9.333333333333332]]`. Reversing its observation rows returns `[[4.0, 6.0], [6.0, 9.333333333333332]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `Z.T @ Z / (len(X) - 1)` after preparing the intermediates for PCA Covariance. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
