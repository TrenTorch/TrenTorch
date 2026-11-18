---
name: sheet-unique-paths
title: 'Unique Paths'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Beginner
theory: counting-paths-in-a-grid
---

## Statement

A robot stands at the top-left cell of a `rows x cols` grid and moves only **right** or **down** to reach the bottom-right cell. Return the **number of different paths**. Return the answer modulo `10**9 + 7`.

For `rows = 3` and `cols = 7` the answer is `28`.

The starter code is a plain recursion. It is correct but too slow for big grids.

### Examples

**Example 1**

Input:

```python
unique_paths(3, 7)
```

Output:

```text
28
```

**Example 2**

Input:

```python
unique_paths(3, 2)
```

Output:

```text
3
```

### Constraints

- `1 <= rows, cols <= 1000`

## Explanation

Every path has exactly `rows - 1` down moves and `cols - 1` right moves in some order, so the number of paths is the number of ways to choose where the down moves go: `C(rows + cols - 2, rows - 1)`. `math.comb` computes that in `O(min(rows, cols))` multiplications, and the result is reduced modulo `10^9 + 7`. The grid table (`row[c] += row[c - 1]`) gives the same answer in `O(rows * cols)` and is the method to use once obstacles appear.

### Complexity

- Time: O(min(r, c)). Every path is a choice of which `r - 1` of the `r + c - 2` moves go down, which is the binomial coefficient `C(r + c - 2, r - 1)`.
- Space: O(1). A few big integers.
