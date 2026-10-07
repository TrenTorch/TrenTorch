---
name: problem-181-transformer-feed-forward
title: 'Transformer Feed-Forward'
tags: [problemset, transformer-llm, transformer-architecture]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'transformer architecture'
hint: 'relu(x @ W1 + b1) @ W2 + b2'
tools: [NumPy]
---

## Statement

Compute the position-wise feed-forward network of a Transformer block: $\max(0,\,xW_1+b_1)\,W_2+b_2$, applied independently to every row of `x`.

Implement `solve(x,W1,b1,W2,b2)`.

**Returns.** Return an array with the same number of rows as `x`.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0]], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0])
```

Output:

```text
[[1.0, 2.0]]
```

**Example 2**

Input:

```python
solve([[1.0, -2.0]], [[1.0], [1.0]], [0.0], [[3.0]], [1.0])
```

Output:

```text
[[1.0]]
```

## Theory

### The simple version

After attention mixes information between tokens, each token is passed through a small two-layer network on its own: expand to a wider hidden size, apply a ReLU, project back. Most of a Transformer's parameters live in these feed-forward layers.

### The formula

$$\operatorname{FFN}(x)=\max(0,\,xW_1+b_1)\,W_2+b_2$$

## Explanation

The same weights are applied to every position independently (hence "position-wise"). In the second example the hidden unit receives $1-2=-1$, which the ReLU turns into $0$, so the output is just $b_2=1$.
