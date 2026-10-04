---
name: problem-194-kv-cache-append
title: KV Cache Append
tags: [transformer-llm, case-study, easy, inference., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(cache, new_value)`. Append one new key/value vector to a cached sequence. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Adobe is scenario context only; this is not an official Adobe interview question or endorsement.

### Example 1

**Input**

```python
solve(np.array([[1.0, 2.0], [3.0, 4.0]]), np.array([5.0, 6.0]))
```

**Output**

```text
[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
```

**Explanation.** Append one new key/value vector to a cached sequence.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[3.0, 4.0], [1.0, 2.0], [6.0, 5.0]]
```

### Hint

concatenate along sequence dimension

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is KV Cache Append?

Append one new key/value vector to a cached sequence. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

KV Cache Append supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **concatenate along sequence dimension**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.concatenate([cache, new_value[None, ...]], axis=-2)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(np.array([[1.,2.],[3.,4.]]),np.array([5.,6.]))` returns `[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]`. Reversing its observation rows returns `[[3.0, 4.0], [1.0, 2.0], [6.0, 5.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.concatenate`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.concatenate([cache, new_value[None, ...]], axis=-2)` after preparing the intermediates for KV Cache Append. `np.concatenate` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
