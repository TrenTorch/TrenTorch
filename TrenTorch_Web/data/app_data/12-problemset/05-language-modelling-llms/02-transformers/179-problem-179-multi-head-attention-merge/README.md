---
name: problem-179-multi-head-attention-merge
title: 'Multi-Head Attention Merge'
tags: [problemset, transformer-llm, multi-head-attention]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'multi-head attention'
hint: 'transpose(0, 2, 1, 3).reshape(B, T, H*width)'
tools: [NumPy]
---

## Statement

Merge attention heads back into the model dimension: the inverse of the head split. `heads` has shape `(batch, n_heads, time, width)`.

Implement `solve(heads)`.

**Returns.** Return an array of shape `(batch, time, n_heads * width)` in which the heads of each token are concatenated in head order.

### Examples

**Example 1**

Input:

```python
solve([[[[1, 2], [5, 6]], [[3, 4], [7, 8]]]])
```

Output:

```text
[[[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]]
```

**Example 2**

Input:

```python
solve([[[[1.0]], [[2.0]], [[3.0]]]])
```

Output:

```text
[[[1.0, 2.0, 3.0]]]
```

## Theory

### The simple version

After every head has produced its own output, the results are laid side by side again so the next layer sees one vector per token. Splitting and merging are exact inverses, so a split followed by a merge returns the original array.

### The reshape

$$(B,\,H,\,T,\,d_h)\;\longrightarrow\;(B,\,T,\,H,\,d_h)\;\longrightarrow\;(B,\,T,\,H\!\cdot\!d_h)$$

### Why it matters

- After per-head attention the heads are joined back.
- It is the inverse of the split.

### How it works

1. Move the head axis after time.
2. Reshape to concatenate the heads.

### Worked example

Head $0=(1,2)$ and head $1=(3,4)$ for the first token join as $(1,2,3,4)$: [[[1.0, 2.0, 3.0, 4.0], [5.0, 6.0, 7.0, 8.0]]].

## Explanation

The first example reproduces the input of the split example: the token vectors $(1,2,3,4)$ and $(5,6,7,8)$. The transpose has to come before the reshape, otherwise values from different tokens would be mixed.
