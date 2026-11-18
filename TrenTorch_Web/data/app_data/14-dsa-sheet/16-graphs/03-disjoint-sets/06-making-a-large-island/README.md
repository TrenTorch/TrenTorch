---
name: sheet-making-a-large-island
title: 'Making a Large Island'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Mastery
theory: sizes-live-at-the-leader
---

## Statement

`grid` holds `0` (water) and `1` (land). You may change **at most one `0` to `1`**. Return the **size of the largest island** (land cells connected up, down, left or right) you can get.

For `[[1, 0], [0, 1]]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
largest_island([[1, 0], [0, 1]])
```

Output:

```text
3
```

**Example 2**

Input:

```python
largest_island([[1, 1], [1, 1]])
```

Output:

```text
4
```

### Constraints

- `0 <= rows, cols <= 300`
- Every cell is `0` or `1`.

## Explanation

`label[r][c]` is the island id of a land cell and `size[id]` its size. The set of neighbour ids makes sure a single island is added only once.

### Complexity

- Time: O(r * c). One search labels every island and records its size; then each water cell looks at its 4 neighbours.
- Space: O(r * c). The label grid and the size table.
