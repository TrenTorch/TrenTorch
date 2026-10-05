---
name: problem-109-relu-activation
title: 'ReLU Activation'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'max(x,0)'
tools: [NumPy]
---

## Statement

109 Relu Activation. Apply the rectified linear unit elementwise to x and return an array with the same shape: max(x, 0).

### Function signature

```python
solve(x)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(x=[-2, 0, 3])
```

**Output**

```python
[0, 0, 3]
```

**Example 2**

**Input**

```python
solve(x=[-1.5, 2])
```

**Output**

```python
[0.0, 2.0]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

ReLU keeps positive activations and clips negative activations to zero. It is piecewise linear and has an elementwise derivative away from its kink.

## Explanation

Take the elementwise maximum with zero. Input shape is preserved and zero maps to zero.
