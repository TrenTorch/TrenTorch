---
name: problem-194-kv-cache-append
title: 'KV Cache Append'
tags: [problemset, transformer-llm, inference]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'inference'
hint: 'np.concatenate([cache, new_value[None, ...]], axis=-2)'
tools: [NumPy]
---

## Statement

Append the key/value vector of the newest token to a KV cache. The cache is a 2-D array of shape `(seq_len, dim)` and `new_value` is a vector of length `dim`; the new row is added at the end of the sequence axis (axis $-2$).

Implement `solve(cache, new_value)`.

**Returns.** Return an array of shape `(seq_len + 1, dim)`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], np.array([5.0, 6.0]))
```

Output:

```text
[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]
```

**Example 2**

Input:

```python
solve(np.zeros((0, 2)), np.array([1.0, 2.0]))
```

Output:

```text
[[1.0, 2.0]]
```

## Theory

### The simple version

When a Transformer generates text one token at a time, the keys and values of all earlier tokens never change. Recomputing them for every new token would waste enormous effort, so they are stored in a cache and each step only computes the new token's key and value and appends them.

### The update

$$K_{1:t}=[\,K_{1:t-1};\,k_t\,]$$

## Explanation

The new vector is given a leading length-1 axis and concatenated along the sequence axis. An empty cache of shape `(0, dim)` (second example) grows to a single row. The cache grows linearly with the sequence, which is why long contexts need a lot of memory.
