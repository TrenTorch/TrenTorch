---
name: problem-155-stable-logsumexp
title: Stable LogSumExp
tags: [dl-training-theory, case-study, hard, numerical-stability., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x)`. Compute log(sum(exp(x))) without overflow. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Ola is scenario context only; this is not an official Ola interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3])
```

**Output**

```text
3.4076059644443806
```

**Explanation.** Compute log(sum(exp(x))) without overflow.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
3.4076059644443806
```

### Hint

subtract max before exponentiating

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Stable LogSumExp?

Compute log(sum(exp(x))) without overflow. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Stable LogSumExp supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **subtract max before exponentiating**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(m + np.log(np.sum(np.exp(x - m))))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],)` returns `3.4076059644443806`. Reversing its observation rows returns `3.4076059644443806`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.exp`, `np.log`, `np.max`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(m + np.log(np.sum(np.exp(x - m))))` after preparing the intermediates for Stable LogSumExp. `np.asarray`, `np.exp`, `np.log`, `np.max`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
