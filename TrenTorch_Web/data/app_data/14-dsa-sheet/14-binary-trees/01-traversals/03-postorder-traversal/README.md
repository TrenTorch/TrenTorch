---
name: sheet-postorder-traversal
title: 'Postorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
theory: iterative-postorder
---

## Statement

Return the values of the tree in **postorder**: visit the left subtree, then the right subtree, then the node itself.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[3, 2, 1]`.

### Examples

**Example 1**

Input:

```python
postorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[3, 2, 1]
```

**Example 2**

Input:

```python
postorder_traversal(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
[4, 5, 2, 3, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Explanation

The loop produces node, right, left; reversing it gives left, right, node.

### Complexity

- Time: O(n). Each node is pushed and popped once, and the reversal is one more pass.
- Space: O(n). The stack and the reversed output.
