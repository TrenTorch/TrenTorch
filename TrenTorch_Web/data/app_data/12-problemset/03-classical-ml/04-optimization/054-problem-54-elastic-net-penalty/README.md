---
name: problem-54-elastic-net-penalty
title: 'Elastic-Net Penalty'
tags: [problemset, classical-ml, regularization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Optimization'
topic: 'regularization'
hint: 'combine L1 and L2 terms'
tools: [NumPy]
---

## Statement

Implement `solve(w, l1, l2)`. Compute the elastic-net penalty l1*||w||₁ + (l2/2)*||w||₂².

### Examples

**Example 1**

Input:

```python
solve([1.0, -2.0], 0.5, 0.2)
```

Output:

```text
2.0
```

**Example 2**

Input:

```python
solve([0.0, 0.0], 1.0, 1.0)
```

Output:

```text
0.0
```

## Theory

The L1 term encourages sparsity; the squared L2 term smoothly penalizes large coefficients.

## Explanation

Use the supplied arrays and scalar parameters to calculate the described statistic or prediction. The function returns the numeric result or structured indices directly.
