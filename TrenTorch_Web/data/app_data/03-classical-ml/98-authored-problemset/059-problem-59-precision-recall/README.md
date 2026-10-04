---
name: problem-59-precision-recall
title: Precision Recall
tags: [classical-ml, case-study, hard, metrics., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(y, pred)`. Implement the precision recall operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Google is scenario context only; this is not an official Google interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 0, 1, 0, 1], [1, 1, 0, 0, 1])
```

**Output**

```text
(0.6666666666666666, 0.6666666666666666)
```

**Explanation.** Implement the precision recall operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(0.6666666666666666, 0.6666666666666666)
```

### Hint

count TP, FP, and FN explicitly

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Precision Recall?

Implement the precision recall operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Precision Recall supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count TP, FP, and FN explicitly**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `(tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,0,1,0,1],[1,1,0,0,1])` returns `(0.6666666666666666, 0.6666666666666666)`. Reversing its observation rows returns `(0.6666666666666666, 0.6666666666666666)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.sum`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `(tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0)` after preparing the intermediates for Precision Recall. `np.asarray`, `np.sum` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
