---
name: problem-111-sigmoid-activation
title: Sigmoid Activation
tags: [dl-core, case-study, easy, activation-functions., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Apply sigmoid to a vector of logits. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Oracle is scenario context only; this is not an official Oracle interview question or endorsement.

### Example 1

**Input**

```python
solve([-100, 0, 2, 100])
```

**Output**

```text
[3.720075976020836e-44, 0.5, 0.8807970779778823, 1.0]
```

**Explanation.** Apply sigmoid to a vector of logits.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.0, 0.8807970779778823, 0.5, 3.720075976020836e-44]
```

### Hint

use a numerically stable branch

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Sigmoid Activation?

Apply sigmoid to a vector of logits. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Sigmoid Activation supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use a numerically stable branch**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `out`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([-100,0,2,100],)` returns `[3.720075976020836e-44, 0.5, 0.8807970779778823, 1.0]`. Reversing its observation rows returns `[1.0, 0.8807970779778823, 0.5, 3.720075976020836e-44]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.empty_like`, `np.exp`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `out` after preparing the intermediates for Sigmoid Activation. `np.asarray`, `np.empty_like`, `np.exp` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
