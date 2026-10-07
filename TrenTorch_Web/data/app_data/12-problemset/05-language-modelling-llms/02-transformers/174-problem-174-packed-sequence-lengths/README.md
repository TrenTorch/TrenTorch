---
name: problem-174-packed-sequence-lengths
title: 'Packed Sequence Lengths'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'cumsum(lengths) - lengths'
tools: [NumPy]
---

## Statement

Compute the start offsets of variable-length sequences when they are concatenated end to end (a 'packed' batch): the exclusive cumulative sum of the lengths. Lengths must be non-negative.

Implement `solve(lengths)`.

**Returns.** Return an integer NumPy array with one offset per sequence (empty input gives an empty array); a negative length raises `ValueError`.

### Examples

**Example 1**

Input:

```python
solve([3, 1, 2])
```

Output:

```text
[0, 3, 4]
```

**Example 2**

Input:

```python
solve([0, 4, 0, 2])
```

Output:

```text
[0, 0, 4, 4]
```

## Theory

### The simple version

Padding wastes computation on filler tokens. Packing instead glues all sequences into one long array and remembers where each starts. The start of a sequence is simply the total length of everything before it.

### The formula

$$\text{offset}_i=\sum_{j<i}\ell_j=\Big(\sum_{j\le i}\ell_j\Big)-\ell_i$$

## Explanation

Sequence $i$ then occupies positions `offset[i] : offset[i] + length[i]` of the packed array. In the first example the offsets $0,3,4$ mean the sequences start at 0, 3 and 4. Zero-length sequences share the offset of the next sequence (second example).
