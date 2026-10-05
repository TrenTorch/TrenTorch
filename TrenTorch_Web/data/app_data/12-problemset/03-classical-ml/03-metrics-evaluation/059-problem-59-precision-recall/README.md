---
name: problem-59-precision-recall
title: 'Precision Recall'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'count TP, FP, and FN explicitly'
tools: [NumPy]
---

## Statement

Implement `solve(y, pred)`. Compute binary precision and recall from true labels and hard predictions, returning zero for either metric when its denominator is zero.

### Examples

**Example 1**

Input:

```python
solve([1, 0, 1, 0], [1, 1, 0, 0])
```

Output:

```text
(0.5, 0.5)
```

**Example 2**

Input:

```python
solve([1, 1, 0], [1, 1, 1])
```

Output:

```text
(0.6666666666666666, 1.0)
```

## Theory

Precision is TP/(TP+FP), while recall is TP/(TP+FN).

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
