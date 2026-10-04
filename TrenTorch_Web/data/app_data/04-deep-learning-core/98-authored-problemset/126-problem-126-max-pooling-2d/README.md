---
name: problem-126-max-pooling-2d
title: Max Pooling 2D
tags: [dl-core, case-study, medium, cnn-basics., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(X, k, s=1)`. Implement the max pooling 2d operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** OpenAI is scenario context only; this is not an official OpenAI interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 3, 2], [4, 6, 5], [7, 8, 9]], 2, 1)
```

**Output**

```text
[[6.0, 6.0], [8.0, 9.0]]
```

**Explanation.** Implement the max pooling 2d operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[8.0, 9.0], [6.0, 6.0]]
```

### Hint

take maximum per window

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Max Pooling 2D?

Implement the max pooling 2d operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Max Pooling 2D supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **take maximum per window**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,3,2],[4,6,5],[7,8,9]],2,1)` returns `[[6.0, 6.0], [8.0, 9.0]]`. Reversing its observation rows returns `[[8.0, 9.0], [6.0, 6.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.empty`, `np.max`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for Max Pooling 2D. `np.asarray`, `np.empty`, `np.max` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
