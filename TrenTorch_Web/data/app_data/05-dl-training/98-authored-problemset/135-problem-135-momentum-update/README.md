---
name: problem-135-momentum-update
title: Momentum Update
tags: [dl-training-theory, case-study, easy, optimizers., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(w, v, grad, lr, mu)`. Update velocity and parameters with momentum. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** ByteDance is scenario context only; this is not an official ByteDance interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2], [0, 0], [0.1, -0.2], 0.5, 0.9)
```

**Output**

```text
([0.1, -0.2], [0.95, 2.1])
```

**Explanation.** Update velocity and parameters with momentum.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([-0.2, 0.1], [2.075, 0.9625])
```

### Hint

v=mu*v+grad; w-=lr*v

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Momentum Update?

Update velocity and parameters with momentum. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Momentum Update supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **v=mu*v+grad; w-=lr*v**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(v, np.asarray(w) - lr * v)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2],[0,0],[.1,-.2],.5,.9)` returns `([0.1, -0.2], [0.95, 2.1])`. Reversing its observation rows returns `([-0.2, 0.1], [2.075, 0.9625])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(v, np.asarray(w) - lr * v)` after preparing the intermediates for Momentum Update. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
