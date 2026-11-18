---
name: sheet-most-stones-removed
title: 'Most Stones Removed'
tags: [dsa-sheet, graphs, disjoint-sets]
difficulty: Advanced
theory: grouping-by-a-rule
---

## Statement

Stones are placed on the integer grid, `stones[i] = [x, y]`, at most one per cell. You may **remove a stone** if there is another stone **in the same row or the same column** that has not been removed. Return the **largest number of stones** you can remove.

For `[[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]]` the answer is `5`.

### Examples

**Example 1**

Input:

```python
remove_stones([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]])
```

Output:

```text
5
```

**Example 2**

Input:

```python
remove_stones([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]])
```

Output:

```text
3
```

### Constraints

- `0 <= len(stones) <= 100000`
- `0 <= x, y <= 10000`
- No two stones share a cell.

## Explanation

Every stone connects its row with its column; the groups of rows and columns are exactly the groups of connected stones.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                                                                                                                                                       |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parent = {}`                       | `parent = {}`                                                                                                                                                   |
| `ra, rb = find(x), find(y + 10001)` | `parent = {0: 0, 10001: 10001}, size = {0: 1, 10001: 1}, find = <function remove_stones.<locals>.find at 0x000002BDE6AF08B0>, x = 0, y = 0, ra = 0, rb = 10001` |
| `ra, rb = find(x), find(y + 10001)` | `parent = {0: 0, 10001: 0, 10002: 10002}, size = {0: 2, 10001: 1, 10002: 1}, y = 1, rb = 10002`                                                                 |
| `ra, rb = find(x), find(y + 10001)` | `parent = {0: 0, 10001: 0, 10002: 0, 1: 1}, size = {0: 3, 10001: 1, 10002: 1, 1: 1}, x = 1, y = 0, ra = 1, rb = 0`                                              |
| `for x, y in stones:`               | `parent = {0: 0, 10001: 0, 10002: 0, 1: 0}, size = {0: 4, 10001: 1, 10002: 1, 1: 1}, y = 2, ra = 0, rb = 1`                                                     |
| `for x, y in stones:`               | `parent = {0: 0, 10001: 0, 10002: 0, 1: 0, 10003: 0}, size = {0: 5, 10001: 1, 10002: 1, 1: 1, 10003: 1}, x = 2, y = 1, rb = 10003`                              |
| `size[ra] += size[rb]`              | `parent = {0: 0, 10001: 0, 10002: 0, 1: 0, 10003: 0, 2: 0}, size = {0: 6, 10001: 1, 10002: 1, 1: 1, 10003: 1, 2: 1}, rb = 2`                                    |
| `return`                            | `returned = 5`                                                                                                                                                  |

### Complexity

- Time: O(s * alpha(s)). Each stone joins its row and its column in a union-find (`s` stones); with union by size and path halving each operation is `O(alpha(n))`, which is below 5 for any input that fits in memory.
- Space: O(s). The parent and size tables over the used rows and columns.
