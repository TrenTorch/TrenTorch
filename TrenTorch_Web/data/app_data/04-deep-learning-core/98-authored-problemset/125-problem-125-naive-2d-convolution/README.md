---
name: problem-125-naive-2d-convolution
title: "Naive 2D Convolution"
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "cnn basics"
hint: "slide the kernel and sum elementwise products"
tools: [NumPy]
---

## Statement

125 Naive 2D Convolution. Compute a valid, stride-one, single-channel 2D convolution (cross-correlation) of matrix X by kernel K, with no padding. The kernel is not flipped. Return shape (H−kh+1, W−kw+1).

### Function signature

```python
solve(X, K)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(X=[[1, 2, 3], [4, 5, 6], [7, 8, 9]], K=[[1, 0], [0, -1]])
```

**Output**

```python
[[-4.0, -4.0], [-4.0, -4.0]]
```

**Example 2**

**Input**

```python
solve(X=[[1, 2], [3, 4]], K=[[1, 1], [1, 1]])
```

**Output**

```python
[[10.0]]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

A convolutional layer slides a kernel over local neighborhoods and combines each by an elementwise weighted sum. In common deep-learning libraries this is technically cross-correlation because the kernel is not reversed.

## Explanation

For every valid top-left position, multiply the input patch elementwise by K and sum. The window advances one cell in both spatial directions.
