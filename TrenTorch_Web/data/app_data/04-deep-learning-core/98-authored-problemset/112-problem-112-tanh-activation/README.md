---
name: problem-112-tanh-activation
title: Tanh Activation
tags: [dl-core, case-study, easy, activation-functions., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Apply tanh element-wise. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Intel is scenario context only; this is not an official Intel interview question or endorsement.

### Example 1

**Input**

```python
solve([-2, 0, 2])
```

**Output**

```text
[-0.9640275800758169, 0.0, 0.9640275800758169]
```

**Explanation.** Apply tanh element-wise.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.9640275800758169, 0.0, -0.9640275800758169]
```

### Hint

use np.tanh

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Tanh Activation?

Apply tanh element-wise. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Tanh Activation supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use np.tanh**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.tanh(np.asarray(x))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([-2,0,2],)` returns `[-0.9640275800758169, 0.0, 0.9640275800758169]`. Reversing its observation rows returns `[0.9640275800758169, 0.0, -0.9640275800758169]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.tanh`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.tanh(np.asarray(x))` after preparing the intermediates for Tanh Activation. `np.asarray`, `np.tanh` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
