---
name: problem-55-linear-svm-hinge-loss
title: 'Linear SVM Hinge Loss'
tags: [problemset, classical-ml, svm]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'svm'
hint: 'use max(0,1-y*s)'
tools: [NumPy]
---

## Statement

Implement `solve(y, scores)`. Compute the mean hinge loss for binary labels y∈{−1,+1} and corresponding prediction scores.

### Examples

**Example 1**

Input:

```python
solve([1, -1], [2.0, -0.5])
```

Output:

```text
0.25
```

**Example 2**

Input:

```python
solve([1, -1], [0.0, 0.0])
```

Output:

```text
1.0
```

## Theory

For each example, hinge loss is max(0,1−y·score); correctly classified points beyond the margin incur no loss.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
