---
name: sheet-inorder-traversal
title: 'Inorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Beginner
theory: iterative-inorder
---

## Statement

Return the values of the tree in **inorder**: visit the left subtree, then the node itself, then the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[1, 3, 2]`.

### Examples

**Example 1**

Input:

```python
inorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[1, 3, 2]
```

**Example 2**

Input:

```python
inorder_traversal(root)  # root = []
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Explanation

`stack` holds the ancestors still waiting for their turn. When no more left child exists, the top of the stack is the next node in inorder.

### Complexity

- Time: O(n). Each node is pushed and popped once.
- Space: O(h). `h` is the height of the tree; the stack holds one path, so `O(n)` in the worst case (the result is output).
