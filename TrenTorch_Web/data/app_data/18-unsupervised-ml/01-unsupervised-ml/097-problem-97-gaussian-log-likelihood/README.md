---
name: problem-97-gaussian-log-likelihood
title: Gaussian Log Likelihood
tags: [unsupervised-ml, case-study, easy, gaussian-mixture., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(x, mu, cov)`. Implement the gaussian log likelihood operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Grab is scenario context only; this is not an official Grab interview question or endorsement.

### Example 1

**Input**

```python
solve([0, 0], [0, 0], [[1, 0], [0, 1]])
```

**Output**

```text
-1.8378770664093453
```

**Explanation.** Implement the gaussian log likelihood operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
-1.8378770664093453
```

### Hint

use quadratic form and log determinant

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Gaussian Log Likelihood?

Implement the gaussian log likelihood operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Gaussian Log Likelihood supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use quadratic form and log determinant**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(-0.5 * (d * np.log(2 * np.pi) + ld + (x - mu) @ np.linalg.solve(S, x - mu)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,0],[0,0],[[1,0],[0,1]])` returns `-1.8378770664093453`. Reversing its observation rows returns `-1.8378770664093453`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.slogdet`, `np.linalg.solve`, `np.log`, `np.pi`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(-0.5 * (d * np.log(2 * np.pi) + ld + (x - mu) @ np.linalg.solve(S, x - mu)))` after preparing the intermediates for Gaussian Log Likelihood. `np.asarray`, `np.linalg.slogdet`, `np.linalg.solve`, `np.log`, `np.pi` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
