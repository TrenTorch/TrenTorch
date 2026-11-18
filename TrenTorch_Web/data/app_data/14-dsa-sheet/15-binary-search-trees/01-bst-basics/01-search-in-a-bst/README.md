---
name: sheet-search-in-a-bst
title: 'Search in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
theory: searching-by-comparing
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **subtree** whose root has the value `val` (the node with all its descendants), or an empty tree if there is no such node.

For `[4, 2, 7, 1, 3]` and `val = 2` the answer is `[2, 1, 3]`.

### Examples

**Example 1**

Input:

```python
search_bst(root, 2)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[2, 1, 3]
```

**Example 2**

Input:

```python
search_bst(root, 5)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.

## Explanation

Each step discards one whole subtree. The loop ends at the matching node, or at `None`.

### Complexity

- Time: O(h). Each step discards one subtree.
- Space: O(1). One pointer; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
