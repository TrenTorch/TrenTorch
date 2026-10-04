---
name: problem-12-gradient-of-a-quadratic
title: Gradient of a Quadratic
tags: [maths-stats-for-ml, case-study, hard, calculus., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(A, x, b)`. Return the gradient of 0.5*xᵀAx + bᵀx. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Meta is scenario context only; this is not an official Meta interview question or endorsement.

### Example 1

**Input**

```python
solve([[2, 0], [0, 4]], [1, 2], [1, -1])
```

**Output**

```text
[3.0, 7.0]
```

**Explanation.** Return the gradient of 0.5*xᵀAx + bᵀx.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[2.0, 7.0]
```

### Hint

use (A+Aᵀ)x/2 + b

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Gradient of a Quadratic?

Return the gradient of 0.5*xᵀAx + bᵀx. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Gradient of a Quadratic supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use (A+Aᵀ)x/2 + b**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `0.5 * (A + A.T) @ x + b`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[2,0],[0,4]],[1,2],[1,-1])` returns `[3.0, 7.0]`. Reversing its observation rows returns `[2.0, 7.0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `0.5 * (A + A.T) @ x + b` after preparing the intermediates for Gradient of a Quadratic. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
