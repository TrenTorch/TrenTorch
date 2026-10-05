---
name: problem-62-roc-curve-points
title: 'ROC Curve Points'
tags: [problemset, classical-ml, metrics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'sort scores descending and sweep thresholds'
tools: [NumPy]
---

## Statement

Implement `solve(y, scores)`. Return (FPR,TPR) pairs at every unique score threshold in descending order. If a class is absent, its corresponding rate is zero.

### Examples

**Example 1**

Input:

```python
solve([1,0,1,0], [0.9,0.8,0.4,0.1])
```

Output:

```text
[(0.0, 0.5), (0.5, 0.5), (0.5, 1.0), (1.0, 1.0)]
```

**Example 2**

Input:

```python
solve([1,0,1], [0.8,0.8,0.2])
```

Output:

```text
[(1.0, 0.5), (1.0, 1.0)]
```

## Theory

At threshold t, predict positive when score≥t; accumulate TP and FP, then normalize by the total positive and negative counts.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
