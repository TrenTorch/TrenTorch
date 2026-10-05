---
name: problem-194-kv-cache-append
title: 'KV Cache Append'
tags: [problemset, transformer-llm, inference]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'inference'
hint: 'concatenate along sequence dimension'
tools: [NumPy]
---

## Statement

Append new_value to cache along sequence axis -2 and return the concatenated array.

Signature: `def solve(cache, new_value)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve(np.array([[1, 2], [3, 4]]), np.array([5, 6]))
```

Returns:

```python
[[1, 2], [3, 4], [5, 6]]
```

### Example 2

```python
solve(np.array([[0, 0], [0, 0]]), np.array([0, 0]))
```

Returns:

```python
[[0, 0], [0, 0], [0, 0]]
```

## Theory

Concatenate cache with a length-one sequence slice of new_value along axis -2.

## Explanation

Append new_value to cache along sequence axis -2 and return the concatenated array. The examples show concrete inputs and expected returned values.
