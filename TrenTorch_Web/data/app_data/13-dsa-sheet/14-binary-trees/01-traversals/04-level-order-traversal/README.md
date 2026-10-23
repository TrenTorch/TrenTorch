---
name: sheet-level-order-traversal
title: 'Level Order Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
---

## Statement

Return the values **level by level**, from the top, and left to right inside each level. The result is a list of lists, one per level.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[3], [9, 20], [15, 7]]`.

### Examples

**Example 1**

Input:

```python
level_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[3], [9, 20], [15, 7]]
```

**Example 2**

Input:

```python
level_order(root)  # root = [1]
```

Output:

```text
[[1]]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Depth-first traversals (inorder, preorder, postorder) go deep before they go wide. **Level order** goes wide first: it is **breadth-first search (BFS)**, and its tool is a **queue**.

Start with the root in a queue. Repeat while the queue is not empty: the nodes in the queue right now are exactly one level, so remember `size = len(queue)`, pop `size` nodes (record their values as one list), and push their children for the next level.

Every node enters and leaves the queue once: `O(n)`. Use `collections.deque` for an `O(1)` pop from the front.

## Explanation

`for _ in range(len(queue))` handles exactly one level, because the children pushed meanwhile are added after the original size was read.
