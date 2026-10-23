---
name: sheet-same-tree
title: 'Same Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
---

## Statement

Return `True` if the two trees `p` and `q` are **identical**: the same shape and the same value at every node.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `p = [1, 2, 3]` and `q = [1, 2, 3]` the answer is `True`; for `[1, 2]` and `[1, None, 2]` it is `False`.

### Examples

**Example 1**

Input:

```python
is_same_tree(p, q)  # p = [1, 2, 3], q = [1, 2, 3]
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_same_tree(p, q)  # p = [1, 2], q = [1, None, 2]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000` in each tree
- The trees are not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

Compare the two trees in lockstep. Two trees are the same when both are empty, or both are non-empty with equal values and the left subtrees are the same **and** the right subtrees are the same.

Return `False` as soon as one is empty and the other is not, or the values differ: the three base cases. `O(min(n, m))`.

## Explanation

The two-`None` case ends the recursion successfully; every other mismatch returns `False`.
