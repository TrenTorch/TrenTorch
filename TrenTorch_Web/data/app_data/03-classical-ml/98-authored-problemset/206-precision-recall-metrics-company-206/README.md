---
name: precision-recall-metrics-company-206
title: "precision-recall-metrics — Amazon case"
tags: [problemset, classical-ml, metrics-and-evaluation, amazon]
difficulty: Beginner
kind: problemset
relatedModule: "part-classical-linear|Classification"
topic: "Classification"
caseCompany: "Amazon"
hint: "Start from the mathematical definition and identify the one intermediate quantity that can be reused instead of recomputed."
tools: [NumPy]
---

## Statement

For binary 0/1 labels return (precision, recall); zero denominator for either metric yields 0.0.

Signature: `def solve(y_true, y_pred)`. Arguments are passed directly; return the stated value without printing.

### Example 1

```python
solve([1, 0, 1, 1], [1, 1, 0, 1])
```

Returns:

```python
[0.6666666666666666, 0.6666666666666666]
```

### Example 2

```python
solve([0, 0], [0, 0])
```

Returns:

```python
[0.0, 0.0]
```

## Theory

Precision=TP/(TP+FP), recall=TP/(TP+FN), with zero-denominator convention 0.

## Explanation

For binary 0/1 labels return (precision, recall); zero denominator for either metric yields 0.0. The examples show concrete inputs and expected returned values.
