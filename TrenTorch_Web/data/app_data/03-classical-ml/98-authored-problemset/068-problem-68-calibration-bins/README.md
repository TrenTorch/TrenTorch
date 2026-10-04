---
name: problem-68-calibration-bins
title: "Calibration Bins"
tags: [problemset, classical-ml, model-evaluation]
difficulty: Intermediate
kind: problemset
relatedModule: "part-classical-unsupervised|Metrics & Evaluation"
topic: "model evaluation"
hint: "bucket probabilities and compare mean confidence with event rate"
tools: [NumPy]
---

## Statement

68 Calibration Bins. Partition binary labels y and predicted probabilities p into equal-width bins over [0, 1]. For each nonempty bin, in increasing order, return (mean_probability, fraction_positive, count). Bins are left-closed/right-open except the final bin, which includes probability 1. Empty bins are omitted.

### Function signature

```python
solve(y, p, bins=10)
```

### Examples
### Examples

**Example 1**

**Input**

```python
solve(y=[0, 1, 1, 0], p=[0.1, 0.2, 0.8, 0.9], bins=2)
```

**Output**

```python
[(0.15, 0.5, 2), (0.85, 0.5, 2)]
```

**Example 2**

**Input**

```python
solve(y=[1], p=[1.0], bins=2)
```

**Output**

```python
[(1.0, 1.0, 1)]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

A reliability diagram compares confidence to empirical event frequency. Equal-width probability buckets summarize those quantities without changing the predictions.

## Explanation

Create uniform edges between zero and one; for each occupied interval, calculate mean confidence, mean binary outcome, and count.
