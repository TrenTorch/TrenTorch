---
name: problem-80-gradient-boosting-residual
title: 'Gradient Boosting Residual'
tags: [problemset, classical-ml-trees-ensembles, gradient-boosting]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'gradient boosting'
hint: 'target minus current prediction'
tools: [NumPy]
---

## Statement

Compute the residuals that a gradient-boosting step fits when the loss is squared error: the difference between the targets and the current ensemble predictions.

Implement `solve(y,pred)`.

**Returns.** Return a float NumPy array $y-\hat y$.

### Examples

**Example 1**

Input:

```python
solve([3.0, 5.0, 7.0], [2.5, 5.0, 8.0])
```

Output:

```text
[0.5, 0.0, -1.0]
```

**Example 2**

Input:

```python
solve([1.0, 1.0], [1.0, 1.0])
```

Output:

```text
[0.0, 0.0]
```

## Theory

### The simple version

Gradient boosting builds a model by repeatedly fitting a small tree to what the current model still gets wrong. For squared error the thing to fit is simply the residual, because the residual is exactly the negative gradient of the loss.

### The derivation

$$L=\tfrac12(y-\hat y)^2\;\Longrightarrow\;-\frac{\partial L}{\partial\hat y}=y-\hat y$$

## Explanation

The new weak learner is trained to predict these residuals; adding it to the ensemble (next problem) moves the predictions toward the targets. Perfect predictions leave zero residuals.
