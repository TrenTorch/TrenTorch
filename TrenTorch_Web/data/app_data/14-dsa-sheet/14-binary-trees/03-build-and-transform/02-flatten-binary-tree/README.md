---
name: sheet-flatten-binary-tree
title: 'Flatten a Binary Tree'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
theory: flattening-into-a-chain
---

## Statement

Rewire the tree **in place** so that it becomes a chain that only uses `right` pointers (`left` is `None` everywhere) and lists the nodes in **preorder**. Return the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 5, 3, 4, None, 6]` the answer is `[1, None, 2, None, 3, None, 4, None, 5, None, 6]`.

### Examples

**Example 1**

Input:

```python
flatten_tree(root)  # root = [1, 2, 5, 3, 4, None, 6]
```

Output:

```text
[1, None, 2, None, 3, None, 4, None, 5, None, 6]
```

**Example 2**

Input:

```python
flatten_tree(root)  # root = []
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

The inner loop finds the tail of the left subtree. Linking it to the old right child keeps all nodes reachable after the left subtree is moved.

### Complexity

- Time: O(n). The right-most walk of each left subtree is paid for once: after the splice those nodes are never walked as a tail again.
- Space: O(1). A couple of pointers; the tree is rewired in place.
