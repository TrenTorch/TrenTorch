---
name: problem-3-cosine-similarity
title: Cosine Similarity
tags: [maths-stats-for-ml, case-study, easy, linear-algebra., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(a, b)`. Compute cosine similarity between two equal-length vectors. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Google is scenario context only; this is not an official Google interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 0], [1, 1])
```

**Output**

```text
0.7071067811865475
```

**Explanation.** Compute cosine similarity between two equal-length vectors.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.7071067811865475
```

### Hint

reuse the two norms and guard against a zero vector

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Cosine Similarity?

Compute cosine similarity between two equal-length vectors. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Cosine Similarity supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **reuse the two norms and guard against a zero vector**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `float(a @ b / (na * nb))`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,0],[1,1])` returns `0.7071067811865475`. Reversing its observation rows returns `0.7071067811865475`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.linalg.norm`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `float(a @ b / (na * nb))` after preparing the intermediates for Cosine Similarity. `np.asarray`, `np.linalg.norm` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
