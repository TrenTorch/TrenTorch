---
name: problem-130-autoencoder-reconstruction
title: 'Autoencoder Reconstruction'
tags: [problemset, dl-core, autoencoders]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'autoencoders'
hint: 'mean of (x - recon) squared over all entries'
tools: [NumPy]
---

## Statement

Compute the reconstruction loss of an autoencoder: the mean squared difference over **all** entries between the input `x` and its reconstruction `recon` (same shape).

Implement `solve(x,recon)`.

**Returns.** Return a non-negative float.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [[1.0, 0.0], [0.0, 1.0]])
```

Output:

```text
5.5
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
```

Output:

```text
0.0
```

## Theory

### The simple version

An autoencoder is trained to squeeze its input through a narrow bottleneck and rebuild it. How well it rebuilds is measured by the reconstruction loss; if the loss is small, the bottleneck has kept the information that matters.

### The formula

$$L=\frac1{nd}\sum_{i,j}(x_{ij}-\hat x_{ij})^2$$

### Why it matters

- The reconstruction loss says how well the bottleneck kept the information.
- It is the training objective of an autoencoder.

### How it works

1. Subtract.
2. Square.
3. Average over all entries.

### Worked example

The differences are $(0,2)$ and $(3,3)$; squares $0,4,9,9$ sum to $22$ and $22/4=5.5$.

## Explanation

In the first example the squared errors are $0,4,9,9$, which average to $5.5$ over four entries. Averaging over all entries (not per row) means the loss does not depend on how the data are split into samples and features.
