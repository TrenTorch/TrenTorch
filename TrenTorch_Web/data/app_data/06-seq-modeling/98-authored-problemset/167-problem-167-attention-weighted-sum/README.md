---
name: problem-167-attention-weighted-sum
title: Attention Weighted Sum
tags: [sequence-models-attention, direct, hard, attention-mechanism.]
difficulty: Advanced
---

## Statement

Implement `solve(weights, V)`. Implement the attention weighted sum operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0.2, 0.8], [[2, 0], [0, 4]])
```

**Output**

```text
[0.4, 3.2]
```

**Explanation.** Implement the attention weighted sum operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.4, 3.2]
```

### Hint

matrix multiply weights by V

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Attention Weighted Sum?

Implement the attention weighted sum operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Attention Weighted Sum supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **matrix multiply weights by V**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(weights) @ np.asarray(V)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([.2,.8],[[2,0],[0,4]])` returns `[0.4, 3.2]`. Reversing its observation rows returns `[0.4, 3.2]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(weights) @ np.asarray(V)` after preparing the intermediates for Attention Weighted Sum. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
