---
name: problem-37-pooled-proportion-test-statistic
title: 'Pooled Proportion Test Statistic'
tags: [problemset, data-stats-for-ds, ab-testing]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'ab testing'
hint: 'pool successes before estimating the null proportion'
tools: [NumPy]
---

## Statement

Implement `solve(a, b)`. Compute the pooled two-proportion z-statistic for two binary samples under the null that their rates are equal.

### Examples

**Example 1**

Input:

```python
solve([1,0,1,1], [0,0,1,0])
```

Output:

```text
1.414213562373095
```

**Example 2**

Input:

```python
solve([1,0,1,0], [1,0,1,0])
```

Output:

```text
0.0
```

## Theory

The null uses the pooled rate; its standard error is √[p̂(1−p̂)(1/n₁+1/n₂)].

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
