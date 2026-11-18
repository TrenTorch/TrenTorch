---
name: sheet-binary-tree-paths
title: 'All Root-to-Leaf Paths'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
theory: listing-all-root-to-leaf-paths
---

## Statement

Return every **root-to-leaf path** as a string like `"1->2->5"`. List the paths from left to right: all the paths through the left subtree come before the paths through the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 3, None, 5]` the answer is `["1->2->5", "1->3"]`.

### Examples

**Example 1**

Input:

```python
root_to_leaf_paths(root)  # root = [1, 2, 3, None, 5]
```

Output:

```text
['1->2->5', '1->3']
```

**Example 2**

Input:

```python
root_to_leaf_paths(root)  # root = [1]
```

Output:

```text
['1']
```

### Constraints

- `0 <= number of nodes <= 20000`
- The tree is not deeper than 800 levels.
- `-100 <= val <= 100`

## Explanation

`go(node, path)` extends the path with the node's value. When a node has no children, `"->".join(path)` is a finished answer. Visiting left before right gives the left-to-right order.

### Complexity

- Time: O(n + S). `S` is the total length of the answer strings: each leaf writes out its whole path.
- Space: O(S). The output, plus `O(h)` for the current path.
