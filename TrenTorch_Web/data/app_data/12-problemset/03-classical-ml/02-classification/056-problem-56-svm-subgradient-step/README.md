---
name: problem-56-svm-subgradient-step
title: 'SVM Subgradient Step'
tags: [problemset, classical-ml, svm]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'svm'
hint: 'update violating examples with y*x'
tools: [NumPy]
---

## Statement

Implement `solve(X, y, w, lr, reg)`. Perform one linear-SVM subgradient update on weights w using learning rate lr and hinge coefficient reg. Examples with margin at least one contribute no hinge subgradient.

### Examples

**Example 1**

Input:

```python
solve([[1.0], [-1.0]], [1, -1], [0.0], 0.1, 1.0)
```

Output:

```text
[0.2]
```

**Example 2**

Input:

```python
solve([[1.0], [-1.0]], [1, -1], [2.0], 0.1, 1.0)
```

Output:

```text
[1.8]
```

## Theory

The weight gradient is the regularization gradient w minus reg times the sum yᵢxᵢ over examples with yᵢ(wᵀxᵢ)<1; subtract lr times this gradient once.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
