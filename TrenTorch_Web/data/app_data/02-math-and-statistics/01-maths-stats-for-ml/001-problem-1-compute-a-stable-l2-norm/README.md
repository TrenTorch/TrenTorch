---
name: problem-1-compute-a-stable-l2-norm
title: Compute a Stable L2 Norm
tags: [maths-stats-for-ml, direct, easy, linear-algebra.]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Given a vector of real values, compute its Euclidean norm without unnecessary overflow or underflow. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([3, 4])
```

**Output**

```text
5.0
```

**Explanation.** Given a vector of real values, compute its Euclidean norm without unnecessary overflow or underflow.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
5.0
```

### Hint

scale the vector by its largest absolute value before squaring

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Compute a Stable L2 Norm?

Given a vector of real values, compute its Euclidean norm without unnecessary overflow or underflow. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Compute a Stable L2 Norm supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **scale the vector by its largest absolute value before squaring**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(scale * np.sqrt(np.sum((x / scale) ** 2)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([3,4],)` returns `5.0`. Reversing its observation rows returns `5.0`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.abs`, `np.asarray`, `np.max`, `np.sqrt`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(scale * np.sqrt(np.sum((x / scale) ** 2)))` after preparing the intermediates for Compute a Stable L2 Norm. `np.abs`, `np.asarray`, `np.max`, `np.sqrt`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
