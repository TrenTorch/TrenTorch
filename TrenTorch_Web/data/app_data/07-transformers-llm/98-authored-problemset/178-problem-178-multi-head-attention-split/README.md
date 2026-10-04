---
name: problem-178-multi-head-attention-split
title: Multi-Head Attention Split
tags: [transformer-llm, case-study, hard, multi-head-attention., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(X, n_heads)`. Implement the multi-head attention split operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Stripe is scenario context only; this is not an official Stripe interview question or endorsement.

### Example 1

**Input**

```python
solve(np.ones((2, 3, 8)), 4)
```

**Output**

```text
[[[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]], [[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]]
```

**Explanation.** Implement the multi-head attention split operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]], [[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]]
```

### Hint

reshape and transpose to head-major form

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Multi-Head Attention Split?

Implement the multi-head attention split operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Multi-Head Attention Split supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **reshape and transpose to head-major form**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `X.reshape(B, T, n_heads, D // n_heads).transpose(0, 2, 1, 3)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(np.ones((2,3,8)),4)` returns `[[[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]], [[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]]`. Reversing its observation rows returns `[[[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]], [[[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]], [[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]]]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `X.reshape(B, T, n_heads, D // n_heads).transpose(0, 2, 1, 3)` after preparing the intermediates for Multi-Head Attention Split. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
