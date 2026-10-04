---
name: problem-126-max-pooling-2d
title: "Max Pooling 2D"
tags: [problemset, dl-core, cnn-basics]
difficulty: Intermediate
kind: problemset
relatedModule: "part-dl-core|Neural Networks"
topic: "cnn basics"
hint: "take maximum per window"
tools: [NumPy]
---

## Statement

A pooling window takes the largest value in its square region.

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
[[6.0, 6.0], [8.0, 9.0]]
```

**Example 2**

**Input**

```python
solve([[-5, -2], [-3, -4]], 2)
```

**Output**

```text
[[-2.0]]
```

## Theory

### Core idea

Pool over every square window of side `k`, starting at stride `s`; the final result is a 2D array.

### Contract

Window reduction is local: the output at `(i, j)` is the maximum of `X[i*s:i*s+k, j*s:j*s+k]`.

## Explanation

In Example 1, the stated operation produces the displayed result directly from the supplied inputs. Example 2 changes the input case while keeping the same rule, so it illustrates that the function applies the contract rather than special-casing one example.
