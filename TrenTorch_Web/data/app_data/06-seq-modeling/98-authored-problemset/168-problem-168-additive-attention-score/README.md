---
name: problem-168-additive-attention-score
title: Additive Attention Score
tags: [sequence-models-attention, case-study, hard, attention-mechanism., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(Q, K, Wq, Wk)`. Implement the additive attention score operation. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Intel is scenario context only; this is not an official Intel interview question or endorsement.

### Example 1

**Input**

```python
solve([[1, 0]], [[1, 0], [0, 1]], [[1, 0], [0, 1]], [[0, 1], [1, 0]])
```

**Output**

```text
[1.5231883119115297, 0.9640275800758169]
```

**Explanation.** Implement the additive attention score operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[0.9640275800758169, 1.5231883119115297]
```

### Hint

apply tanh to a learned projection sum

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Additive Attention Score?

Implement the additive attention score operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Additive Attention Score supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **apply tanh to a learned projection sum**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `np.tanh(np.asarray(Q) @ Wq + np.asarray(K) @ Wk).sum(-1)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([[1,0]],[[1,0],[0,1]],[[1,0],[0,1]],[[0,1],[1,0]])` returns `[1.5231883119115297, 0.9640275800758169]`. Reversing its observation rows returns `[0.9640275800758169, 1.5231883119115297]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.asarray`, `np.tanh`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `np.tanh(np.asarray(Q) @ Wq + np.asarray(K) @ Wk).sum(-1)` after preparing the intermediates for Additive Attention Score. `np.asarray`, `np.tanh` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
