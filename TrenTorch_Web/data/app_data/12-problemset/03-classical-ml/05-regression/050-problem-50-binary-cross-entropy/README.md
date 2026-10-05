---
name: problem-50-binary-cross-entropy
title: 'Binary Cross-Entropy'
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'logistic regression'
hint: 'use logaddexp-style stabilization'
tools: [NumPy]
---

## Statement

Implement `solve(logits, labels)`. Compute mean binary cross-entropy from real-valued logits and binary labels, using a stable logits-based formula.

### Examples

**Example 1**

Input:

```python
solve([0.0, 0.0], [0, 1])
```

Output:

```text
0.6931471805599453
```

**Example 2**

Input:

```python
solve([2.0, -2.0], [1, 0])
```

Output:

```text
0.1269280110429725
```

## Theory

For logit z and label y, the loss is max(z,0)−zy+log(1+e^(−|z|)); this softplus form avoids unstable probability clipping.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
