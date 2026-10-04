---
name: problem-105-apriori-candidate-join
title: Apriori Candidate Join
tags: [unsupervised-ml, case-study, hard, association-rules., company-case]
difficulty: Advanced
---

## Statement

Implement `solve(prev)`. Generate k-item candidates from frequent (k-1)-itemsets. Return only the specified value, preserving its shape and deterministic tie behavior.

> **Case-study disclaimer:** Discord is scenario context only; this is not an official Discord interview question or endorsement.

### Example 1

**Input**

```python
solve([(1, 2), (1, 3), (2, 3)])
```

**Output**

```text
[(1, 2, 3)]
```

**Explanation.** Generate k-item candidates from frequent (k-1)-itemsets.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
[(1, 2, 3)]
```

### Hint

join compatible sorted prefixes

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Apriori Candidate Join?

Generate k-item candidates from frequent (k-1)-itemsets. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Apriori Candidate Join supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **join compatible sorted prefixes**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `sorted(out)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([(1,2),(1,3),(2,3)],)` returns `[(1, 2, 3)]`. Reversing its observation rows returns `[(1, 2, 3)]`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `sorted(out)` after preparing the intermediates for Apriori Candidate Join. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
