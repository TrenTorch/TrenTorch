---
name: problem-164-scaled-dot-product-attention
title: 'Scaled Dot-Product Attention'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'scores = Q@K.T/sqrt(d); mask with -1e9; softmax over the last axis; times V'
tools: [NumPy]
---

## Statement

Compute scaled dot-product attention $\operatorname{softmax}\!\big(QK^\top/\sqrt{d}\big)V$ with an optional boolean `mask` (same shape as the score matrix): positions where the mask is `False` are blocked, so they get (almost) zero attention weight.

Implement `solve(Q,K,V,mask=None)`.

**Returns.** Return an array with one output row per query row. Rows of `Q` are queries (length $d$), rows of `K` are keys, rows of `V` are values.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 2.0], [3.0, 4.0]], None)
```

Output:

```text
[[1.660477, 2.660477]]
```

**Example 2**

Input:

```python
solve([[1.0, 0.0]], [[1.0, 0.0], [0.0, 1.0]], [[1.0, 2.0], [3.0, 4.0]], [[True, False]])
```

Output:

```text
[[1.0, 2.0]]
```

## Theory

### The simple version

Attention lets each query look at all the values and take a weighted average, giving more weight to those whose keys match the query. Matching is measured by a dot product, divided by $\sqrt d$ so the scores do not grow with the dimension and push the softmax into a region with tiny gradients.

### The formula

$$\operatorname{Attention}(Q,K,V)=\operatorname{softmax}\!\Big(\frac{QK^\top}{\sqrt d}\Big)V$$

### Why it matters

- Attention lets each position gather information from the others, weighted by relevance.
- Dividing by $\sqrt d$ keeps the softmax from saturating.

### How it works

1. Scores $QK^\top/\sqrt d$.
2. Mask blocked positions.
3. Softmax each row, multiply by $V$.

### Worked example

The query $(1,0)$ scores $1/\sqrt2=0.707$ against the first key and $0$ against the second. The softmax gives weights $0.670$ and $0.330$, so the output is $0.670(1,2)+0.330(3,4)=[[1.660477, 2.660477]]$.

## Explanation

Blocked positions have their score replaced by a very large negative number before the softmax, so their weight is essentially $0$ (second example: only the first key is allowed, so the output equals the first value row). The row maximum is subtracted before exponentiating for stability.
