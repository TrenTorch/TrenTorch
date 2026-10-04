---
name: problem-65-bias-variance-decomposition
title: "Bias-Variance Decomposition"
tags: [problemset, classical-ml, bias-variance]
difficulty: Intermediate
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "bias variance"
hint: "compare mean prediction with target and spread across models"
tools: [NumPy]
---

## Statement

65 Bias Variance Decomposition. Given predictions from multiple models for the same observations, return (squared_bias, variance). Squared bias is the mean squared difference between the model-mean prediction and y. Variance is the mean prediction variance across models, using population variance.

### Function signature

```python
solve(predictions, y)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(predictions=[[2, 4], [4, 6]], y=[3, 5])
```

**Output**

```python
(0.0, 1.0)
```

**Example 2**

**Input**

```python
solve(predictions=[[1, 3], [3, 5]], y=[2, 4])
```

**Output**

```python
(0.0, 1.0)
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

The ensemble mean estimates the expected prediction. Squared bias measures its mean squared error against the target; variance averages per-observation population variance across models.

## Explanation

Average along the model axis, then reduce squared residuals and population variances to scalars. Return these components in that order.
