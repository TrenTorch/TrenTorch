---
name: problem-62-roc-curve-points
title: 'ROC Curve Points'
tags: [problemset, classical-ml, metrics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'for each unique score (descending), predict score >= threshold and compute (FP/N, TP/P)'
tools: [NumPy]
---

## Statement

List the ROC curve points obtained by using every distinct score as a decision threshold (predict positive when `score >= threshold`), going from the highest threshold to the lowest. `y` holds 0/1 labels.

Implement `solve(y, scores)`.

**Returns.** Return a list of `(fpr, tpr)` tuples, one per unique score in decreasing order of threshold. The curve's starting point $(0,0)$ is not included. If a class is absent its rate is `0.0`.

### Examples

**Example 1**

Input:

```python
solve([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8])
```

Output:

```text
[(0.0, 0.5), (0.5, 0.5), (0.5, 1.0), (1.0, 1.0)]
```

**Example 2**

Input:

```python
solve([0, 1], [0.5, 0.5])
```

Output:

```text
[(1.0, 1.0)]
```

## Theory

### The simple version

A classifier outputs scores, and you choose a threshold to turn them into yes/no. Lowering the threshold catches more true positives but also lets in more false positives. The ROC curve plots that trade-off: true-positive rate against false-positive rate for every possible threshold.

### The formulas

$$\text{TPR}=\frac{TP}{P},\qquad \text{FPR}=\frac{FP}{N}$$

where $P$ and $N$ are the numbers of real positives and negatives.

## Explanation

Only thresholds equal to an observed score can change the predictions, so those are the only ones needed. Tied scores move together: in the second example both samples share one score, so lowering the threshold to that value flips both at once and there is only one point, $(1,1)$.
