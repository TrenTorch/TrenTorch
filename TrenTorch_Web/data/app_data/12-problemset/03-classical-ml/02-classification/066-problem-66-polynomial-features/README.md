---
name: problem-66-polynomial-features
title: 'Polynomial Features'
tags: [problemset, classical-ml, feature-engineering]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'feature engineering'
hint: 'column_stack of x**1, x**2, ..., x**degree'
tools: [NumPy]
---

## Statement

Expand features into powers $1,\dots,d$. A length-$n$ vector `x` becomes an $n\times d$ matrix whose column $j$ is $x^{j}$. A 2-D input is expanded block by block: all columns to the power 1, then all columns to the power 2, and so on.

Implement `solve(x,degree)`.

**Returns.** Return a float NumPy array. For a vector of length $n$ the shape is $n\times\text{degree}$.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], 3)
```

Output:

```text
[[1.0, 1.0, 1.0], [2.0, 4.0, 8.0], [3.0, 9.0, 27.0]]
```

**Example 2**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], 2)
```

Output:

```text
[[1.0, 2.0, 1.0, 4.0], [3.0, 4.0, 9.0, 16.0]]
```

## Theory

### The simple version

A straight-line model cannot fit a curve, but a linear model on _extra columns_ $x,x^2,x^3,\dots$ can. This is polynomial regression: the model is still linear in its weights, only the features are non-linear in $x$.

### The mapping

$$x\;\longmapsto\;\big(x,\;x^2,\;\dots,\;x^d\big)$$

## Explanation

The powers are computed one at a time and stacked side by side. The constant column (the power $0$) is deliberately left out because the regression usually adds its own intercept. High degrees give huge values and unstable fits, so scale the input first.
