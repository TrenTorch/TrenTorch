---
name: problem-25-one-hot-encode-categories
title: 'One-Hot Encode Categories'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'sort or preserve a supplied category order and set one column per label'
tools: [NumPy]
---

## Statement

Implement `solve(values, categories)`. Encode each value as a row in a binary matrix whose columns follow the supplied category order. Every input value must appear in categories.

### Examples

**Example 1**

Input:

```python
solve(["a", "b", "a"], ["a", "b", "c"])
```

Output:

```text
[[1, 0, 0], [0, 1, 0], [1, 0, 0]]
```

**Example 2**

Input:

```python
solve(["green", "red"], ["red", "green"])
```

Output:

```text
[[0, 1], [1, 0]]
```

## Theory

One-hot encoding places a single 1 in the column for each category and zeros elsewhere.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.
