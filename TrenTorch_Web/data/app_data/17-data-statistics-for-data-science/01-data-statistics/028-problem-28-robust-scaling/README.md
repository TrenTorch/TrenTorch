---
name: problem-28-robust-scaling
title: Robust Scaling
tags: [data-stats-for-ds, direct, easy, data-cleaning.]
difficulty: Beginner
---

## Statement

Implement `solve(x)`. Implement the robust scaling operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[1, 2], [3, 4], [100, 6]])
```

**Output**

```text
[[-0.04040404040404041, -1.0], [0.0, 0.0], [1.9595959595959596, 1.0]]
```

**Explanation.** Implement the robust scaling operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[1.9595959595959596, 1.0], [0.0, 0.0], [-0.04040404040404041, -1.0]]
```

### Hint

use Q3-Q1 and guard against zero IQR

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Robust Scaling?

Implement the robust scaling operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Robust Scaling supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use Q3-Q1 and guard against zero IQR**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.divide(X - med, iqr, out=np.zeros_like(X), where=iqr != 0)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,2],[3,4],[100,6]],)` returns `[[-0.04040404040404041, -1.0], [0.0, 0.0], [1.9595959595959596, 1.0]]`. Reversing its observation rows returns `[[1.9595959595959596, 1.0], [0.0, 0.0], [-0.04040404040404041, -1.0]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.divide`, `np.median`, `np.quantile`, `np.zeros_like`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.divide(X - med, iqr, out=np.zeros_like(X), where=iqr != 0)` after preparing the intermediates for Robust Scaling. `np.asarray`, `np.divide`, `np.median`, `np.quantile`, `np.zeros_like` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
