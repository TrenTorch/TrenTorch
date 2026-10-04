---
name: problem-181-transformer-feed-forward
title: Transformer Feed-Forward
tags: [transformer-llm, direct, easy, transformer-architecture.]
difficulty: Beginner
---

## Statement

Implement `solve(x, W1, b1, W2, b2)`. Implement the two-linear-layer position-wise feed-forward network. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2]], [[1, -1], [2, 1]], [0, 0], [[1], [2]], [0.5])
```

**Output**

```text
[[7.5]]
```

**Explanation.** Implement the two-linear-layer position-wise feed-forward network.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[8.5]]
```

### Hint

apply activation between projections

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Transformer Feed-Forward?

Implement the two-linear-layer position-wise feed-forward network. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Transformer Feed-Forward supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **apply activation between projections**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.maximum(0, np.asarray(x) @ W1 + b1) @ W2 + b2`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2]],[[1,-1],[2,1]],[0,0],[[1],[2]],[.5])` returns `[[7.5]]`. Reversing its observation rows returns `[[8.5]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.maximum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.maximum(0, np.asarray(x) @ W1 + b1) @ W2 + b2` after preparing the intermediates for Transformer Feed-Forward. `np.asarray`, `np.maximum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
