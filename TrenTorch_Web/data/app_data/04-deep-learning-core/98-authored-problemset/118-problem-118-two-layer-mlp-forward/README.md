---
name: problem-118-two-layer-mlp-forward
title: Two-Layer MLP Forward
tags: [dl-core, case-study, hard, forward-pass., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, W1, b1, W2, b2)`. Implement the two-layer mlp forward operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Amazon is scenario context only; this is not an official Amazon interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [[1, -1], [2, 1]], [0, 0], [[1], [2]], [0.5])
```

**Output**

```text
([[7.5], [13.5]], ([[5, 1], [11, 1]], [[5, 1], [11, 1]]))
```

**Explanation.** Implement the two-layer mlp forward operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([[20.5], [8.5]], ([[10, -1], [4, -1]], [[10, 0], [4, 0]]))
```

### Hint

cache hidden preactivation for backward

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Two-Layer MLP Forward?

Implement the two-layer mlp forward operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Two-Layer MLP Forward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **cache hidden preactivation for backward**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(h @ W2 + b2, (z1, h))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[[1,-1],[2,1]],[0,0],[[1],[2]],[.5])` returns `([[7.5], [13.5]], ([[5, 1], [11, 1]], [[5, 1], [11, 1]]))`. Reversing its observation rows returns `([[20.5], [8.5]], ([[10, -1], [4, -1]], [[10, 0], [4, 0]]))`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.maximum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(h @ W2 + b2, (z1, h))` after preparing the intermediates for Two-Layer MLP Forward. `np.asarray`, `np.maximum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
