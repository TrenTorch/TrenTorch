---
name: problem-131-encoder-bottleneck
title: 'Encoder Bottleneck'
tags: [problemset, dl-core, autoencoders]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'autoencoders'
hint: 'X @ W + b'
tools: [NumPy]
---

## Statement

Map each input row to a lower-dimensional code with a single affine transform: $Z=XW+b$, where `X` is $n\times d$, `W` is $d\times m$ with $m<d$ and `b` has length $m$.

Implement `solve(X, W, b)`.

**Returns.** Return an $n\times m$ NumPy array.

### Examples

**Example 1**

Input:

```python
solve([[1, 2, 3], [4, 5, 6]], [[1, 0], [0, 1], [1, 1]], [0, 1])
```

Output:

```text
[[4, 6], [10, 12]]
```

**Example 2**

Input:

```python
solve([[1, 1]], [[2], [3]], [1])
```

Output:

```text
[[6]]
```

## Theory

### The simple version

The encoder of an autoencoder squeezes the input into fewer numbers. The simplest encoder is a single linear layer; with that choice the autoencoder learns essentially the same subspace as PCA.

### The formula

$$Z=XW+\mathbf 1b^\top,\qquad W\in\mathbb R^{d\times m},\;m<d$$

### Why it matters

- An encoder squeezes the input into fewer numbers.
- A linear encoder learns the same subspace as PCA.

### How it works

1. $XW$.
2. Add the bias.

### Worked example

Row $(1,2,3)$ times the weights gives $(1+3,\,2+3)=(4,5)$, plus bias $(0,1)$ is $(4,6)$. Row $(4,5,6)$ gives $(10,11)+(0,1)=(10,12)$: [[4, 6], [10, 12]].

## Explanation

Each output coordinate is a weighted sum of all inputs plus a bias. In the second example the single row $(1,1)$ is mapped to $2+3+1=6$. A non-linear activation after this layer would turn it into a non-linear encoder.
