---
name: problem-66-polynomial-features
title: Polynomial Features
tags: [classical-ml, case-study, medium, feature-engineering., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x, degree)`. Implement the polynomial features operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Stripe is scenario context only; this is not an official Stripe interview question or endorsement.

### Example 1

**Input**

```python
solve([2, 3], 3)
```

**Output**

```text
[[2.0, 4.0, 8.0], [3.0, 9.0, 27.0]]
```

**Explanation.** Implement the polynomial features operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[3.0, 9.0, 27.0], [2.0, 4.0, 8.0]]
```

### Hint

construct a Vandermonde-style matrix

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Polynomial Features?

Implement the polynomial features operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Polynomial Features supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **construct a Vandermonde-style matrix**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.column_stack([x ** d for d in range(1, degree + 1)])`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([2,3],3)` returns `[[2.0, 4.0, 8.0], [3.0, 9.0, 27.0]]`. Reversing its observation rows returns `[[3.0, 9.0, 27.0], [2.0, 4.0, 8.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.column_stack`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.column_stack([x ** d for d in range(1, degree + 1)])` after preparing the intermediates for Polynomial Features. `np.asarray`, `np.column_stack` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
