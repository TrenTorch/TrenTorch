---
name: conv1d-valid-company-237
title: 'conv1d-valid — Intel case'
tags: [problemset, dl-core, cnn-basics, intel]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Intel'
hint: '[dot(x[i:i+m], k) for i in range(n - m + 1)]'
tools: [NumPy]
---

## Statement

Intel-inspired edge inference prototype is validating a small one-dimensional convolution before mapping it to an optimized kernel. You need to compute the valid convolution output for a single channel with stride 1. The operation is cross-correlation (the kernel is not flipped): out[i] = sum_j x[i+j]*k[j] over valid positions only.

Compute the 'valid' one-dimensional convolution of the signal `x` with the kernel `k`, without flipping the kernel (cross-correlation): $\text{out}[i]=\sum_jx[i+j]\,k[j]$ for every position where the kernel fits entirely inside the signal.

Implement `solve(x,k)`.

**Returns.** Return a float NumPy array of length `len(x) - len(k) + 1` (empty if the kernel is longer than the signal).

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3, 4], [1, 0, -1])
```

Output:

```text
[-2.0, -2.0]
```

**Example 2**

Input:

```python
solve([1.0, 1.0, 1.0], [2.0])
```

Output:

```text
[2.0, 2.0, 2.0]
```

## Theory

### The simple version

A convolution slides a small window of weights (the kernel) along a signal and, at each position, multiplies the overlapping numbers and adds them up. 'Valid' means the window never leaves the signal, so the output is a little shorter than the input. Edge hardware implements exactly this loop.

### The formula

$$y_i=\sum_{j=0}^{m-1}x_{i+j}\,k_j,\qquad i=0,\dots,n-m$$

## Explanation

In the first example the kernel $(1,0,-1)$ computes "left value minus right value", so every output is $-2$. Strictly speaking, mathematical convolution flips the kernel; machine-learning libraries (and this problem) do not, since the kernel is learned and the flip would only relabel its weights.
