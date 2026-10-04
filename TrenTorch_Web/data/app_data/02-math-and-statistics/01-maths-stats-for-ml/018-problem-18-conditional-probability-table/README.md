---
name: problem-18-conditional-probability-table
title: "Conditional Probability Table"
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Intermediate
kind: problemset
relatedModule: "part-math|Probability"
topic: "probability"
hint: "divide joint count by B count"
tools: [NumPy]
---

# Conditional Probability Table

## Statement

Implement `solve(A, B)`. Estimate P(A|B) from paired Boolean observations. Return 0.0 when the sample contains no B observations.

## Theory

Conditional probability is the fraction of observations satisfying both A and B among all observations satisfying B.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([True, True, False, False], [True, False, True, False])
```

Output:
```text
0.5
```

**Example 2**

Input:
```python
solve([True, False, True], [True, True, False])
```

Output:
```text
0.5
```
