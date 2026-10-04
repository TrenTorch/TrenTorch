---
name: problem-145-detect-vanishing-gradients
title: Detect Vanishing Gradients
tags: [dl-training-theory, direct, easy, gradient-stability.]
difficulty: Beginner
---

## Statement

Implement `solve(grad, threshold)`. Flag layers whose gradient norms fall below a threshold. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([0.001, 0.002], 0.01)
```

**Output**

```text
True
```

**Explanation.** Flag layers whose gradient norms fall below a threshold.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
True
```

### Hint

compare norms to threshold

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Detect Vanishing Gradients?

Flag layers whose gradient norms fall below a threshold. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Detect Vanishing Gradients supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **compare norms to threshold**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `n < threshold`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([.001,.002],.01)` returns `True`. Reversing its observation rows returns `True`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.norm`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `n < threshold` after preparing the intermediates for Detect Vanishing Gradients. `np.asarray`, `np.linalg.norm` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
