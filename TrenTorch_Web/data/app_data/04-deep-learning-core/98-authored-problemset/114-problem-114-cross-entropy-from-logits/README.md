---
name: problem-114-cross-entropy-from-logits
title: Cross-Entropy from Logits
tags: [dl-core, case-study, medium, loss-functions., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(logits, target)`. Compute categorical cross-entropy for one labeled example. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Uber is scenario context only; this is not an official Uber interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3], 2)
```

**Output**

```text
0.4076059644443804
```

**Explanation.** Compute categorical cross-entropy for one labeled example.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
2.4076059644443806
```

### Hint

use log-sum-exp and subtract the target logit

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Cross-Entropy from Logits?

Compute categorical cross-entropy for one labeled example. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Cross-Entropy from Logits supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use log-sum-exp and subtract the target logit**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(-np.mean(np.sum(target * lp, axis=-1)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],2)` returns `0.4076059644443804`. Reversing its observation rows returns `2.4076059644443806`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.exp`, `np.log`, `np.mean`, `np.sum`, `np.take_along_axis`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(-np.mean(np.sum(target * lp, axis=-1)))` after preparing the intermediates for Cross-Entropy from Logits. `np.asarray`, `np.exp`, `np.log`, `np.mean`, `np.sum`, `np.take_along_axis` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
