---
name: problem-117-linear-layer-backward
title: Linear Layer Backward
tags: [dl-core, case-study, hard, backpropagation., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, dY, W)`. Implement the linear layer backward operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** AWS is scenario context only; this is not an official AWS interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4]], [[1, 2], [3, 4]], [[1, 0], [0, 1]])
```

**Output**

```text
([[1, 2], [3, 4]], [[10, 14], [14, 20]], [4, 6])
```

**Explanation.** Implement the linear layer backward operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([[4, 3], [2, 1]], [[10, 14], [14, 20]], [4, 6])
```

### Hint

apply chain rule to matrix products

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Linear Layer Backward?

Implement the linear layer backward operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Linear Layer Backward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **apply chain rule to matrix products**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(dY @ W.T, X.T @ dY, dY.sum(0))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4]],[[1,2],[3,4]],[[1,0],[0,1]])` returns `([[1, 2], [3, 4]], [[10, 14], [14, 20]], [4, 6])`. Reversing its observation rows returns `([[4, 3], [2, 1]], [[10, 14], [14, 20]], [4, 6])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(dY @ W.T, X.T @ dY, dY.sum(0))` after preparing the intermediates for Linear Layer Backward. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
