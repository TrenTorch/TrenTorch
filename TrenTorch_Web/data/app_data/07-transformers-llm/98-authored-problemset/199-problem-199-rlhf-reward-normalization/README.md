---
name: problem-199-rlhf-reward-normalization
title: RLHF Reward Normalization
tags: [transformer-llm, case-study, medium, rlhf-intuition., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(rewards)`. Implement the rlhf reward normalization operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Lyft is scenario context only; this is not an official Lyft interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3])
```

**Output**

```text
[-1.224744871391589, 0.0, 1.224744871391589]
```

**Explanation.** Implement the rlhf reward normalization operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.224744871391589, 0.0, -1.224744871391589]
```

### Hint

standardize reward values

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is RLHF Reward Normalization?

Implement the rlhf reward normalization operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

RLHF Reward Normalization supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **standardize reward values**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(r - r.mean()) / r.std()`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],)` returns `[-1.224744871391589, 0.0, 1.224744871391589]`. Reversing its observation rows returns `[1.224744871391589, 0.0, -1.224744871391589]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(r - r.mean()) / r.std()` after preparing the intermediates for RLHF Reward Normalization. `np.asarray` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
