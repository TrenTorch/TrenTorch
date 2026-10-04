---
name: problem-76-random-forest-vote
title: Random Forest Vote
tags: [classical-ml-trees-ensembles, case-study, easy, random-forest., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(predictions)`. Implement the random forest vote operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Razorpay is scenario context only; this is not an official Razorpay interview question or endorsement.

### Example 1

**Input**

```python
solve((([[0,1,0],[1,1,0],[1,0,0]])))
```

**Output**

```text
[1, 1, 0]
```

**Explanation.** Implement the random forest vote operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1, 1, 0]
```

### Hint

majority vote with deterministic ties

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Random Forest Vote?

Implement the random forest vote operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Random Forest Vote supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **majority vote with deterministic ties**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.asarray(out)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0,1,0],[1,1,0],[1,0,0]])` returns `[1, 1, 0]`. Reversing its observation rows returns `[1, 1, 0]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`, `np.asarray`, `np.unique`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.asarray(out)` after preparing the intermediates for Random Forest Vote. `np.argmax`, `np.asarray`, `np.unique` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
