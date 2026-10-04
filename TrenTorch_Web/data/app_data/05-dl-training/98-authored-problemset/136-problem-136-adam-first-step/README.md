---
name: problem-136-adam-first-step
title: Adam First Step
tags: [dl-training-theory, case-study, easy, optimizers., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(w, g, m, v, t, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-08)`. Implement the adam first step operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** TikTok is scenario context only; this is not an official TikTok interview question or endorsement.

### Example 1

**Input**

```python
solve([1.0, 2.0], [0.1, -0.2], [0.0, 0.0], [0.0, 0.0], 1, 0.01)
```

**Output**

```text
([0.9900000009999999, 2.0099999995], [0.009999999999999998, -0.019999999999999997], [1.0000000000000011e-05, 4.0000000000000044e-05])
```

**Explanation.** Implement the adam first step operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
([2.007499999625, 0.9925000007499999], [-0.019999999999999997, 0.009999999999999998], [4.0000000000000044e-05, 1.0000000000000011e-05])
```

### Hint

maintain first and second moments

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Adam First Step?

Implement the adam first step operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Adam First Step supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **maintain first and second moments**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(w - lr * mh / (np.sqrt(vh) + eps), m, v)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1.,2.],[.1,-.2],[0.,0.],[0.,0.],1,.01)` returns `([0.9900000009999999, 2.0099999995], [0.009999999999999998, -0.019999999999999997], [1.0000000000000011e-05, 4.0000000000000044e-05])`. Reversing its observation rows returns `([2.007499999625, 0.9925000007499999], [-0.019999999999999997, 0.009999999999999998], [4.0000000000000044e-05, 1.0000000000000011e-05])`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sqrt`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(w - lr * mh / (np.sqrt(vh) + eps), m, v)` after preparing the intermediates for Adam First Step. `np.asarray`, `np.sqrt` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
