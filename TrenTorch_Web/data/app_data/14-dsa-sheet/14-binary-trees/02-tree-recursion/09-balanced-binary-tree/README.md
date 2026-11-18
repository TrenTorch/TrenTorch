---
name: sheet-balanced-binary-tree
title: 'Balanced Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
theory: balanced-tree-check
---

## Statement

A tree is **height-balanced** if, for **every node**, the heights of its left and right subtrees differ by **at most 1**. Return `True` if the tree is balanced.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `True`; for `[1, 2, 2, 3, 3, None, None, 4, 4]` it is `False`.

### Examples

**Example 1**

Input:

```python
is_balanced(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_balanced(root)  # root = [1, 2, 2, 3, 3, None, None, 4, 4]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

`check(node)` returns the height, or `-1` if any node below is unbalanced. The first `-1` bubbles up unchanged.

### Complexity

- Time: O(n). Heights are computed bottom up and the search stops at the first unbalanced node.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
