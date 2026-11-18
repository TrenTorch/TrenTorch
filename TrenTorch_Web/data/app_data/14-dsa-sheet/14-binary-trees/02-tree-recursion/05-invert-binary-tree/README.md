---
name: sheet-invert-binary-tree
title: 'Invert a Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: inverting-a-tree
---

## Statement

**Invert** the tree: swap the left and right child of **every** node, and return the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[4, 2, 7, 1, 3, 6, 9]` the answer is `[4, 7, 2, 9, 6, 3, 1]`.

### Examples

**Example 1**

Input:

```python
invert_tree(root)  # root = [4, 2, 7, 1, 3, 6, 9]
```

Output:

```text
[4, 7, 2, 9, 6, 3, 1]
```

**Example 2**

Input:

```python
invert_tree(root)  # root = [2, 1, 3]
```

Output:

```text
[2, 3, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

The right-hand side is evaluated first, so both recursive calls see the original children before the assignment swaps them.

### Complexity

- Time: O(n). Every node swaps its two children once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
