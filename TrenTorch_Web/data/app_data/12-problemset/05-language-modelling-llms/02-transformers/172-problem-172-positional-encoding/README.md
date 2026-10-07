---
name: problem-172-positional-encoding
title: 'Positional Encoding'
tags: [problemset, sequence-models-attention, positional-encoding]
difficulty: Advanced
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'positional encoding'
hint: 'angle = pos / 10000**(2*(k//2)/dim); sin on even columns, cos on odd'
tools: [NumPy]
---

## Statement

Generate the sinusoidal positional encodings of the original Transformer for `n` positions and model dimension `dim`. Even columns hold $\sin(\text{pos}\cdot r_k)$ and odd columns hold $\cos(\text{pos}\cdot r_k)$, where $r_k=10000^{-2\lfloor k/2\rfloor/\text{dim}}$ for column $k$.

Implement `solve(n,dim)`.

**Returns.** Return a float array of shape `(n, dim)`.

### Examples

**Example 1**

Input:

```python
solve(3, 4)
```

Output:

```text
[[0.0, 1.0, 0.0, 1.0], [0.841471, 0.540302, 0.01, 0.99995], [0.909297, -0.416147, 0.019999, 0.9998]]
```

**Example 2**

Input:

```python
solve(1, 5)
```

Output:

```text
[[0.0, 1.0, 0.0, 1.0, 0.0]]
```

## Theory

### The simple version

Attention by itself ignores word order, so the model needs to be told each token's position. Sinusoidal encodings give every position a unique pattern of sines and cosines at geometrically spaced frequencies: fast-changing columns tell neighbouring positions apart, slow ones locate a position in the whole sequence.

### The formula

$$PE_{(\text{pos},2i)}=\sin\!\Big(\frac{\text{pos}}{10000^{2i/d}}\Big),\qquad PE_{(\text{pos},2i+1)}=\cos\!\Big(\frac{\text{pos}}{10000^{2i/d}}\Big)$$

## Explanation

Position $0$ is always $(0,1,0,1,\dots)$ since $\sin0=0$ and $\cos0=1$ (the single row in the second example). The encoding of position $p+k$ is a linear function of the encoding of $p$ for any fixed offset $k$, which makes relative positions easy to learn. An odd `dim` simply leaves the last column as a sine.
