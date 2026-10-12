---
name: problem-180-transformer-residual-block
title: 'Transformer Residual Block'
tags: [problemset, transformer-llm, transformer-architecture]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'transformer architecture'
hint: 'x + sublayer(x)'
tools: [NumPy]
---

## Statement

Apply a residual connection around a sublayer: return $x+\text{sublayer}(x)$. `sublayer` is a function (for example attention or a feed-forward network) that returns an array of the same shape as `x`.

Implement `solve(x, sublayer)`.

**Returns.** Return a NumPy array with the shape of `x`.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], lambda v: v * 2)
```

Output:

```text
[3.0, 6.0]
```

**Example 2**

Input:

```python
solve([[1.0, -1.0]], lambda v: np.zeros_like(v))
```

Output:

```text
[[1.0, -1.0]]
```

## Theory

### The simple version

A residual connection adds a layer's input to its output. The layer therefore only has to learn a _correction_ to the identity, and gradients can flow straight through the addition. This is what makes very deep Transformers trainable.

### The formula

$$y=x+F(x)$$

### Why it matters

- Residuals let a layer learn a correction to the identity and let gradients flow through the sum.
- They make very deep stacks trainable.

### How it works

1. Apply the sublayer.
2. Add the input.

### Worked example

Input $(1,2)$ plus the sublayer output $(2,4)$ is [3.0, 6.0].

## Explanation

If the sublayer outputs zeros the block is the identity (second example), which is the starting point for training deep stacks. The shapes of `x` and the sublayer output must match for the addition.
