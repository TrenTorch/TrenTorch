---
name: problem-84-feature-importance-from-splits
title: Feature Importance from Splits
tags: [classical-ml-trees-ensembles, case-study, hard, feature-importance., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(splits)`. Accumulate impurity reduction by feature across tree nodes. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Shopify is scenario context only; this is not an official Shopify interview question or endorsement.

### Example 1

**Input**

```python
solve((([('a',2),('b',1),('a',3)])))
```

**Output**

```text
{'a': 0.8333333333333334, 'b': 0.16666666666666666}
```

**Explanation.** Accumulate impurity reduction by feature across tree nodes.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
{'a': 0.8333333333333334, 'b': 0.16666666666666666}
```

### Hint

sum reductions and normalize

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Feature Importance from Splits?

Accumulate impurity reduction by feature across tree nodes. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Feature Importance from Splits supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **sum reductions and normalize**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `{k: v / total for k, v in imp.items()} if total else imp`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([('a',2),('b',1),('a',3)])` returns `{'a': 0.8333333333333334, 'b': 0.16666666666666666}`. Reversing its observation rows returns `{'a': 0.8333333333333334, 'b': 0.16666666666666666}`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `{k: v / total for k, v in imp.items()} if total else imp` after preparing the intermediates for Feature Importance from Splits. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
