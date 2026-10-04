---
name: problem-73-tree-leaf-majority
title: Tree Leaf Majority
tags: [classical-ml-trees-ensembles, case-study, easy, decision-trees., company-case]
difficulty: Beginner
---

## Statement

Implement `solve(y)`. Return the majority class for a leaf's labels. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** DoorDash is scenario context only; this is not an official DoorDash interview question or endorsement.

### Example 1

**Input**

```python
solve([1, 2, 2, 3])
```

**Output**

```text
2
```

**Explanation.** Return the majority class for a leaf's labels.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
2
```

### Hint

count classes and break ties deterministically

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Tree Leaf Majority?

Return the majority class for a leaf's labels. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Tree Leaf Majority supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count classes and break ties deterministically**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `u[np.argmax(c)]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([1,2,2,3],)` returns `2`. Reversing its observation rows returns `2`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses `np.argmax`, `np.unique`. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `u[np.argmax(c)]` after preparing the intermediates for Tree Leaf Majority. `np.argmax`, `np.unique` directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
