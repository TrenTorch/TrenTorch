---
name: problem-176-vocabulary-frequency-count
title: 'Vocabulary Frequency Count'
tags: [problemset, sequence-models-attention, sequence-modeling]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence modeling'
hint: 'Counter, sort by (-count, first-seen index), slice to k'
tools: [NumPy]
---

## Statement

Return the `k` most frequent tokens with their counts. Tokens with equal counts are ordered by their first appearance in the input. `k` must be non-negative.

Implement `solve(tokens, k)`.

**Returns.** Return a list of `(token, count)` tuples of length at most `k`, from most to least frequent.

### Examples

**Example 1**

Input:

```python
solve(['a', 'b', 'a', 'c', 'b', 'a'], 2)
```

Output:

```text
[('a', 3), ('b', 2)]
```

**Example 2**

Input:

```python
solve(['x', 'y', 'x', 'y', 'z'], 3)
```

Output:

```text
[('x', 2), ('y', 2), ('z', 1)]
```

## Theory

### The simple version

Building a vocabulary starts with counting. Keeping only the most frequent tokens bounds the vocabulary size, and everything rarer is mapped to an _unknown_ token. Frequency tables also show the long-tailed (Zipf-like) distribution of words.

### The procedure

1. Count every token.
2. Sort by count, largest first, breaking ties by first occurrence.
3. Keep the first $k$.

## Explanation

Tie-breaking by first appearance makes the output deterministic. In the second example `'x'` and `'y'` both occur twice and `'x'` appears first, so it is listed first.
