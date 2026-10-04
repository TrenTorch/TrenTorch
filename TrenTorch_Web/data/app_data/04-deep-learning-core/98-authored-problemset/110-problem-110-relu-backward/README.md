---
name: problem-110-relu-backward
title: "ReLU Backward"
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: "part-dl-core|Activation Functions"
topic: "activation functions"
hint: "return 1 where x>0 else 0"
tools: [NumPy]
---

## Statement

110 Relu Backward. Return the elementwise derivative mask for ReLU: 1 where x is strictly positive and 0 where x is zero or negative. The result is the local derivative only; no upstream gradient is supplied.

### Function signature

```python
solve(x)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(x=[-1, 0, 2])
```

**Output**

```python
[0.0, 0.0, 1.0]
```

**Example 2**

**Input**

```python
solve(x=[0.5, -0.5])
```

**Output**

```python
[1.0, 0.0]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

ReLU is max(x, 0). Its derivative is one on the positive branch and zero on the nonpositive branch; this contract chooses derivative zero at x=0.

## Explanation

Compare each input to zero and convert the boolean mask to floating-point values.
