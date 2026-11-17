---
name: sheet-maximum-depth
title: 'Maximum Depth'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: maximum-depth
---

## Statement

Return the **depth** (number of levels) of the tree: the number of nodes on the longest path from the root down to a leaf. An empty tree has depth `0`.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `3`.

### Examples

**Example 1**

Input:

```python
max_depth(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
3
```

**Example 2**

Input:

```python
max_depth(root)  # root = [1, None, 2]
```

Output:

```text
2
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

The base case `None` returns 0. Each node adds 1 to the better of its two subtrees.

### Complexity

- Time: O(n). Every node is visited once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
