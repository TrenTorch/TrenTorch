---
name: problem-40-group-aggregation
title: 'Group Aggregation'
tags: [problemset, data-stats-for-ds, data-wrangling]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data wrangling'
hint: 'build a dictionary of running sum and count'
tools: [NumPy]
---

## Statement

Implement `solve(keys, values)`. Return the arithmetic mean of numeric values for each categorical key.

### Examples

**Example 1**

Input:

```python
solve(["a", "a", "b"], [1.0, 2.0, 4.0])
```

Output:

```text
{'a': 1.5, 'b': 4.0}
```

**Example 2**

Input:

```python
solve(["north", "south", "north"], [10, 6, 14])
```

Output:

```text
{'north': 12.0, 'south': 6.0}
```

## Theory

Maintain a running sum and count per key, then divide each sum by its group count.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.
