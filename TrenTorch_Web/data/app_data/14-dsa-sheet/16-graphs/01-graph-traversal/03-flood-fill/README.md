---
name: sheet-flood-fill
title: 'Flood Fill'
tags: [dsa-sheet, graphs, graph-traversal]
difficulty: Beginner
theory: flood-fill-and-counting-islands
---

## Statement

`image` is a grid of colours. Starting at the cell `(sr, sc)`, **recolour** it and every cell connected to it (up, down, left or right) that has the **same original colour** to `color`. Return the new image.

For `image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]`, `(sr, sc) = (1, 1)` and `color = 2` the answer is `[[2, 2, 2], [2, 2, 0], [2, 0, 1]]`.

### Examples

**Example 1**

Input:

```python
flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2)
```

Output:

```text
[[2, 2, 2], [2, 2, 0], [2, 0, 1]]
```

**Example 2**

Input:

```python
flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0)
```

Output:

```text
[[0, 0, 0], [0, 0, 0]]
```

### Constraints

- `1 <= rows, cols <= 300`
- `0 <= image[i][j], color < 65536`
- `(sr, sc)` is a cell of the image.

## Explanation

The early return handles `color == old`. Otherwise each recoloured cell no longer has the old colour, so it is never pushed again.

### Complexity

- Time: O(r * c). Every cell is pushed and popped at most once and each has 4 neighbours.
- Space: O(r * c). The stack can hold the whole region (the image is changed in place).
