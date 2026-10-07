---
name: sinusoidal-position-encoding-company-245
title: 'sinusoidal-position-encoding — Amazon case'
tags: [problemset, transformer-llm, positional-encoding-intro, amazon]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Amazon'
hint: 'angle = pos * exp(-ln(10000) * 2*(c//2) / d); sin on even columns, cos on odd'
tools: [NumPy]
---

## Statement

Amazon-inspired sequence model needs deterministic position information without adding learned position parameters. You need to construct the sinusoidal positional encoding for the requested sequence length and embedding dimension.

Build the sinusoidal positional encoding matrix of shape `(n, d)`: for position $p$ and column $c$, with $r_c=10000^{-2\lfloor c/2\rfloor/d}$, even columns hold $\sin(p\,r_c)$ and odd columns hold $\cos(p\,r_c)$.

Implement `solve(n,d)`.

**Returns.** Return a float NumPy array of shape `(n, d)`.

### Examples

**Example 1**

Input:

```python
solve(2, 4)
```

Output:

```text
[[0.0, 1.0, 0.0, 1.0], [0.841471, 0.540302, 0.01, 0.99995]]
```

**Example 2**

Input:

```python
solve(3, 3)
```

Output:

```text
[[0.0, 1.0, 0.0], [0.841471, 0.540302, 0.002154], [0.909297, -0.416147, 0.004309]]
```

## Theory

### The simple version

Attention has no built-in sense of order, so each token's embedding is combined with a position signal. Sinusoids of geometrically spaced wavelengths give each position a unique fingerprint without any trainable parameters, and the encoding works for any sequence length, even longer ones than seen in training.

### The formula

$$PE_{p,2i}=\sin\frac{p}{10000^{2i/d}},\qquad PE_{p,2i+1}=\cos\frac{p}{10000^{2i/d}}$$

## Explanation

Position $0$ is always $(0,1,0,1,\dots)$. Within a row, the first columns oscillate quickly with position and the last ones slowly, like the digits of a counter. An odd `d` leaves the last column as a sine.
