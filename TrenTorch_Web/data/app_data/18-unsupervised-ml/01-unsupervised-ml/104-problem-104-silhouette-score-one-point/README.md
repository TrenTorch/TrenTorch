---
name: problem-104-silhouette-score-one-point
title: Silhouette Score One Point
tags: [unsupervised-ml, direct, medium, clustering-metrics.]
difficulty: Intermediate
---

## Statement

Implement `solve(intra, nearest)`. Compute a point's silhouette coefficient from intra- and nearest-cluster distances. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([1, 2], [3, 4])
```

**Output**

```text
0.5
```

**Explanation.** Compute a point's silhouette coefficient from intra- and nearest-cluster distances.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.5
```

### Hint

use (b-a)/max(a,b)

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Silhouette Score One Point?

Compute a point's silhouette coefficient from intra- and nearest-cluster distances. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Silhouette Score One Point supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **use (b-a)/max(a,b)**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `0.0 if max(a, b) == 0 else (b - a) / max(a, b)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2],[3,4])` returns `0.5`. Reversing its observation rows returns `0.5`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.mean`, `np.min`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `0.0 if max(a, b) == 0 else (b - a) / max(a, b)` after preparing the intermediates for Silhouette Score One Point. `np.mean`, `np.min` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
