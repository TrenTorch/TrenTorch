---
name: problem-125-naive-2d-convolution
title: 'Naive 2D Convolution'
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: 'for each position sum(X[i:i+kh, j:j+kw] * K)'
tools: [NumPy]
---

## Statement

Compute the single-channel **valid** 2-D convolution of an image `X` with a kernel `K`, as deep-learning libraries do: slide the kernel over the image without flipping it (technically cross-correlation) and sum the element-wise products at each position. No padding, stride 1.

Implement `solve(X,K)`.

**Returns.** Return a float array of shape `(H - kh + 1, W - kw + 1)`.

### Examples

**Example 1**

Input:

```python
solve([[1, 2], [3, 4]], [[1, 0], [0, 1]])
```

Output:

```text
[[5.0]]
```

**Example 2**

Input:

```python
solve([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [[1, 0], [0, -1]])
```

Output:

```text
[[-4.0, -4.0], [-4.0, -4.0]]
```

## Theory

### The simple version

A convolutional layer detects local patterns. The small kernel is laid over every position of the image; at each position the overlapping numbers are multiplied pairwise and summed, producing one number of the output "feature map". The same kernel is reused everywhere, which is what makes convolutions so parameter-efficient.

### The formula

$$Y_{ij}=\sum_{u=0}^{k_h-1}\sum_{v=0}^{k_w-1}X_{i+u,\,j+v}\,K_{uv}$$

### Why it matters

- Convolution detects local patterns with a small shared kernel.
- It needs far fewer parameters than a dense layer.

### How it works

1. Slide the kernel over the image.
2. At each position multiply element-wise and sum.

### Worked example

The $2\times2$ image has one position. Multiplying with the kernel $\begin{pmatrix}1&0\\0&1\end{pmatrix}$ keeps $1$ and $4$, so the output is $1+4=[[5.0]]$.

## Explanation

'Valid' means the kernel must lie entirely inside the image, so the output is smaller than the input. Mathematical convolution flips the kernel; deep-learning layers do not, and because the kernel is learned, the distinction does not matter in practice. In the first example the only window gives $1\cdot1+4\cdot1=5$.
