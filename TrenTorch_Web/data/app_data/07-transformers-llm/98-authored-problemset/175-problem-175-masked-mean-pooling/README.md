---
name: problem-175-masked-mean-pooling
title: Masked Mean Pooling
tags: [sequence-models-attention, case-study, medium, sequence-padding., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(E, mask)`. Average token embeddings while ignoring padding. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Spotify is scenario context only; this is not an official Spotify interview question or endorsement.

### Example 1

**Input**

```python
solve([[[1, 2], [3, 4], [5, 6]], [[2, 4], [6, 8], [10, 12]]], [[1, 1, 0], [1, 0, 0]])
```

**Output**

```text
[[2.0, 3.0], [2.0, 4.0]]
```

**Explanation.** Average token embeddings while ignoring padding.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[2.0, 4.0], [2.0, 3.0]]
```

### Hint

sum masked embeddings and divide by valid counts

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Masked Mean Pooling?

Average token embeddings while ignoring padding. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Masked Mean Pooling supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum masked embeddings and divide by valid counts**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(E * m).sum(1) / np.maximum(m.sum(1), 1)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[[1,2],[3,4],[5,6]],[[2,4],[6,8],[10,12]]],[[1,1,0],[1,0,0]])` returns `[[2.0, 3.0], [2.0, 4.0]]`. Reversing its observation rows returns `[[2.0, 4.0], [2.0, 3.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.maximum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(E * m).sum(1) / np.maximum(m.sum(1), 1)` after preparing the intermediates for Masked Mean Pooling. `np.asarray`, `np.maximum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
