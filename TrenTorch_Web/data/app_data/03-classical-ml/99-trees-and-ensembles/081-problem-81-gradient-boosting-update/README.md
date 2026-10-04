---
name: problem-81-gradient-boosting-update
title: Gradient Boosting Update
tags: [classical-ml-trees-ensembles, case-study, hard, gradient-boosting., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(pred, weak_pred, learning_rate)`. Add a shrinkage-scaled weak learner prediction to the ensemble. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** NVIDIA is scenario context only; this is not an official NVIDIA interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2], [0.5, -1], 0.1)
```

**Output**

```text
[1.05, 1.9]
```

**Explanation.** Add a shrinkage-scaled weak learner prediction to the ensemble.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.925, 1.0375]
```

### Hint

pred += learning_rate*weak_pred

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Gradient Boosting Update?

Add a shrinkage-scaled weak learner prediction to the ensemble. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Gradient Boosting Update supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **pred += learning_rate\*weak_pred**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(pred, float) + learning_rate * np.asarray(weak_pred, float)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2],[.5,-1],.1)` returns `[1.05, 1.9]`. Reversing its observation rows returns `[1.925, 1.0375]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(pred, float) + learning_rate * np.asarray(weak_pred, float)` after preparing the intermediates for Gradient Boosting Update. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
