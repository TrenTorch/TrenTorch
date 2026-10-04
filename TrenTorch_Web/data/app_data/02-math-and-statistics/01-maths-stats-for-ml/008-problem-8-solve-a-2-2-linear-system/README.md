---
name: problem-8-solve-a-2-2-linear-system
title: Solve a 2×2 Linear System
tags: [maths-stats-for-ml, direct, medium, linear-algebra.]
difficulty: Intermediate
---

## Statement

Implement `solve(coeffs)`. Implement the solve a 2×2 linear system operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve((2, 1, 1, 3, 5, 6))
```

**Output**

```text
[1.8, 1.4]
```

**Explanation.** Implement the solve a 2×2 linear system operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.8, 1.4]
```

### Hint

use the closed-form determinant and handle a zero determinant

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Solve a 2×2 Linear System?

Implement the solve a 2×2 linear system operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Solve a 2×2 Linear System supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use the closed-form determinant and handle a zero determinant**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.array([(e * d - b * f) / det, (a * f - e * c) / det])`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `((2,1,1,3,5,6),)` returns `[1.8, 1.4]`. Reversing its observation rows returns `[1.8, 1.4]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.array`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.array([(e * d - b * f) / det, (a * f - e * c) / det])` after preparing the intermediates for Solve a 2×2 Linear System. `np.array` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
