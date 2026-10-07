---
name: problem-40-group-aggregation
title: 'Group Aggregation'
tags: [problemset, data-stats-for-ds, data-wrangling]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data wrangling'
hint: 'keep a running (sum, count) per key, then divide'
tools: [NumPy]
---

## Statement

Compute the mean of `values` for each distinct key in `keys` (a group-by-mean) without using pandas. `keys[i]` is the group of `values[i]`.

Implement `solve(keys, values)`.

**Returns.** Return a dict mapping each key to the mean of its values. Keys appear in order of first occurrence.

### Examples

**Example 1**

Input:

```python
solve(['a', 'a', 'b'], [1.0, 2.0, 4.0])
```

Output:

```text
{'a': 1.5, 'b': 4.0}
```

**Example 2**

Input:

```python
solve(['x', 'y', 'x', 'y', 'x'], [10.0, 1.0, 20.0, 3.0, 30.0])
```

Output:

```text
{'x': 20.0, 'y': 2.0}
```

## Theory

### The simple version

A group-by-mean walks through the data once, keeping for each key a running sum and a running count. At the end, sum divided by count is the mean of that group.

### The formula

$$\mu_k=\frac{1}{|G_k|}\sum_{i\in G_k} v_i,\qquad G_k=\{i: \text{keys}_i=k\}$$

## Explanation

One pass with a dictionary of `(sum, count)` pairs is linear in the data size and needs no sorting. Storing the sum and count rather than the values keeps memory proportional to the number of groups.
