---
name: sheet-vertical-order-traversal
title: 'Vertical Order Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Advanced
---

## Statement

Give each node a **column**: the root is column `0`, a left child is one column to the **left** (column − 1) and a right child one column to the **right** (column + 1). Return the values grouped by column, from the leftmost column to the rightmost. Inside a column, go from **top to bottom**; nodes in the same row and column are ordered by **value** (smaller first).

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[9], [3, 15], [20], [7]]`.

### Examples

**Example 1**

Input:

```python
vertical_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[9], [3, 15], [20], [7]]
```

**Explanation:** The columns are: 9 at -1, then 3 and 15 together at 0 (15 is a left child of 20, so it is back under the root), then 20 at 1 and 7 at 2. Read from left to right they give [[9], [3, 15], [20], [7]].

**Example 2**

Input:

```python
vertical_order(root)  # root = [1, 2, 3, 4, 5, 6, 7]
```

Output:

```text
[[4], [2], [1, 5, 6], [3], [7]]
```

**Explanation:** In the full tree of 7 nodes, column 0 holds 1 first (row 0), then 5 and 6 (both in row 2), ordered by value. The other columns are 4 at -2, 2 at -1, 3 at 1 and 7 at 2.

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Compute for every node its **column** and its **row** (depth) while traversing (a BFS or DFS passing `(row, col)` down). Collect `(col, row, value)` for every node. Then **sort** these triples: sorting by column groups the columns left to right, then by row gives top to bottom, then by value breaks ties exactly as the question wants. Finally cut the sorted list into groups of equal column.

A dictionary `col -> list of (row, value)` also works: sort each group by `(row, value)` and output the columns in increasing order. `O(n log n)`.

## Explanation

The key `(col, row, value)` encodes the whole required order. `groupby`-style grouping then splits by column.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                       | Variables                                                                                                  |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `columns = {}`                                        | `columns = {}`                                                                                             |
| `node, row, col = queue.popleft()`                    | `queue = deque([]), node = <07-vertical-order-traversal_solution.TreeNode object at ..., row = 0, col = 0` |
| `queue.append((node.left, row + 1, col - 1))`         | `columns = {0: [(0, 3)]}, queue = deque([(<07-vertical-order-traversal_solution.TreeNode ob...`            |
| `columns.setdefault(col, []).append((row, node.val))` | `columns = {0: [(0, 3)], -1: [(1, 9)]}, row = 1, col = -1`                                                 |
| `columns.setdefault(col, []).append((row, node.val))` | `columns = {0: [(0, 3)], -1: [(1, 9)], 1: [(1, 20)]}, queue = deque([]), col = 1`                          |
| `node, row, col = queue.popleft()`                    | `queue = deque([(<07-vertical-order-traversal_solution.TreeNode ob..., row = 2, col = 0`                   |
| `node, row, col = queue.popleft()`                    | `columns = {0: [(0, 3), (2, 15)], -1: [(1, 9)], 1: [(1, 20)]}, queue = deque([]), col = 2`                 |
| `return`                                              | `returned = [[9], [3, 15], [20], [7]]`                                                                     |

### Complexity

- Time: O(n log n) where n is number of nodes.
- Extra space: O(n) for columns and queue.
- The brute force takes O(n log n) where n is number of nodes.
