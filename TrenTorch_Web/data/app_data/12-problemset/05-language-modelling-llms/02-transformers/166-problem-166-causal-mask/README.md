---
name: problem-166-causal-mask
title: 'Causal Mask'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'row index >= column index, via broadcasting'
tools: [NumPy]
---

## Statement

Build the causal (look-ahead) mask for a sequence of length `n`: a boolean $n\times n$ matrix whose entry $(i,j)$ is `True` when position $i$ may attend to position $j$, i.e. when $j\le i$.

Implement `solve(n)`.

**Returns.** Return a lower-triangular boolean NumPy array (diagonal included).

### Examples

**Example 1**

Input:

```python
solve(4)
```

Output:

```text
[[True, False, False, False], [True, True, False, False], [True, True, True, False], [True, True, True, True]]
```

**Example 2**

Input:

```python
solve(1)
```

Output:

```text
[[True]]
```

## Theory

### The simple version

A language model that predicts the next word must not see the words that come after it. Row $i$ of the mask lists which positions query $i$ is allowed to read: itself and everything before it, nothing after.

### The definition

$$M_{ij}=\begin{cases}\text{True}&j\le i\\\text{False}&j>i\end{cases}$$

## Explanation

Comparing a column of row indices with a row of column indices, `i >= j`, produces the whole matrix by broadcasting. In attention the `False` entries get their scores replaced by a very large negative number before the softmax, so they receive zero weight.
