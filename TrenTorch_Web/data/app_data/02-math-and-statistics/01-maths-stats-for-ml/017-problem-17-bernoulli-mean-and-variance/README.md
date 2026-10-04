---
name: problem-17-bernoulli-mean-and-variance
title: Bernoulli Mean and Variance
tags: [maths-stats-for-ml, case-study, medium, probability., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x)`. Implement the bernoulli mean and variance operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** DoorDash is scenario context only; this is not an official DoorDash interview question or endorsement.

### Example 1

**Input**

```python
solve([0, 1, 1, 0, 1])
```

**Output**

```text
(0.6, 0.24)
```

**Explanation.** Implement the bernoulli mean and variance operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(0.6, 0.24)
```

### Hint

use p̂ and p̂(1-p̂)

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Bernoulli Mean and Variance?

Implement the bernoulli mean and variance operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Bernoulli Mean and Variance supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use p̂ and p̂(1-p̂)**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(p, p * (1 - p))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([0,1,1,0,1],)` returns `(0.6, 0.24)`. Reversing its observation rows returns `(0.6, 0.24)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(p, p * (1 - p))` after preparing the intermediates for Bernoulli Mean and Variance. `np.asarray`, `np.mean` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
