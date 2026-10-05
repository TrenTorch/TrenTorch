---
name: problem-114-cross-entropy-from-logits
title: 'Cross-Entropy from Logits'
tags: [problemset, dl-core, loss-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Loss Functions'
topic: 'loss functions'
hint: 'use log-sum-exp and subtract the target logit'
tools: [NumPy]
---

## Statement

114 Cross Entropy From Logits. Return categorical cross-entropy from a one-dimensional logits vector and an integer target class index. Compute log(sum(exp(logits)))−logits[target] using a numerically stable log-sum-exp calculation.

### Function signature

```python
solve(logits, target)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(logits=[1, 2, 3], target=2)
```

**Output**

```python
0.4076059644
```

**Example 2**

**Input**

```python
solve(logits=[0, 0], target=0)
```

**Output**

```python
0.6931471806
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

For a categorical target, cross-entropy is the negative log probability assigned to the correct class. In logit form it is log-sum-exp of all logits minus the target logit.

## Explanation

Subtract the largest logit before exponentiation, then restore it in log-sum-exp. Subtract the target logit to obtain the scalar loss without explicitly forming probabilities.
