---
name: problem-2-normalize-a-vector
title: Normalize a Vector
tags: [maths-stats-for-ml, direct, easy, linear-algebra.]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Return the unit vector for a non-zero vector. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([3, 4])
```

**Output**

```text
[0.6, 0.8]
```

**Explanation.** Return the unit vector for a non-zero vector.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.8, 0.6]
```

### Hint

compute the norm once and divide every component by it

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Normalize a Vector?

Return the unit vector for a non-zero vector. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Normalize a Vector supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compute the norm once and divide every component by it**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `x / n`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([3,4],)` returns `[0.6, 0.8]`. Reversing its observation rows returns `[0.8, 0.6]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.norm`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `x / n` after preparing the intermediates for Normalize a Vector. `np.asarray`, `np.linalg.norm` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
