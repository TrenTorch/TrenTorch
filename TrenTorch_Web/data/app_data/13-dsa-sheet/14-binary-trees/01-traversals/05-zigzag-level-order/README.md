---
name: sheet-zigzag-level-order
title: 'Zigzag Level Order'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
---

## Statement

Return the values level by level, but **alternate the direction**: the first level left to right, the second right to left, the third left to right again, and so on.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[3], [20, 9], [15, 7]]`.

### Examples

**Example 1**

Input:

```python
zigzag_level_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[3], [20, 9], [15, 7]]
```

**Example 2**

Input:

```python
zigzag_level_order(root)  # root = [1, 2, 3, 4, None, None, 5]
```

Output:

```text
[[1], [3, 2], [4, 5]]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

This is the level order traversal with one twist. Do the normal BFS (always push the left child before the right child), and **reverse every other level's list** before adding it to the answer. A counter or a boolean flag that flips after each level says which levels to reverse.

The queue order stays the same; only the output order of alternate levels changes. `O(n)`.

## Explanation

`left_to_right` flips after every level. A level is reversed (`level[::-1]`) when it is false.
