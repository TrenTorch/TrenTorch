---
name: problem-178-multi-head-attention-split
title: 'Multi-Head Attention Split'
tags: [problemset, transformer-llm, multi-head-attention]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'multi-head attention'
hint: 'reshape(B, T, H, F//H).transpose(0, 2, 1, 3)'
tools: [NumPy]
---

## Statement

Split the feature dimension of a batch into attention heads. `X` has shape `(batch, time, features)`; reshape the features into `n_heads` groups of `features // n_heads` and move the head axis forward. `features` must be divisible by a positive `n_heads`, otherwise `ValueError`.

Implement `solve(X, n_heads)`.

**Returns.** Return an array of shape `(batch, n_heads, time, features // n_heads)`.

### Examples

**Example 1**

Input:

```python
solve([[[1, 2, 3, 4], [5, 6, 7, 8]]], 2)
```

Output:

```text
[[[[1.0, 2.0], [5.0, 6.0]], [[3.0, 4.0], [7.0, 8.0]]]]
```

**Example 2**

Input:

```python
solve([[[1, 2, 3]]], 2)
```

Output: Raises `ValueError`.

## Theory

### The simple version

Multi-head attention runs several smaller attentions in parallel, each free to focus on a different kind of relationship. Instead of separate matrices, the model dimension is simply cut into equal slices and each slice becomes one head.

### The reshape

$$(B,\,T,\,H\!\cdot\!d_h)\;\longrightarrow\;(B,\,T,\,H,\,d_h)\;\longrightarrow\;(B,\,H,\,T,\,d_h)$$

## Explanation

In the first example the features $(1,2,3,4)$ become head 0 $=(1,2)$ and head 1 $=(3,4)$ for the first token. Moving the head axis in front of time lets each head's attention run as an ordinary batched matrix product.
