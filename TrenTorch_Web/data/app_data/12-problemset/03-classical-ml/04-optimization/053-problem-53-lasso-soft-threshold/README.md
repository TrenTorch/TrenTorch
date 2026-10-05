---
name: problem-53-lasso-soft-threshold
title: 'Lasso Soft Threshold'
tags: [problemset, classical-ml, regularization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'separate the smooth gradient from the L1 penalty'
tools: [NumPy]
---

## Statement

Implement `solve(z, lam)`. Apply scalar soft-thresholding with nonnegative threshold lambda.

### Examples

**Example 1**

Input:

```python
solve(3.0, 1.0)
```

Output:

```text
2.0
```

**Example 2**

Input:

```python
solve(-0.5, 1.0)
```

Output:

```text
-0.0
```

## Theory

Soft thresholding shrinks magnitude by lambda and sets values with magnitude at most lambda to zero.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
