---
name: problem-41-winsorize-values
title: 'Winsorize Values'
tags: [problemset, data-stats-for-ds, eda]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'EDA'
hint: 'compute quantiles and clip'
tools: [NumPy]
---

## Statement

Implement `solve(x, lower=0.05, upper=0.95)`. Winsorize a numeric vector by clipping values to the supplied lower and upper quantiles (defaults 0.05 and 0.95).

### Examples

**Example 1**

Input:

```python
solve([0.0, 1.0, 2.0, 3.0, 100.0], lower=0.2, upper=0.8)
```

Output:

```text
[0.8, 1.0, 2.0, 3.0, 22.400000000000016]
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0, 5.0], lower=0.0, upper=1.0)
```

Output:

```text
[1.0, 2.0, 3.0, 4.0, 5.0]
```

## Theory

Quantile thresholds are calculated from the data; observations below/above them are replaced by the respective boundary.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
