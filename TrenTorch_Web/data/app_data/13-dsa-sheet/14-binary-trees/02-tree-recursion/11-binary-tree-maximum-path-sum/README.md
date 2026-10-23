---
name: sheet-binary-tree-maximum-path-sum
title: 'Maximum Path Sum'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Mastery
---

## Statement

A **path** is a sequence of connected nodes where each pair of neighbours is a parent and its child; it may start and end at **any** nodes and does **not** have to pass through the root, but it uses each node at most once. Return the **largest sum of the values** along any non-empty path.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[-10, 9, 20, None, None, 15, 7]` the answer is `42` (`15 + 20 + 7`).

### Examples

**Example 1**

Input:

```python
max_path_sum(root)  # root = [-10, 9, 20, None, None, 15, 7]
```

Output:

```text
42
```

**Example 2**

Input:

```python
max_path_sum(root)  # root = [1, 2, 3]
```

Output:

```text
6
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-1000 <= val <= 1000`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

This is the diameter question with **sums** instead of lengths, plus negative numbers. Every path has a highest node. Through it, the best path takes the **best downward path on the left** and the **best downward path on the right**, but only when they are positive (a negative branch is better skipped: use `max(0, ...)`).

So `best_through(node) = node.val + max(0, left_gain) + max(0, right_gain)`. The recursion also has to **return** something to the parent: a path that continues upward can only use **one** side, so it returns `node.val + max(0, left_gain, right_gain)`.

Update the global best with `best_through` at each node and return the one-sided gain. `O(n)`.

## Explanation

`gain(node)` is the best sum of a path that starts at `node` and goes down. `best` records the best path that bends at each node, using both sides.
