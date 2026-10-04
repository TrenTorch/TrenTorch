---
name: problem-101-pca-projection
title: PCA Projection
tags: [unsupervised-ml, direct, medium, pca.]
difficulty: Intermediate
---

## Statement

Implement `solve(X, components, k)`. Project centered data onto the first k principal directions. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [[1, 0], [0, 1]], 1)
```

**Output**

```text
[[1], [3]]
```

**Explanation.** Project centered data onto the first k principal directions.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[4], [2]]
```

### Hint

matrix multiply by the component matrix

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is PCA Projection?

Project centered data onto the first k principal directions. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

PCA Projection supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **matrix multiply by the component matrix**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(X) @ np.asarray(components)[:, :k]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[[1,0],[0,1]],1)` returns `[[1], [3]]`. Reversing its observation rows returns `[[4], [2]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(X) @ np.asarray(components)[:, :k]` after preparing the intermediates for PCA Projection. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
