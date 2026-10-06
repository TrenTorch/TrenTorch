---
name: problem-64-stratified-k-fold
title: 'K-Fold Splits (Index-Based)'
tags: [problemset, classical-ml, cross-validation]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'cross validation'
hint: 'distribute shuffled class indices round-robin across folds'
tools: [NumPy]
---

## Statement

64 Stratified K Fold. Partition indices 0 through n−1 into k deterministic folds as evenly as possible. Return a list of (training_indices, validation_indices) pairs in fold order. The signature provides no class labels, so this is index-based K-fold splitting and does not stratify on labels.

### Function signature

```python
solve(n, k)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(n=5, k=3)
```

**Output**

```python
[([2, 3, 4], [0, 1]), ([0, 1, 4], [2, 3]), ([0, 1, 2, 3], [4])]
```

**Example 2**

**Input**

```python
solve(n=4, k=2)
```

**Output**

```python
[([2, 3], [0, 1]), ([0, 1], [2, 3])]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

K-fold validation partitions observation indices into disjoint validation groups. Each training group is the complement of its validation group. `array_split` keeps fold sizes balanced while preserving order.

## Explanation

Create indices, split into k consecutive groups, then concatenate all groups except the validation group for each training set. No labels are supplied or used.
