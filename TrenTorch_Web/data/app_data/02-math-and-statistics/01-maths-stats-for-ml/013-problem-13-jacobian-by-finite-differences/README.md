---
name: problem-13-jacobian-by-finite-differences
title: Jacobian by Finite Differences
tags: [maths-stats-for-ml, case-study, easy, calculus., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(f, x, h=1e-05)`. Estimate the Jacobian of a vector-valued function. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Apple is scenario context only; this is not an official Apple interview question or endorsement.

### Example 1

**Input**

```python
solve(lambda z: np.array([z[0] ** 2, z[0] * z[1]]), [2, 3])
```

**Output**

```text
[[4.000000000026205, 0.0], [3.000000000064062, 2.0000000000131024]]
```

**Explanation.** Estimate the Jacobian of a vector-valued function.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[6.000000000039306, 0.0], [2.0000000000131024, 3.000000000064062]]
```

### Hint

perturb one input coordinate at a time

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Jacobian by Finite Differences?

Estimate the Jacobian of a vector-valued function. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Jacobian by Finite Differences supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **perturb one input coordinate at a time**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `J`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(lambda z:np.array([z[0]**2,z[0]*z[1]]),[2,3])` returns `[[4.000000000026205, 0.0], [3.000000000064062, 2.0000000000131024]]`. Reversing its observation rows returns `[[6.000000000039306, 0.0], [2.0000000000131024, 3.000000000064062]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.zeros`, `np.zeros_like`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `J` after preparing the intermediates for Jacobian by Finite Differences. `np.asarray`, `np.zeros`, `np.zeros_like` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
