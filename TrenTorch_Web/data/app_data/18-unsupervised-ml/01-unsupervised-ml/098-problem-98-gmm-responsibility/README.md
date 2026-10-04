---
name: problem-98-gmm-responsibility
title: GMM Responsibility
tags: [unsupervised-ml, case-study, easy, gaussian-mixture., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x, weights, means, covs)`. Implement the gmm responsibility operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Meesho is scenario context only; this is not an official Meesho interview question or endorsement.

### Example 1

**Input**

```python
solve([0], [0.5, 0.5], [[0], [2]], [[[1]], [[1]]])
```

**Output**

```text
[0.8807970779778823, 0.11920292202211755]
```

**Explanation.** Implement the gmm responsibility operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.11920292202211755, 0.8807970779778823]
```

### Hint

evaluate log probabilities then apply log-sum-exp

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is GMM Responsibility?

Implement the gmm responsibility operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

GMM Responsibility supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **evaluate log probabilities then apply log-sum-exp**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `q / q.sum()`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0],[.5,.5],[[0],[2]],[[[1]],[[1]]])` returns `[0.8807970779778823, 0.11920292202211755]`. Reversing its observation rows returns `[0.11920292202211755, 0.8807970779778823]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.array`, `np.asarray`, `np.exp`, `np.linalg.slogdet`, `np.linalg.solve`, `np.log`, `np.max`, `np.pi`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `q / q.sum()` after preparing the intermediates for GMM Responsibility. `np.array`, `np.asarray`, `np.exp`, `np.linalg.slogdet`, `np.linalg.solve`, `np.log`, `np.max`, `np.pi` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
