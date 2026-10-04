---
name: problem-173-learned-positional-embeddings
title: Learned Positional Embeddings
tags: [sequence-models-attention, case-study, medium, positional-encoding., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(embeddings, length)`. Look up position embeddings for a sequence length. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** AWS is scenario context only; this is not an official AWS interview question or endorsement.

### Example 1

**Input**

```python
solve(np.array([[1, 2], [3, 4], [5, 6]]), 2)
```

**Output**

```text
[[1, 2], [3, 4]]
```

**Explanation.** Look up position embeddings for a sequence length.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[5, 6], [3, 4]]
```

### Hint

index an embedding matrix by position

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Learned Positional Embeddings?

Look up position embeddings for a sequence length. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Learned Positional Embeddings supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **index an embedding matrix by position**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `embeddings[np.arange(length)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(np.array([[1,2],[3,4],[5,6]]),2)` returns `[[1, 2], [3, 4]]`. Reversing its observation rows returns `[[5, 6], [3, 4]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.arange`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `embeddings[np.arange(length)]` after preparing the intermediates for Learned Positional Embeddings. `np.arange` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
