---
name: problem-25-one-hot-encode-categories
title: 'One-Hot Encode Categories'
tags: [problemset, data-stats-for-ds, data-cleaning]
difficulty: Beginner
kind: problemset
relatedModule: 'part-data-science|Data Processing'
topic: 'data cleaning'
hint: 'map each category to its column index first'
tools: [NumPy]
---

## Statement

Convert categorical labels into a binary indicator matrix with one column per category, in the order given by `categories`.

Implement `solve(values, categories)`.

**Returns.** Return an integer NumPy array of shape `(len(values), len(categories))`. A label that is not in `categories` raises `KeyError`.

### Examples

**Example 1**

Input:

```python
solve(['a', 'c', 'b'], ['a', 'b', 'c'])
```

Output:

```text
[[1, 0, 0], [0, 0, 1], [0, 1, 0]]
```

**Example 2**

Input:

```python
solve(['x', 'x'], ['x', 'y'])
```

Output:

```text
[[1, 0], [1, 0]]
```

## Theory

### The simple version

One-hot encoding turns a label into a row of zeros with a single 1 in the column that belongs to its category. Models can then use categories as numbers without implying an order.

### The formula

$$M_{r,c}=\begin{cases}1&\text{values}[r]=\text{categories}[c]\\0&\text{otherwise}\end{cases}$$

### Why it matters

- Models need numbers, and integer codes for categories would imply a false order (is `c` bigger than `a`?).
- One-hot vectors treat categories as equally distant from each other.

### How it works

1. Fix the list of categories (one column each).
2. For each sample, put a $1$ in the column of its category and $0$ elsewhere.

### Worked example

With categories $(a,b,c)$, the sample `a` becomes $(1,0,0)$, `c` becomes $(0,0,1)$ and `b` becomes $(0,1,0)$, giving [[1, 0, 0], [0, 0, 1], [0, 1, 0]].

## Explanation

A dictionary maps each category to its column once, so every lookup is constant time. Column order comes from `categories` exactly as given, which keeps the encoding deterministic and reproducible.
