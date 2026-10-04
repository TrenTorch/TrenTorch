---
name: problem-116-linear-layer-forward
title: Linear Layer Forward
tags: [dl-core, case-study, medium, forward-pass., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(X, W, b)`. Implement the linear layer forward operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Microsoft is scenario context only; this is not an official Microsoft interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [[1, 0], [0, 1]], [0.5, -1])
```

**Output**

```text
[[1.5, 1.0], [3.5, 3.0]]
```

**Explanation.** Implement the linear layer forward operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[3.0, 3.5], [1.0, 1.5]]
```

### Hint

XW+b

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Linear Layer Forward?

Implement the linear layer forward operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Linear Layer Forward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **XW+b**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(X) @ np.asarray(W) + np.asarray(b)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[[1,0],[0,1]],[.5,-1])` returns `[[1.5, 1.0], [3.5, 3.0]]`. Reversing its observation rows returns `[[3.0, 3.5], [1.0, 1.5]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(X) @ np.asarray(W) + np.asarray(b)` after preparing the intermediates for Linear Layer Forward. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
