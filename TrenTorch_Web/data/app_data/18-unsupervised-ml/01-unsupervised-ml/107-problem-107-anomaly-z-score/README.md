---
name: problem-107-anomaly-z-score
title: Anomaly Z-Score
tags: [unsupervised-ml, direct, hard, anomaly-detection.]
difficulty: Advanced
---

## Statement

Implement `solve(x)`. Implement the anomaly z-score operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([[0, 1], [1, 2], [2, 3], [100, 4]])
```

**Output**

```text
[[-0.6005958529659056, -1.3416407864998738], [-0.5772717421711131, -0.4472135954999579], [-0.5539476313763206, 0.4472135954999579], [1.7318152265133393, 1.3416407864998738]]
```

**Explanation.** Implement the anomaly z-score operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[[1.7318152265133393, 1.3416407864998738], [-0.5539476313763206, 0.4472135954999579], [-0.5772717421711131, -0.4472135954999579], [-0.6005958529659056, -1.3416407864998738]]
```

### Hint

standardize using training mean and std

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Anomaly Z-Score?

Implement the anomaly z-score operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Anomaly Z-Score supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **standardize using training mean and std**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.divide(X - mu, sd, out=np.zeros_like(X), where=sd != 0)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[0,1],[1,2],[2,3],[100,4]],)` returns `[[-0.6005958529659056, -1.3416407864998738], [-0.5772717421711131, -0.4472135954999579], [-0.5539476313763206, 0.4472135954999579], [1.7318152265133393, 1.3416407864998738]]`. Reversing its observation rows returns `[[1.7318152265133393, 1.3416407864998738], [-0.5539476313763206, 0.4472135954999579], [-0.5772717421711131, -0.4472135954999579], [-0.6005958529659056, -1.3416407864998738]]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.divide`, `np.zeros_like`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.divide(X - mu, sd, out=np.zeros_like(X), where=sd != 0)` after preparing the intermediates for Anomaly Z-Score. `np.asarray`, `np.divide`, `np.zeros_like` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
