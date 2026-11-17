---
name: sheet-binary-tree-maximum-path-sum
title: 'Maximum Path Sum'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Mastery
theory: maximum-path-sum
---

## Statement

A **path** is a sequence of connected nodes where each pair of neighbours is a parent and its child; it may start and end at **any** nodes and does **not** have to pass through the root, but it uses each node at most once. Return the **largest sum of the values** along any non-empty path.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[-10, 9, 20, None, None, 15, 7]` the answer is `42` (`15 + 20 + 7`).

### Examples

**Example 1**

Input:

```python
max_path_sum(root)  # root = [-10, 9, 20, None, None, 15, 7]
```

Output:

```text
42
```

**Example 2**

Input:

```python
max_path_sum(root)  # root = [1, 2, 3]
```

Output:

```text
6
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-1000 <= val <= 1000`

## Explanation

`gain(node)` is the best sum of a path that starts at `node` and goes down. `best` records the best path that bends at each node, using both sides.

### Complexity

- Time: O(n). Every node is visited once and its best downward gain is computed from its children.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
