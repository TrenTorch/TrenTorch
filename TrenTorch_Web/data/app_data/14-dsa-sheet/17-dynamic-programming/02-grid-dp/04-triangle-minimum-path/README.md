---
name: sheet-triangle-minimum-path
title: 'Triangle Minimum Path'
tags: [dsa-sheet, dynamic-programming, grid-dp]
difficulty: Intermediate
theory: triangles-and-falling-paths
---

## Statement

`triangle` has `i + 1` numbers in row `i`. Start at the top and move down; from position `j` of a row you may go to position `j` or `j + 1` of the next row. Return the **smallest sum** of a path from the top to the bottom. An empty triangle gives `0`.

For `[[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]]` the answer is `11` (`2 + 3 + 5 + 1`).

### Examples

**Example 1**

Input:

```python
minimum_total([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]])
```

Output:

```text
11
```

**Example 2**

Input:

```python
minimum_total([[-10]])
```

Output:

```text
-10
```

### Constraints

- `0 <= rows <= 1000`
- `-10**4 <= value <= 10**4`

## Explanation

`best` starts as a copy of the last row. Each higher row replaces `best` with the cheapest total from each of its cells down to the bottom.

### Complexity

- Time: O(n^2). The triangle has about `n^2 / 2` cells, each computed once from the two below it.
- Space: O(n). One row of the table (`n` = number of rows).
