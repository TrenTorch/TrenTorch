---
name: problem-113-softmax-vector
title: Softmax Vector
tags: [dl-core, case-study, medium, activation-functions., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(x)`. Convert logits into a probability vector. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Netflix is scenario context only; this is not an official Netflix interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3])
```

**Output**

```text
[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]
```

**Explanation.** Convert logits into a probability vector.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.6652409557748218, 0.24472847105479764, 0.09003057317038046]
```

### Hint

subtract the maximum logit before exponentiation

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Softmax Vector?

Convert logits into a probability vector. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Softmax Vector supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **subtract the maximum logit before exponentiation**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `p / p.sum(axis=-1, keepdims=True)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],)` returns `[0.09003057317038046, 0.24472847105479764, 0.6652409557748218]`. Reversing its observation rows returns `[0.6652409557748218, 0.24472847105479764, 0.09003057317038046]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.exp`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `p / p.sum(axis=-1, keepdims=True)` after preparing the intermediates for Softmax Vector. `np.asarray`, `np.exp` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
