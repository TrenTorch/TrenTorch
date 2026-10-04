---
name: problem-60-f1-score
title: "F1 Score"
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: "part-classical-unsupervised|Metrics & Evaluation"
topic: "metrics"
hint: "return zero when both are zero"
tools: [NumPy]
---

# F1 Score

## Statement

Implement `solve(precision, recall)`. Compute the harmonic mean of precision and recall, returning 0.0 when both are zero.

## Theory

The F1 score is 2PR/(P+R), balancing precision and recall.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.

## Examples

**Example 1**

Input:
```python
solve(0.5, 0.5)
```

Output:
```text
0.5
```

**Example 2**

Input:
```python
solve(1.0, 0.0)
```

Output:
```text
0.0
```
