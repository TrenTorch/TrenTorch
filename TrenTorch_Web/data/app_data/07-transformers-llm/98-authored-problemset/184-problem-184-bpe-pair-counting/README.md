---
name: problem-184-bpe-pair-counting
title: BPE Pair Counting
tags: [transformer-llm, direct, easy, tokenization.]
difficulty: Beginner
---

## Statement

Implement `solve(corpus)`. Find the most frequent adjacent symbol pair in a corpus. Return only the specified value, preserving its shape and deterministic tie behavior.

### Example 1

**Input**

```python
solve((([['a','b','a','b'],['a','b','c']])))
```

**Output**

```text
(('a', 'b'), 3)
```

**Explanation.** Find the most frequent adjacent symbol pair in a corpus.

### Example 2

Reversing or changing the input values exercises the same contract on another valid case. The expected result is:

```text
(('a', 'b'), 3)
```

### Hint

count adjacent pairs across token sequences

### Constraints

- Inputs are finite and dimensionally compatible unless NaN, text, or random sampling is explicit.
- Dimensions are at most 512; probabilities, counts, and indices are in-domain.
- Empty, singular, and zero-denominator behavior follows the actual reference implementation; no undocumented clipping is expected.

## Theory

### What is BPE Pair Counting?

Find the most frequent adjacent symbol pair in a corpus. This is the particular statistic/transformation named here, returning exactly the requested scalar, array, or structure.

### Why it matters

BPE Pair Counting supports later machine-learning calculations. Incorrect scale, axes, dimensions, or ties can silently change a model's behavior.

### Process / mechanism

Convert inputs to the form required, compute the operation's intermediates, and return the specified object. The reference's key cue is **count adjacent pairs across token sequences**. Preserve the operation order and boundaries in the code.

### Mathematical representation

The exact object is represented by the reference expression `c.most_common(1)[0]`. Reductions use its stated axes and order; no other normalization or clipping is implied.

### Worked example

The input `([['a','b','a','b'],['a','b','c']])` returns `(('a', 'b'), 3)`. Reversing its observation rows returns `(('a', 'b'), 3)`. Compute each intermediate using the same steps rather than memorizing either output.

### Library implementation

The reference uses Python arithmetic/iteration. Vectorized NumPy operations run in optimized kernels; explicit loops remain for operations that are inherently sequential. Do not substitute a similarly named helper if its axes, variance convention, inclusivity, dtype, or tie order differ.

## Explanation

The code computes `c.most_common(1)[0]` after preparing the intermediates for BPE Pair Counting. Python arithmetic/iteration directly correspond to the contract. Tests cover the visible input, a reversed-order case, and an all-zero/boundary case; all expected values were obtained by executing this exact oracle.

**Complexity.** Vectorized transformations over n values use O(n) time and output space; scalar reductions use O(1) extra storage. Dense matrix products cost O(nd²) for n rows and d features.
