---
name: problem-40-group-aggregation
title: Group Aggregation
tags: [data-stats-for-ds, direct, easy, data-wrangling.]
difficulty: Beginner
---

## Statement

Implement `solve(keys, values)`. Aggregate numeric values by a categorical key without pandas groupby. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve(['a', 'b', 'a', 'c'], [2, 4, 6, 8])
```

**Output**

```text
{'a': 4.0, 'b': 4.0, 'c': 8.0}
```

**Explanation.** Aggregate numeric values by a categorical key without pandas groupby.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
{'c': 8.0, 'a': 4.0, 'b': 4.0}
```

### Hint

build a dictionary of running sum and count

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Group Aggregation?

Aggregate numeric values by a categorical key without pandas groupby. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Group Aggregation supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **build a dictionary of running sum and count**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `{k: s / n for k, (s, n) in acc.items()}`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `(['a','b','a','c'],[2,4,6,8])` returns `{'a': 4.0, 'b': 4.0, 'c': 8.0}`. Reversing its observation rows returns `{'c': 8.0, 'a': 4.0, 'b': 4.0}`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `{k: s / n for k, (s, n) in acc.items()}` after preparing the intermediates for Group Aggregation. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
