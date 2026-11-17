---
name: sheet-lowest-common-ancestor
title: 'Lowest Common Ancestor'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
theory: lowest-common-ancestor
---

## Statement

The **lowest common ancestor** of two values `p` and `q` is the lowest node that has **both** of them in its subtree (a node counts as being in its own subtree). All values in the tree are different, and both `p` and `q` are in the tree. Return that **node**. The tests check its value.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]`, `p = 5` and `q = 1` the answer is the node `3`; for `p = 5` and `q = 4` it is the node `5`.

### Examples

**Example 1**

Input:

```python
lowest_common_ancestor(root, 5, 1)  # root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
```

Output:

```text
3
```

**Example 2**

Input:

```python
lowest_common_ancestor(root, 5, 4)  # root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
```

Output:

```text
5
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- All values are different; `p != q` and both are in the tree.

## Explanation

When the recursion reaches `p` or `q` it stops and returns that node (a node is an ancestor of itself). The first node with two non-empty answers from its children is the split point.

### Complexity

- Time: O(n). Every node is visited at most once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
