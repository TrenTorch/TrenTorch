---
name: problem-106-support-counting
title: Support Counting
tags: [unsupervised-ml, direct, hard, association-rules.]
difficulty: Advanced
---

## Statement

Implement `solve(transactions, itemset)`. Implement the support counting operation. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve([['a', 'b'], ['a'], ['b', 'c']], ['a'])
```

**Output**

```text
0.6666666666666666
```

**Explanation.** Implement the support counting operation.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
0.6666666666666666
```

### Hint

test subset inclusion for each transaction

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is Support Counting?

Implement the support counting operation. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

Support Counting supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **test subset inclusion for each transaction**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `sum((item.issubset(set(t)) for t in transactions)) / len(transactions)`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([['a','b'],['a'],['b','c']],['a'])` returns `0.6666666666666666`. Reversing its observation rows returns `0.6666666666666666`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `sum((item.issubset(set(t)) for t in transactions)) / len(transactions)` after preparing the intermediates for Support Counting. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
