---
name: problem-38-sample-size-for-proportion
title: Sample Size for Proportion
tags: [data-stats-for-ds, case-study, easy, experiment-design., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(p1, p2)`. Implement the sample size for proportion operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Palantir is scenario context only; this is not an official Palantir interview question or endorsement.

### Example 1

**Input**

```python
solve(0.1, 0.2)
```

**Output**

```text
398
```

**Explanation.** Implement the sample size for proportion operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
555
```

### Hint

use the standard normal-approximation formula

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Sample Size for Proportion?

Implement the sample size for proportion operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Sample Size for Proportion supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use the standard normal-approximation formula**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `int(np.ceil(2 * (z1 * np.sqrt(2 * p * (1 - p)) + z2 * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(.1,.2)` returns `398`. Reversing its observation rows returns `555`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.ceil`, `np.sqrt`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `int(np.ceil(2 * (z1 * np.sqrt(2 * p * (1 - p)) + z2 * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p1 - p2) ** 2))` after preparing the intermediates for Sample Size for Proportion. `np.ceil`, `np.sqrt` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
