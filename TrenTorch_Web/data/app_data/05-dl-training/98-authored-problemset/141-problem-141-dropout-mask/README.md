---
name: problem-141-dropout-mask
title: Dropout Mask
tags: [dl-training-theory, case-study, hard, regularization., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x, keep_prob, seed=0)`. Apply inverted dropout during training. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Pinterest is scenario context only; this is not an official Pinterest interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 4], 0.5, 0)
```

**Output**

```text
[0.0, 4.0, 6.0, 8.0]
```

**Explanation.** Apply inverted dropout during training.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.0, 8.0, 5.333333333333333, 2.6666666666666665]
```

### Hint

sample Bernoulli mask and divide by keep probability

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Dropout Mask?

Apply inverted dropout during training. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Dropout Mask supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sample Bernoulli mask and divide by keep probability**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(x) * mask / keep_prob`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4],.5,0)` returns `[0.0, 4.0, 6.0, 8.0]`. Reversing its observation rows returns `[0.0, 8.0, 5.333333333333333, 2.6666666666666665]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.random.default_rng`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(x) * mask / keep_prob` after preparing the intermediates for Dropout Mask. `np.asarray`, `np.random.default_rng` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
