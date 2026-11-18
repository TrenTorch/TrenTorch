---
name: sheet-same-tree
title: 'Same Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: same-tree-and-symmetric-tree
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

## Explanation

The two-`None` case ends the recursion successfully; every other mismatch returns `False`.

### Complexity

- Time: O(n). Every node pair is compared once.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the recursion.
