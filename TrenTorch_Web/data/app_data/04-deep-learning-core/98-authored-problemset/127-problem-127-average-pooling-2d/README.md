---
name: problem-127-average-pooling-2d
title: "Average Pooling 2D"
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "cnn basics"
hint: "take mean per window"
tools: [NumPy]
---

## Statement

Average pooling replaces each window with its arithmetic mean.

### Function signature

```python
def solve(X, k, s=1):
```

Arguments are passed directly to `solve`; there is no stdin/stdout parsing. The function returns its result without printing.

### Examples

**Example 1**

**Input**

```python
solve([[1, 3, 2], [4, 6, 5], [7, 8, 9]], 2, 1)
```

**Output**

```text
[[3.5, 4.0], [6.25, 7.0]]
```

**Example 2**

**Input**

```python
solve([[-1, -2], [-3, -4]], 2)
```

**Output**

```text
[[-2.5]]
```

## Theory

### Core idea

Use the same window positions and output shape as max pooling, but average all values in each window.

### Contract

Each output cell reduces exactly one `k`-by-`k` patch by its arithmetic mean.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
