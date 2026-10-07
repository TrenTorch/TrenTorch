---
name: problem-175-masked-mean-pooling
title: 'Masked Mean Pooling'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'sum of masked embeddings divided by the number of valid tokens (0 if none)'
tools: [NumPy]
---

## Statement

Average token embeddings over the valid (non-padding) positions of each sequence. `embeddings` has shape `(batch, time, dim)` and `mask` has shape `(batch, time)` with `True` for real tokens. A sequence with no valid token gets the zero vector.

Implement `solve(embeddings, mask)`.

**Returns.** Return an array of shape `(batch, dim)`.

### Examples

**Example 1**

Input:

```python
solve([[[1.0, 1.0], [3.0, 3.0]]], [[True, True]])
```

Output:

```text
[[2.0, 2.0]]
```

**Example 2**

Input:

```python
solve([[[1.0, 1.0], [3.0, 3.0]]], [[True, False]])
```

Output:

```text
[[1.0, 1.0]]
```

**Example 3**

Input:

```python
solve([[[5.0, 5.0]]], [[False]])
```

Output:

```text
[[0.0, 0.0]]
```

## Theory

### The simple version

To get one vector for a sentence you can average its token vectors. A plain mean would also average in the padding vectors and give a different answer depending on how much padding the batch happened to have. Masked mean pooling sums only the real tokens and divides by how many there are.

### The formula

$$\bar e_b=\frac{\sum_tm_{bt}\,e_{bt}}{\sum_tm_{bt}}$$

## Explanation

Masked-out entries are zeroed before summing and the denominator is the count of valid tokens, so padding has no influence. When the count is $0$ (third example) the division is skipped and zeros are returned instead of `NaN`.
