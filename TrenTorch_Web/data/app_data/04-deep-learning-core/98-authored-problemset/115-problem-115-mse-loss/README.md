---
name: problem-115-mse-loss
title: "MSE Loss"
tags: [problemset, dl-core, loss-functions]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-core|Loss Functions"
topic: "loss functions"
hint: "average squared residual"
tools: [NumPy]
---

## Statement

115 Mse Loss. Return mean squared error between target values y and predictions pred. Both inputs have the same shape. The result is a Python float.

### Function signature

```python
solve(y, pred)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(y=[1, 2, 3], pred=[1, 4, 2])
```

**Output**

```python
1.6666666667
```

**Example 2**

**Input**

```python
solve(y=[0, 0], pred=[1, -1])
```

**Output**

```python
1.0
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Mean squared error averages squared residuals, giving larger deviations proportionally greater weight.

## Explanation

Subtract predictions from targets, square each residual, and average all entries.
