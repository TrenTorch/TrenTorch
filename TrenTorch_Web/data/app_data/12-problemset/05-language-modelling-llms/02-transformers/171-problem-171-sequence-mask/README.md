---
name: problem-171-sequence-mask
title: 'Sequence Mask'
tags: [problemset, sequence-models-attention, sequence-masking]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence masking'
hint: '(ids != pad_id) as int'
tools: [NumPy]
---

## Statement

Build a 0/1 mask of non-padding tokens: `1` where the id differs from `pad_id`, `0` where it equals `pad_id`.

Implement `solve(ids,pad_id)`.

**Returns.** Return an integer NumPy array of the same shape as `ids`.

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3], 2)
```

Output:

```text
[1, 0, 1]
```

**Example 2**

Input:

```python
solve([7, 7, 0, 0], 0)
```

Output:

```text
[1, 1, 0, 0]
```

## Theory

### The simple version

This is the integer version of the padding mask: a 1 for every real token and a 0 for every padded one. Multiplying values by it zeroes the padded positions, and summing it gives the real length of each sequence.

### The definition

$$m_j=\mathbb 1[\,\text{id}_j\ne\text{pad\_id}\,]\in\{0,1\}$$

## Explanation

The id that is _equal_ to the padding id is the one masked out, even if it is 'real' (first example, where the id $2$ is treated as padding). Pick a padding id that never occurs as a genuine token.
