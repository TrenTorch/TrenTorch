---
name: sheet-path-sum
title: 'Root-to-Leaf Path Sum'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
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

**Explanation:** The path 5 -> 4 -> 11 -> 2 from root to leaf sums to 22.

**Example 2**

Input:

```python
has_path_sum(root, 5)  # root = [1, 2, 3]
```

Output:

```text
False
```

**Explanation:** No root-to-leaf path in the tree sums to 5.

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-1000 <= val <= 1000`, `-10**9 <= target <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Pass the **remaining sum** down the recursion. At each node subtract its value from the target; the question for a child is the same question with the smaller target. At a **leaf**, the path is complete: it works exactly when the remaining target equals the leaf's value.

The answer for a node is `True` if either child's subtree has a matching path (`or`). Remember that only leaves end a path: a node with a single child must continue into it.

## Explanation

The leaf check `not root.left and not root.right` is where the path ends. For inner nodes the target shrinks by the node's value.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                          | Variables                                                                                     |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| `rest = target - root.val`                                               | `rest = 17`                                                                                   |
| `rest = target - root.val`                                               | `root = <06-path-sum_solution.TreeNode object at 0x000001F4854CCCA0>, target = 17, rest = 13` |
| `return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)` | `root = <06-path-sum_solution.TreeNode object at 0x000001F4854CE1A0>, target = 13`            |
| `return has_path_sum(root.left, rest) or has_path_sum(root.right, rest)` | `root = <06-path-sum_solution.TreeNode object at 0x000001F4854CE650>, target = 2`             |
| `return`                                                                 | `returned = False`                                                                            |
| `return`                                                                 | `returned = True`                                                                             |
| `return`                                                                 | `(no change)`                                                                                 |
| `return`                                                                 | `(no change)`                                                                                 |

### Complexity

- Time: O(n), n is number of nodes.
- Extra space: O(h), h is height of tree.
- The brute force takes O(n), n nodes.
