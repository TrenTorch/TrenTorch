---
name: problem-170-sequence-padding
title: 'Sequence Padding'
tags: [problemset, sequence-models-attention, sequence-padding]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'sequence padding'
hint: 'np.full((n, max_len), pad_value) then copy each sequence into its row'
tools: [NumPy]
---

## Statement

Right-pad variable-length sequences to the length of the longest one. `sequences` is a list of lists and `pad_value` (default 0) fills the missing positions.

Implement `solve(sequences, pad_value=0)`.

**Returns.** Return a tuple `(padded, lengths)`: a 2-D NumPy array of shape `(n_sequences, max_length)` and an integer array with the original lengths.

### Examples

**Example 1**

Input:

```python
solve([[1, 2, 3], [4]], 0)
```

Output:

```text
([[1, 2, 3], [4, 0, 0]], [3, 1])
```

**Example 2**

Input:

```python
solve([[], [7, 8]], -1)
```

Output:

```text
([[-1, -1], [7, 8]], [0, 2])
```

## Theory

### The simple version

Neural networks process rectangular batches, but sentences have different lengths. The standard fix is to pad the short ones with a filler value up to the longest length, and to remember the true lengths so the filler can be masked out later.

### The result

$$\text{padded}_{i,t}=\begin{cases}s_{i,t}&t<\ell_i\\\text{pad\_value}&t\ge\ell_i\end{cases}$$

### Why it matters

- Networks process rectangular batches, but sentences differ in length, so short ones must be padded.
- Keeping the true lengths lets you mask the padding later or pack the batch.

### How it works

1. Record each sequence's length.
2. Find the longest.
3. Create a matrix filled with the padding value and copy each sequence into the start of its row.

### Worked example

The sequences $(1,2,3)$ and $(4)$ have lengths $3$ and $1$. The second is padded with two zeros to $(4,0,0)$, so the result is ([[1, 2, 3], [4, 0, 0]], [3, 1]).

## Explanation

The width is the maximum length, and an empty sequence becomes a row of padding (second example). The returned lengths let you build the padding mask or pack the batch without padding.
