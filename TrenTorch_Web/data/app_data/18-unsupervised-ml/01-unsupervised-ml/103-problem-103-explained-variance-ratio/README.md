---
name: problem-103-explained-variance-ratio
title: Explained Variance Ratio
tags: [unsupervised-ml, direct, medium, pca.]
difficulty: Intermediate
---

## Statement

Implement `solve(eigenvalues)`. Convert eigenvalues into explained variance ratios. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([3, 1, 0])
```

**Output**

```text
[0.75, 0.25, 0.0]
```

**Explanation.** Convert eigenvalues into explained variance ratios.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.0, 0.25, 0.75]
```

### Hint

divide each eigenvalue by their sum

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Explained Variance Ratio?

Convert eigenvalues into explained variance ratios. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Explained Variance Ratio supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **divide each eigenvalue by their sum**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `e / e.sum()`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([3,1,0],)` returns `[0.75, 0.25, 0.0]`. Reversing its observation rows returns `[0.0, 0.25, 0.75]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `e / e.sum()` after preparing the intermediates for Explained Variance Ratio. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
