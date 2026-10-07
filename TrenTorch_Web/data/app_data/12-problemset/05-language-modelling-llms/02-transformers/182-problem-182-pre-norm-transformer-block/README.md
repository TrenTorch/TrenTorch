---
name: problem-182-pre-norm-transformer-block
title: 'Pre-Norm Transformer Block'
tags: [problemset, transformer-llm, layer-norm-and-residuals]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'layer norm and residuals'
hint: 'x1 = x + attention(norm(x)); return x1 + ff(norm(x1))'
tools: [NumPy]
---

## Statement

Apply a **pre-norm** Transformer block. With callables `norm`, `attention` and `ff`: first $x_1=x+\text{attention}(\text{norm}(x))$, then return $x_1+\text{ff}(\text{norm}(x_1))$.

Implement `solve(x, norm, attention, ff)`.

**Returns.** Return an array with the shape of `x`. Pass `x` as a NumPy array.

### Examples

**Example 1**

Input:

```python
solve(np.array([1.0, 2.0]), lambda v: v - v.mean(), lambda v: v * 2, lambda v: v + 1)
```

Output:

```text
[-0.5, 5.5]
```

**Example 2**

Input:

```python
solve(np.array([1.0, 1.0]), lambda v: v, lambda v: v, lambda v: v * 0)
```

Output:

```text
[2.0, 2.0]
```

## Theory

### The simple version

Where the layer normalisation sits matters. In a pre-norm block it is applied to the _input_ of each sublayer and the residual path stays untouched, so gradients flow unobstructed from the output to the input. This makes deep models much easier to train, and most modern LLMs use it.

### The formulas

$$x_1=x+\operatorname{Attn}(\operatorname{Norm}(x)),\qquad y=x_1+\operatorname{FF}(\operatorname{Norm}(x_1))$$

## Explanation

The first example uses a centring "norm" (subtract the mean), attention $2v$ and feed-forward $v+1$ so the normalisation visibly matters: the residual path carries the raw input, so the result is **not** centred (its mean is $2.5$). Compare the post-norm block, whose output is always normalised. In the second example the feed-forward branch returns zeros and the attention branch returns the input, so the output is $x+x=(2,2)$.
