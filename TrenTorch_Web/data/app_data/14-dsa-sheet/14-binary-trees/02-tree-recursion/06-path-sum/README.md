---
name: sheet-path-sum
title: 'Root-to-Leaf Path Sum'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: root-to-leaf-path-sum
---

## Statement

Return `True` if the tree has a **root-to-leaf path** whose values add up to `target`. A leaf is a node with no children. An empty tree has no path.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]` and `target = 22` the answer is `True` (`5 + 4 + 11 + 2`).

### Examples

**Example 1**

Input:

```python
has_path_sum(root, 22)  # root = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1]
```

Output:

```text
True
```

**Example 2**

Input:

```python
has_path_sum(root, 5)  # root = [1, 2, 3]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-1000 <= val <= 1000`, `-10**9 <= target <= 10**9`

## Explanation

The leaf check `not root.left and not root.right` is where the path ends. For inner nodes the target shrinks by the node's value.

### Complexity

- Time: O(n). Every node is visited at most once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
