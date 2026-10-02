---
name: numpy-basic-indexing
title: Basic Indexing (1D and Multi-Dimensional)
tags: [numpy-core]
difficulty: Beginner
---

## Statement

Implement functions that retrieve single elements from 1D and multi-dimensional arrays using integer indices.

## Theory

A 1D array is indexed like a Python list: an integer inside `[]` retrieves the element at that position, counting from `0`. Negative indices count from the end (`-1` is the last element).

```python
arr = np.array([10, 20, 30, 40])
arr[0]       # 10
arr[-1]      # 40
```

A 2D array uses `arr[i, j]` to retrieve row `i`, column `j` directly, in one step — preferred over chaining `arr[i][j]`, which is actually two separate operations (produce row `i` as its own array, then index into it).

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
arr[0, 0]     # 1
arr[1, 2]     # 6
```

A partial index — fewer indices than the array has dimensions — returns an entire sub-array along the remaining dimensions, not an error:

```python
arr[0]     # array([1, 2, 3]) — the entire first row
```

Negative indices work identically across every dimension: `arr[-1, -1]` is the last row, last column.

## Explanation

`get_element_1d` and `get_element_2d` are direct index expressions (`arr[index]`, `arr[row, col]`). `get_row` uses a partial index (`arr[row]`), which returns the whole row as a 1D array rather than raising an error.
