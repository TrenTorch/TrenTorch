---
name: problem-191-top-p-sampling
title: "Top-P Sampling"
tags: [problemset, transformer-llm, generation]
difficulty: Advanced
kind: problemset
relatedModule: "part-transformers-llm|Transformers"
topic: "generation"
hint: "sort probabilities and truncate the tail"
tools: [NumPy]
---

## Statement

Perform nucleus sampling: softmax logits, keep the smallest descending-probability prefix reaching p_cut, renormalize, then sample with rng.

Signature: `def solve(logits, p_cut, rng)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([0.0, 1.0, 2.0], 0.7, np.random.default_rng(3))
```

Returns:

```python
1
```

### Example 2

```python
solve([0.0, 5.0, -2.0], 0.2, np.random.default_rng(0))
```

Returns:

```python
1
```

## Theory

Include the token that reaches cumulative mass p_cut, then sample from retained normalized probabilities.

## Explanation

Perform nucleus sampling: softmax logits, keep the smallest descending-probability prefix reaching p_cut, renormalize, then sample with rng. The examples show concrete inputs and expected returned values.
