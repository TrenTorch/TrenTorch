---
name: problem-124-convolution-output-shape
title: 'Convolution Output Shape'
tags: [problemset, dl-core, cnn-basics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'cnn basics'
hint: 'apply floor((W+2P-K)/S)+1'
tools: [NumPy]
---

## Statement

124 Convolution Output Shape. Compute the output length of a convolution for input width W, kernel width K, symmetric padding P, and stride S using floor((W+2P−K)/S)+1.

### Function signature

```python
solve(W, K, P, S)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(W=7, K=3, P=1, S=2)
```

**Output**

```python
4
```

**Example 2**

**Input**

```python
solve(W=5, K=3, P=0, S=1)
```

**Output**

```python
3
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Convolution output dimensions count valid kernel positions after padding and stepping by the stride.

## Explanation

Add padding on both sides, subtract kernel width, divide by stride with floor rounding, and add the first position.
