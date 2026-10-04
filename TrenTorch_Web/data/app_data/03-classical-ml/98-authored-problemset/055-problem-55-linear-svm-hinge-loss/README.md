---
name: problem-55-linear-svm-hinge-loss
title: Linear SVM Hinge Loss
tags: [classical-ml, case-study, medium, svm., company-case]
difficulty: Intermediate
---

## Statement

Implement `solve(y, scores)`. Compute mean hinge loss for binary labels in {-1,+1}. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Oracle is scenario context only; this is not an official Oracle interview question or endorsement.

### Example 1

**Input**

```python
solve([-1, 1, 1], [-0.5, 1.5, 0.2])
```

**Output**

```text
0.43333333333333335
```

**Explanation.** Compute mean hinge loss for binary labels in {-1,+1}.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.43333333333333335
```

### Hint

use max(0,1-y*s)

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Linear SVM Hinge Loss?

Compute mean hinge loss for binary labels in {-1,+1}. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Linear SVM Hinge Loss supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use max(0,1-y\*s)**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(np.mean(np.maximum(0, 1 - y * s)))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([-1,1,1],[-.5,1.5,.2])` returns `0.43333333333333335`. Reversing its observation rows returns `0.43333333333333335`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.maximum`, `np.mean`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(np.mean(np.maximum(0, 1 - y * s)))` after preparing the intermediates for Linear SVM Hinge Loss. `np.asarray`, `np.maximum`, `np.mean` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
