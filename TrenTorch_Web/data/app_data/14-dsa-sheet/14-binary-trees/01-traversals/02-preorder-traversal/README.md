---
name: sheet-preorder-traversal
title: 'Preorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Beginner
theory: iterative-preorder
---

## Statement

Return the values of the tree in **preorder**: visit the node itself, then the left subtree, then the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[1, 2, 3]`.

### Examples

**Example 1**

Input:

```python
preorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[1, 2, 3]
```

**Example 2**

Input:

```python
preorder_traversal(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
[1, 2, 4, 5, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Explanation

The stack always has the next node on top. Because a stack is last in, first out, pushing right then left makes left come out first.

### Complexity

- Time: O(n). Each node is pushed and popped once.
- Space: O(h). `h` is the height of the tree; the stack holds one path of pending right children, so `O(n)` in the worst case (the result is output).
