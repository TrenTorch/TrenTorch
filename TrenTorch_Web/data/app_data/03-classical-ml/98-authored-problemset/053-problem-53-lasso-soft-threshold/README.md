---
name: problem-53-lasso-soft-threshold
title: Lasso Soft Threshold
tags: [classical-ml, case-study, medium, regularization., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(z, lam)`. Apply one coordinate-descent soft-threshold update. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** MongoDB is scenario context only; this is not an official MongoDB interview question or endorsement.

### Example 1

**Input**

```python
solve(3, 1)
```

**Output**

```text
2.0
```

**Explanation.** Apply one coordinate-descent soft-threshold update.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
2.0
```

### Hint

separate the smooth gradient from the L1 penalty

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Lasso Soft Threshold?

Apply one coordinate-descent soft-threshold update. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Lasso Soft Threshold supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **separate the smooth gradient from the L1 penalty**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.sign(z) * max(abs(z) - lam, 0.0)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(3,1)` returns `2.0`. Reversing its observation rows returns `2.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.sign`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.sign(z) * max(abs(z) - lam, 0.0)` after preparing the intermediates for Lasso Soft Threshold. `np.sign` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
