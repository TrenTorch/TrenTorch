---
name: problem-190-top-k-sampling
title: "Top-K Sampling"
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "generation"
hint: "mask all but top-k before softmax"
tools: [NumPy]
---

## Statement

Sample an index after retaining the k largest logits. Softmax retained logits and sample with the supplied NumPy generator.

Signature: `def solve(logits, k, rng)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([0.0, 1.0, 2.0], 2, np.random.default_rng(3))
```

Returns:

```python
1
```

### Example 2

```python
solve([1.0, 4.0, -2.0], 1, np.random.default_rng(0))
```

Returns:

```python
1
```

## Theory

Top-k truncation retains k logits, normalizes with softmax, then samples an original index.

## Explanation

Sample an index after retaining the k largest logits. Softmax retained logits and sample with the supplied NumPy generator. The examples show concrete inputs and expected returned values.
