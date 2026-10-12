---
name: problem-173-learned-positional-embeddings
title: 'Learned Positional Embeddings'
tags: [problemset, sequence-models-attention, positional-encoding]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'positional encoding'
hint: 'table[:length], with a range check'
tools: [NumPy]
---

## Statement

Look up positional embeddings: from a learned table with one row per position, return the first `length` rows. `length` must be between 0 and the number of rows, otherwise `ValueError`.

Implement `solve(embeddings, length)`.

**Returns.** Return a copy of `table[:length]`.

### Examples

**Example 1**

Input:

```python
solve([[0, 0], [1, 1], [2, 2]], 2)
```

Output:

```text
[[0, 0], [1, 1]]
```

**Example 2**

Input:

```python
solve([[2, 3], [4, 5]], 1)
```

Output:

```text
[[2, 3]]
```

## Theory

### The simple version

Instead of fixed sine waves, many models (BERT, GPT-2) simply learn one vector per position. A sequence of length $L$ uses the first $L$ rows of the table and adds them to the token embeddings. The price is a hard maximum length: positions beyond the table size have no embedding.

### The lookup

$$P=E_{\text{pos}}[0:L]\in\mathbb R^{L\times d}$$

### Why it matters

- Many models (BERT, GPT-2) learn one embedding vector per position instead of using fixed sinusoids.
- A sequence of length $L$ uses the first $L$ rows, and positions beyond the table have no embedding.

### How it works

1. Check $0\le L\le$ number of table rows.
2. Return a copy of the first $L$ rows.

### Worked example

Taking the first $2$ of $3$ rows from the table $(0,0),(1,1),(2,2)$ gives [[0, 0], [1, 1]].

## Explanation

The slice is copied so later changes to the result do not modify the learned table. Asking for more positions than the table holds raises an error because there is nothing learned for them.
