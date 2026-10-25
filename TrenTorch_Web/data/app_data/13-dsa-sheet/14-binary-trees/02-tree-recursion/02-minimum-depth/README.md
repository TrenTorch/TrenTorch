---
name: sheet-minimum-depth
title: 'Minimum Depth'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
---

## Statement

Return the number of nodes on the **shortest path from the root down to a leaf** (a node with no children). An empty tree gives `0`.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `2`; for `[2, None, 3, None, 4]` it is `3`.

### Examples

**Example 1**

Input:

```python
min_depth(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
2
```

**Explanation:** Root 3 has left child 9 which is a leaf, so shortest path has 2 nodes.

**Example 2**

Input:

```python
min_depth(root)  # root = [2, None, 3, None, 4]
```

Output:

```text
3
```

**Explanation:** Root 2 has only right child 3, which has only right child 4, a leaf, giving path of 3 nodes.

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

This looks like the maximum depth with `min` instead of `max`, but there is a trap: a node with **only one child** is not a leaf, so the path must continue into that child. `min(depth(left), depth(right))` would wrongly take the empty side as depth 0.

Handle the cases: if a child is missing, the answer comes from the other child (`1 + depth(other)`); if both exist, `1 + min(both)`.

BFS finds it more directly: the first leaf you reach in level order is the closest one. That can stop early without visiting the whole tree.

## Explanation

The BFS returns the depth of the first node without children. For a tree that is deep on one side only, the recursion would otherwise visit everything.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                                                                                           |
| -------------------------------------- | --------------------------------------------------------------------------------------------------- |
| `queue = deque([(root, 1)])`           | `queue = deque([(<02-minimum-depth_solution.TreeNode object at 0x0...`                              |
| `node, depth = queue.popleft()`        | `queue = deque([]), node = <02-minimum-depth_solution.TreeNode object at 0x000001F48..., depth = 1` |
| `queue.append((node.left, depth + 1))` | `queue = deque([(<02-minimum-depth_solution.TreeNode object at 0x0...`                              |
| `node, depth = queue.popleft()`        | `depth = 2`                                                                                         |
| `return`                               | `returned = 2`                                                                                      |

### Complexity

- Time: O(n) where n is the number of nodes.
- Extra space: O(n) where n is the number of nodes.
- The brute force takes O(n) where n is the number of nodes.
