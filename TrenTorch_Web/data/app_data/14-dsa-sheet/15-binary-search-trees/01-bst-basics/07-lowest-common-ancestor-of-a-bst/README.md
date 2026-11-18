---
name: sheet-lowest-common-ancestor-of-a-bst
title: 'Lowest Common Ancestor in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: lowest-common-ancestor-in-a-bst
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **lowest common ancestor** of the values `p` and `q`: the lowest node that has both in its subtree (a node counts as being in its own subtree). Both values are in the tree. The tests check the value of the node you return.

For `[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]`, `p = 2` and `q = 8` the answer is the node `6`; for `p = 2` and `q = 4` it is the node `2`.

### Examples

**Example 1**

Input:

```python
lca_bst(root, 2, 8)  # root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
```

Output:

```text
6
```

**Example 2**

Input:

```python
lca_bst(root, 2, 4)  # root = [6, 2, 8, 0, 4, 7, 9, None, None, 3, 5]
```

Output:

```text
2
```

### Constraints

- `2 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `p` and `q` are values in the tree.

## Explanation

The loop descends while both values are on the same side. The first node where they split (or equal one of them) is returned.

### Complexity

- Time: O(h). The first node whose value lies between `p` and `q` is the answer, one walk down.
- Space: O(1). One pointer; `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
