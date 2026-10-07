---
name: problem-81-gradient-boosting-update
title: 'Gradient Boosting Update'
tags: [problemset, classical-ml-trees-ensembles, gradient-boosting]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Classic ML'
topic: 'gradient boosting'
hint: 'pred + learning_rate * weak_pred'
tools: [NumPy]
---

## Statement

Apply one gradient-boosting update: add the weak learner's predictions, scaled by the learning rate (shrinkage), to the current ensemble predictions.

Implement `solve(pred,weak_pred,learning_rate)`.

**Returns.** Return a float NumPy array $\hat y+\eta\,h$.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [0.5, -1.0], 0.1)
```

Output:

```text
[1.05, 1.9]
```

**Example 2**

Input:

```python
solve([0.0, 0.0], [4.0, 8.0], 0.5)
```

Output:

```text
[2.0, 4.0]
```

## Theory

### The simple version

Each new tree is only trusted a little. Multiplying its output by a small learning rate $\eta$ (shrinkage) makes the ensemble improve in many small, safe steps instead of a few big, overfit ones.

### The formula

$$F_{m}(x)=F_{m-1}(x)+\eta\,h_m(x)$$

## Explanation

Smaller $\eta$ needs more trees but usually generalises better. With $\eta=1$ the weak learner is added at full strength.
