---
name: problem-168-additive-attention-score
title: 'Additive Attention Score'
tags: [problemset, sequence-models-attention, attention-mechanism]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'attention mechanism'
hint: 'tanh(query @ Wq + keys @ Wk) @ v'
tools: [NumPy]
---

## Statement

Compute additive (Bahdanau-style) attention scores between one query and several keys: $s_j=v^\top\tanh(W_qq+W_kk_j)$. Here `query` is a vector, `keys` has one key per row, `Wq` and `Wk` project them to a common hidden size and `v` maps the hidden vector to a scalar.

Implement `solve(query, keys, Wq, Wk, v)`.

**Returns.** Return a NumPy vector with one score per key. The scores are unnormalised; a softmax turns them into attention weights.

### Examples

**Example 1**

Input:

```python
solve([1.0, 0.0], [[0.0, 1.0], [1.0, 0.0]], [[1.0], [0.0]], [[0.0], [1.0]], [1.0])
```

Output:

```text
[0.964028, 0.761594]
```

**Example 2**

Input:

```python
solve([0.0], [[0.0]], [[1.0, 2.0]], [[1.0, 2.0]], [1.0, 1.0])
```

Output:

```text
[0.0]
```

## Theory

### The simple version

Before dot-product attention, sequence models scored each key against the query with a tiny neural network: project both into a shared space, add them, squash with $\tanh$, then reduce to a number with a learned vector. This lets query and key have different sizes, at the cost of more computation than a dot product.

### The formula

$$e_j=v^\top\tanh\big(W_qq+W_kk_j\big),\qquad \alpha_j=\operatorname{softmax}(e)_j$$

## Explanation

The query projection is computed once and added (by broadcasting) to every projected key. In the second example everything is zero, so the hidden vector is $\tanh(0)=0$ and the score is $0$.
