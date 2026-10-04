---
name: problem-22-entropy-of-a-distribution
title: Entropy of a Distribution
tags: [maths-stats-for-ml, direct, hard, information-theory.]
difficulty: Advanced
---

## Statement

Implement `solve(p)`. Compute Shannon entropy for a discrete probability vector. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0.5, 0.5])
```

**Output**

```text
1.0
```

**Explanation.** Compute Shannon entropy for a discrete probability vector.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1.0
```

### Hint

sum -p log2 p over positive probabilities

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Entropy of a Distribution?

Compute Shannon entropy for a discrete probability vector. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Entropy of a Distribution supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum -p log2 p over positive probabilities**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(-np.sum(p * np.log2(p)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([.5,.5],)` returns `1.0`. Reversing its observation rows returns `1.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.log2`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(-np.sum(p * np.log2(p)))` after preparing the intermediates for Entropy of a Distribution. `np.asarray`, `np.log2`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
