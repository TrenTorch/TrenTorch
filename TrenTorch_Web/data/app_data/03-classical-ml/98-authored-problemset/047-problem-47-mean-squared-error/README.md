---
name: problem-47-mean-squared-error
title: Mean Squared Error
tags: [classical-ml, direct, hard, metrics.]
difficulty: Advanced
---

## Statement

Implement `solve(y, pred)`. Implement the mean squared error operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([1, 2, 3], [1, 4, 2])
```

**Output**

```text
1.6666666666666667
```

**Explanation.** Implement the mean squared error operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
1.6666666666666667
```

### Hint

average squared residuals

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Mean Squared Error?

Implement the mean squared error operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Mean Squared Error supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **average squared residuals**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.mean((np.asarray(y, float) - np.asarray(pred, float)) ** 2))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,3],[1,4,2])` returns `1.6666666666666667`. Reversing its observation rows returns `1.6666666666666667`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.mean`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.mean((np.asarray(y, float) - np.asarray(pred, float)) ** 2))` after preparing the intermediates for Mean Squared Error. `np.asarray`, `np.mean` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
