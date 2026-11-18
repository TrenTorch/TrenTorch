---
name: sheet-diameter-of-binary-tree
title: 'Diameter of a Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
theory: diameter-of-a-tree
---

## Statement

The **diameter** is the number of **edges** on the longest path between **any two nodes** of the tree. The path does not have to pass through the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 3, 4, 5]` the answer is `3` (the path `4 -> 2 -> 1 -> 3`).

### Examples

**Example 1**

Input:

```python
diameter(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
3
```

**Example 2**

Input:

```python
diameter(root)  # root = [1, 2]
```

Output:

```text
1
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

`height(node)` returns the number of nodes on the longest downward path. `best` is updated with `left + right` at every node; with heights counted in nodes, that sum is exactly the number of edges.

### Complexity

- Time: O(n). Every node is visited once and its height is computed from its children.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
