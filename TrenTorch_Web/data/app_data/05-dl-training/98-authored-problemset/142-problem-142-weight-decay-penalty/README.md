---
name: problem-142-weight-decay-penalty
title: Weight Decay Penalty
tags: [dl-training-theory, direct, hard, regularization.]
difficulty: Advanced
---

## Statement

Implement `solve(w, lam)`. Compute L2 weight decay contribution. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([1, -2, 3], 0.1)
```

**Output**

```text
1.4000000000000001
```

**Explanation.** Compute L2 weight decay contribution.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1.0500000000000003
```

### Hint

sum squared weights times coefficient

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Weight Decay Penalty?

Compute L2 weight decay contribution. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Weight Decay Penalty supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum squared weights times coefficient**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(lam * np.sum(w * w))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,-2,3],.1)` returns `1.4000000000000001`. Reversing its observation rows returns `1.0500000000000003`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(lam * np.sum(w * w))` after preparing the intermediates for Weight Decay Penalty. `np.asarray`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
