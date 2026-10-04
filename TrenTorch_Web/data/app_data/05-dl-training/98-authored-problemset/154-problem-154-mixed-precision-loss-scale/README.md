---
name: problem-154-mixed-precision-loss-scale
title: Mixed Precision Loss Scale
tags: [dl-training-theory, case-study, hard, numerical-stability., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(loss, scaled_grads, scale)`. Scale a loss before backward and unscale gradients safely. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Meesho is scenario context only; this is not an official Meesho interview question or endorsement.

### Example 1

**Input**

```python
solve(2, [[4, 8], [2]], 2)
```

**Output**

```text
(4, [[2.0, 4.0], [1.0]])
```

**Explanation.** Scale a loss before backward and unscale gradients safely.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(4, [[1.0], [2.0, 4.0]])
```

### Hint

multiply before backward and divide before update

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Mixed Precision Loss Scale?

Scale a loss before backward and unscale gradients safely. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Mixed Precision Loss Scale supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **multiply before backward and divide before update**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(scaled, unscaled)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(2,[[4,8],[2]],2)` returns `(4, [[2.0, 4.0], [1.0]])`. Reversing its observation rows returns `(4, [[1.0], [2.0, 4.0]])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(scaled, unscaled)` after preparing the intermediates for Mixed Precision Loss Scale. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
