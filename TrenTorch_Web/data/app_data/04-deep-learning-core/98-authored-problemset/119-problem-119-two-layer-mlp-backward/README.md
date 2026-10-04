---
name: problem-119-two-layer-mlp-backward
title: Two-Layer MLP Backward
tags: [dl-core, case-study, hard, backpropagation., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, dY, W1, W2, cache)`. Implement the two-layer mlp backward operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Spotify is scenario context only; this is not an official Spotify interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 2], [2, 1]], [[1], [2]], [[1, -1], [1, 1]], [[1], [2]], (np.array([[1, 1], [3, 3]]), np.array([[1, 3], [0, 5]])))
```

**Output**

```text
([[-1, 3], [-2, 6]], [[5, 10], [4, 8]], [3, 6], [[1], [13]], [3])
```

**Explanation.** Implement the two-layer mlp backward operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([[6, 2], [3, 1]], [[10, 5], [8, 4]], [6, 3], [[1], [13]], [3])
```

### Hint

reverse the forward operations

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Two-Layer MLP Backward?

Implement the two-layer mlp backward operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Two-Layer MLP Backward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **reverse the forward operations**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(dz @ W1.T, X.T @ dz, dz.sum(0), dW2, db2)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[2,1]],[[1],[2]],[[1,-1],[1,1]],[[1],[2]],(np.array([[1,1],[3,3]]),np.array([[1,3],[0,5]])))` returns `([[-1, 3], [-2, 6]], [[5, 10], [4, 8]], [3, 6], [[1], [13]], [3])`. Reversing its observation rows returns `([[6, 2], [3, 1]], [[10, 5], [8, 4]], [6, 3], [[1], [13]], [3])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(dz @ W1.T, X.T @ dz, dz.sum(0), dW2, db2)` after preparing the intermediates for Two-Layer MLP Backward. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
