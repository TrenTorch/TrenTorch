---
name: problem-46-linear-regression-normal-equation
title: Linear Regression Normal Equation
tags: [classical-ml, direct, hard, linear-regression.]
difficulty: Advanced
---

## Statement

Implement `solve(X, y)`. Implement the linear regression normal equation operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[0], [1], [2]], [1, 3, 5])
```

**Output**

```text
[1.0000000000000022, 1.999999999999998]
```

**Explanation.** Implement the linear regression normal equation operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[1.0000000000000022, 1.9999999999999978]
```

### Hint

augment X with a column of ones and solve the system

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Linear Regression Normal Equation?

Implement the linear regression normal equation operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Linear Regression Normal Equation supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **augment X with a column of ones and solve the system**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.linalg.pinv(A.T @ A) @ A.T @ y`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0],[1],[2]],[1,3,5])` returns `[1.0000000000000022, 1.999999999999998]`. Reversing its observation rows returns `[1.0000000000000022, 1.9999999999999978]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.c_`, `np.linalg.pinv`, `np.ones`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.linalg.pinv(A.T @ A) @ A.T @ y` after preparing the intermediates for Linear Regression Normal Equation. `np.asarray`, `np.c_`, `np.linalg.pinv`, `np.ones` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
