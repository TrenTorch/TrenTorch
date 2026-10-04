---
name: problem-131-encoder-bottleneck
title: Encoder Bottleneck
tags: [dl-core, case-study, hard, autoencoders., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, W, b)`. Implement a linear bottleneck projection. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Swiggy is scenario context only; this is not an official Swiggy interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [[1, 0], [0, 1]], [0.5, -1])
```

**Output**

```text
[[1.5, 1.0], [3.5, 3.0]]
```

**Explanation.** Implement a linear bottleneck projection.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[3.0, 3.5], [1.0, 1.5]]
```

### Hint

compress X with an encoder matrix

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Encoder Bottleneck?

Implement a linear bottleneck projection. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Encoder Bottleneck supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compress X with an encoder matrix**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(X) @ np.asarray(W) + np.asarray(b)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[[1,0],[0,1]],[.5,-1])` returns `[[1.5, 1.0], [3.5, 3.0]]`. Reversing its observation rows returns `[[3.0, 3.5], [1.0, 1.5]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(X) @ np.asarray(W) + np.asarray(b)` after preparing the intermediates for Encoder Bottleneck. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
