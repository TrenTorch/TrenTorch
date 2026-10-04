---
name: problem-25-one-hot-encode-categories
title: One-Hot Encode Categories
tags: [data-stats-for-ds, direct, easy, data-cleaning.]
difficulty: Beginner
---

## Statement

Implement `solve(values, categories)`. Convert categorical labels into a deterministic binary matrix. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(['b', 'a', 'b'], ['a', 'b', 'c'])
```

**Output**

```text
[[0, 1, 0], [1, 0, 0], [0, 1, 0]]
```

**Explanation.** Convert categorical labels into a deterministic binary matrix.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[0, 1, 0], [0, 0, 1], [0, 1, 0]]
```

### Hint

sort or preserve a supplied category order and set one column per label

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is One-Hot Encode Categories?

Convert categorical labels into a deterministic binary matrix. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

One-Hot Encode Categories supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sort or preserve a supplied category order and set one column per label**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(['b','a','b'],['a','b','c'])` returns `[[0, 1, 0], [1, 0, 0], [0, 1, 0]]`. Reversing its observation rows returns `[[0, 1, 0], [0, 0, 1], [0, 1, 0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.zeros`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for One-Hot Encode Categories. `np.zeros` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
