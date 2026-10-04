---
name: problem-49-logistic-sigmoid
title: "Logistic Sigmoid"
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: "part-classical-linear|Regression"
topic: "logistic regression"
hint: "use separate positive and negative branches"
tools: [NumPy]
---

# Logistic Sigmoid

## Statement

Implement `solve(x)`. Compute sigmoid probabilities for arbitrary real logits using a numerically stable expression.

## Theory

The logistic sigmoid is 1/(1+e^(−x)); splitting positive and negative inputs avoids overflow in exponentiation.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve([0.0])
```

Output:
```text
[0.5]
```

**Example 2**

Input:
```python
solve([2.0, -2.0])
```

Output:
```text
[0.8807970779778823, 0.11920292202211755]
```
