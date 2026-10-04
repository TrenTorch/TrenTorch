---
name: problem-65-bias-variance-decomposition
title: Bias-Variance Decomposition
tags: [classical-ml, direct, medium, bias-variance.]
difficulty: Intermediate
---

## Statement

Implement `solve(predictions, y)`. Estimate bias squared and variance from repeated predictions. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2], [2, 4], [3, 6]], [2, 3])
```

**Output**

```text
(0.5, 1.6666666666666665)
```

**Explanation.** Estimate bias squared and variance from repeated predictions.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(2.5, 1.6666666666666665)
```

### Hint

compare mean prediction with target and spread across models

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Bias-Variance Decomposition?

Estimate bias squared and variance from repeated predictions. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Bias-Variance Decomposition supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compare mean prediction with target and spread across models**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(float(np.mean((mean - y) ** 2)), float(np.mean(np.var(P, axis=0))))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[2,4],[3,6]],[2,3])` returns `(0.5, 1.6666666666666665)`. Reversing its observation rows returns `(2.5, 1.6666666666666665)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`, `np.var`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(float(np.mean((mean - y) ** 2)), float(np.mean(np.var(P, axis=0))))` after preparing the intermediates for Bias-Variance Decomposition. `np.asarray`, `np.mean`, `np.var` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
