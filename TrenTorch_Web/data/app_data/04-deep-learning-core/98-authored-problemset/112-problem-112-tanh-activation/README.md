---
name: problem-112-tanh-activation
title: "Tanh Activation"
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-core|Activation Functions"
topic: "activation functions"
hint: "use np.tanh"
tools: [NumPy]
---

## Statement

112 Tanh Activation. Apply the hyperbolic tangent elementwise to x, preserving its shape.

### Function signature

```python
solve(x)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(x=[-1, 0, 1])
```

**Output**

```python
[-0.761594156, 0.0, 0.761594156]
```

**Example 2**

**Input**

```python
solve(x=[0])
```

**Output**

```python
[0.0]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Tanh maps real inputs into (−1, 1), is odd-symmetric, and is centered at zero.

## Explanation

NumPy’s tanh computes the elementwise hyperbolic tangent and preserves the array shape.
