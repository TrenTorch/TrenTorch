---
name: problem-11-finite-difference-derivative
title: Finite Difference Derivative
tags: [maths-stats-for-ml, case-study, hard, calculus., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(f, x, h=1e-05)`. Estimate a scalar derivative at x using a centered finite difference. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Airbnb is scenario context only; this is not an official Airbnb interview question or endorsement.

### Example 1

**Input**

```python
solve(lambda z: z * z, 3)
```

**Output**

```text
6.000000000039306
```

**Explanation.** Estimate a scalar derivative at x using a centered finite difference.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
6.000000000039306
```

### Hint

evaluate f at x+h and x-h

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Finite Difference Derivative?

Estimate a scalar derivative at x using a centered finite difference. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Finite Difference Derivative supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **evaluate f at x+h and x-h**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float((f(x + h) - f(x - h)) / (2 * h))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(lambda z:z*z,3)` returns `6.000000000039306`. Reversing its observation rows returns `6.000000000039306`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float((f(x + h) - f(x - h)) / (2 * h))` after preparing the intermediates for Finite Difference Derivative. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
