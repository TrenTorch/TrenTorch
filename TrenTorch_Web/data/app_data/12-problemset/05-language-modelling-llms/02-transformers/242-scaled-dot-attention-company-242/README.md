---
name: scaled-dot-attention-company-242
title: 'scaled-dot-attention — Twilio case'
tags: [problemset, transformer-llm, multi-head-attention, twilio]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Twilio'
hint: 'scores = Q@K.T/sqrt(d); set j>i to -inf; softmax over each row; times V'
tools: [NumPy]
---

## Statement

Twilio-inspired messaging model combines query, key, and value representations to select relevant context. You need to compute causal scaled dot-product attention: each position may attend only to itself and earlier positions, and the scores are scaled by the square root of the key dimension.

Compute **causal** scaled dot-product attention: scores $S=QK^\top/\sqrt d$, set every score above the diagonal (future positions) to $-\infty$, take a row-wise softmax and return the weights times `V`. Row $i$ therefore only attends to positions $0,\dots,i$.

Implement `solve(Q,K,V)`.

**Returns.** Return an array with one output row per query row. `Q`, `K` and `V` have the same number of rows.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 2.0], [3.0, 4.0]])
```

Output:

```text
[[1.0, 2.0], [2.339523, 3.339523]]
```

**Example 2**

Input:

```python
solve([[1.0]], [[2.0]], [[5.0]])
```

Output:

```text
[[5.0]]
```

## Theory

### The simple version

Attention lets each position gather information from others by comparing its query with their keys. Dividing by $\sqrt d$ stops the dot products from growing with the dimension, which would push the softmax into a nearly one-hot, low-gradient regime. The causal mask forbids looking ahead, as required when predicting the next token.

### The formula

$$\operatorname{Attn}(Q,K,V)=\operatorname{softmax}\!\Big(\frac{QK^\top}{\sqrt d}+M\Big)V,\qquad M_{ij}=\begin{cases}0&j\le i\\-\infty&j>i\end{cases}$$

## Explanation

The first output row can only see the first value row, so it equals it exactly. A single position (second example) attends only to itself and returns its own value. The row maximum is subtracted before exponentiating for stability.
