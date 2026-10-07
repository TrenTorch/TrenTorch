---
name: problem-183-post-norm-transformer-block
title: 'Post-Norm Transformer Block'
tags: [problemset, transformer-llm, layer-norm-and-residuals]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'layer norm and residuals'
hint: 'h = norm(x + attention(x)); return norm(h + ff(h))'
tools: [NumPy]
---

## Statement

Apply a **post-norm** Transformer block (the original design). With callables `norm`, `attention` and `ff`: first $h=\text{norm}\big(x+\text{attention}(x)\big)$, then return $\text{norm}\big(h+\text{ff}(h)\big)$.

Implement `solve(x, norm, attention, ff)`.

**Returns.** Return an array with the shape of `x`.

### Examples

**Example 1**

Input:

```python
solve(np.array([1.0, 2.0]), lambda v: v - v.mean(), lambda v: v * 2, lambda v: v + 1)
```

Output:

```text
[-3.0, 3.0]
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

In a post-norm block the normalisation comes _after_ each residual addition, so everything, including the residual path itself, is renormalised. This is the arrangement of the original Transformer paper. It can give slightly better final quality but is harder to train deep without careful warm-up, which is why pre-norm took over.

### The formulas

$$h=\operatorname{Norm}\big(x+\operatorname{Attn}(x)\big),\qquad y=\operatorname{Norm}\big(h+\operatorname{FF}(h)\big)$$

## Explanation

With the same centring "norm", attention and feed-forward as in the pre-norm example the output is centred (mean $0$), because the last operation is the normalisation, and it is $(-3,3)$ rather than the pre-norm result. In the second example the feed-forward branch adds nothing and the norm is the identity, so the output is $x+x=(2,2)$.
