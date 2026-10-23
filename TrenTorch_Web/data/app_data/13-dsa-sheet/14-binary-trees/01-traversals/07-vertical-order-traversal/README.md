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

**Example 2**

Input:

```python
vertical_order(root)  # root = [1, 2, 3, 4, 5, 6, 7]
```

Output:

```text
[[4], [2], [1, 5, 6], [3], [7]]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Compute for every node its **column** and its **row** (depth) while traversing (a BFS or DFS passing `(row, col)` down). Collect `(col, row, value)` for every node. Then **sort** these triples: sorting by column groups the columns left to right, then by row gives top to bottom, then by value breaks ties exactly as the question wants. Finally cut the sorted list into groups of equal column.

A dictionary `col -> list of (row, value)` also works: sort each group by `(row, value)` and output the columns in increasing order. `O(n log n)`.

## Explanation

The key `(col, row, value)` encodes the whole required order. `groupby`-style grouping then splits by column.
