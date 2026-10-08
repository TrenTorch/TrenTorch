---
name: problem-165-masked-attention
title: 'Masked Attention'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'same as attention; use np.where(mask, scores, -1e9) before the softmax'
tools: [NumPy]
---

## Statement

Compute scaled dot-product attention with a mask that stops queries from attending to future positions. `mask[i][j]` is `True` when query $i$ may attend to key $j$; for causal (autoregressive) attention it is lower triangular. The output is $\operatorname{softmax}(QK^\top/\sqrt d + \text{mask})V$.

Implement `solve(Q,K,V,mask=None)`.

**Returns.** Return an array with one output row per query row.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 2.0], [3.0, 4.0]], [[True, False], [True, True]])
```

Output:

```text
[[1.0, 2.0], [2.339523, 3.339523]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[[1.660477, 2.660477], [2.339523, 3.339523]]
```

## Theory

### The simple version

A language model that predicts the next word must not be allowed to peek at the words that come after. A causal mask hides every future position: position $i$ may only attend to positions $\le i$. Without it, training would be trivial (the answer is visible) and generation would fail.

### The mask

$$M_{ij}=\begin{cases}0&j\le i\\-\infty&j>i\end{cases}$$ added to the scores before the softmax.

### Why it matters

- A language model must not see future tokens while predicting.
- The mask hides them.

### How it works

1. Scores $QK^\top/\sqrt d$.
2. Set masked positions to a very negative number.
3. Softmax and multiply by $V$.

### Worked example

Query 0 may only see key 0, so its output is the first value row $(1,2)$. Query 1 sees both keys with weights $0.330$ and $0.670$ and gets $(2.34,3.34)$: [[1.0, 2.0], [2.339523, 3.339523]].

## Explanation

In the first example the first query can only see key 0, so its output is the first value row exactly, while the second query sees both keys. Without a mask (second example) the first query would also attend to the future key. The mask is built outside this function (see the causal-mask problem).
