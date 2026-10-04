---
name: problem-72-decision-stump
title: Decision Stump
tags: [classical-ml-trees-ensembles, case-study, hard, decision-trees., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(x, y)`. Train a depth-1 classifier on one numeric feature. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Snowflake is scenario context only; this is not an official Snowflake interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 3, 4], [0, 0, 1, 1])
```

**Output**

```text
(2, 0, 1)
```

**Explanation.** Train a depth-1 classifier on one numeric feature.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(2, 0, 1)
```

### Hint

choose the split with lowest weighted impurity

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Decision Stump?

Train a depth-1 classifier on one numeric feature. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Decision Stump supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **choose the split with lowest weighted impurity**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(t, mode(left), mode(right))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3,4],[0,0,1,1])` returns `(2, 0, 1)`. Reversing its observation rows returns `(2, 0, 1)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`, `np.asarray`, `np.sum`, `np.unique`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(t, mode(left), mode(right))` after preparing the intermediates for Decision Stump. `np.argmax`, `np.asarray`, `np.sum`, `np.unique` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
