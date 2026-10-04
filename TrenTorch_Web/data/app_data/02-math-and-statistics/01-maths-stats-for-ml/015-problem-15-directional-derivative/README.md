---
name: problem-15-directional-derivative
title: Directional Derivative
tags: [maths-stats-for-ml, case-study, easy, calculus., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(grad, direction)`. Compute the directional derivative of a scalar function. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Datadog is scenario context only; this is not an official Datadog interview question or endorsement.

### Example 1

**Input**

```python
solve([3, 4], [1, 0])
```

**Output**

```text
3.0
```

**Explanation.** Compute the directional derivative of a scalar function.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
3.0
```

### Hint

normalize the direction before taking the dot product with the gradient

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Directional Derivative?

Compute the directional derivative of a scalar function. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Directional Derivative supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **normalize the direction before taking the dot product with the gradient**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(grad @ d)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([3,4],[1,0])` returns `3.0`. Reversing its observation rows returns `3.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.norm`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(grad @ d)` after preparing the intermediates for Directional Derivative. `np.asarray`, `np.linalg.norm` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
