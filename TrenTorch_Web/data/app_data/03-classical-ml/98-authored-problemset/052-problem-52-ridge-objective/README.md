---
name: problem-52-ridge-objective
title: Ridge Objective
tags: [classical-ml, case-study, easy, regularization., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(X, y, w, b, lam)`. Compute squared-error loss plus L2 penalty. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Twilio is scenario context only; this is not an official Twilio interview question or endorsement.

### Example 1

**Input**

```python
solve([[1], [2], [3]], [2, 4, 6], [1], 0, 0.1)
```

**Output**

```text
4.766666666666667
```

**Explanation.** Compute squared-error loss plus L2 penalty.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
4.741666666666667
```

### Hint

add lambda times squared weight norm

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Ridge Objective?

Compute squared-error loss plus L2 penalty. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Ridge Objective supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **add lambda times squared weight norm**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.mean(r * r) + lam * np.sum(np.asarray(w) ** 2))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1],[2],[3]],[2,4,6],[1],0,.1)` returns `4.766666666666667`. Reversing its observation rows returns `4.741666666666667`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.mean(r * r) + lam * np.sum(np.asarray(w) ** 2))` after preparing the intermediates for Ridge Objective. `np.asarray`, `np.mean`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
