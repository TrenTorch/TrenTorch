---
name: sheet-maximum-width-of-binary-tree
title: 'Maximum Width of a Binary Tree'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
theory: maximum-width-by-numbering-positions
---

## Statement

The **width** of a level is the distance between its leftmost and rightmost non-empty nodes, **counting the empty places between them** as if the tree were complete (the number of positions from the first to the last node, both included). Return the **largest width** among all levels.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 3, 2, 5, 3, None, 9]` the answer is `4`.

### Examples

**Example 1**

Input:

```python
width_of_tree(root)  # root = [1, 3, 2, 5, 3, None, 9]
```

Output:

```text
4
```

**Example 2**

Input:

```python
width_of_tree(root)  # root = [1, 3, 2, 5]
```

Output:

```text
2
```

### Constraints

- `0 <= number of nodes <= 3000`
- The tree is not deeper than 800 levels.

## Explanation

The queue stores `(node, index)`. At the start of each level the first index is read, and the width is the last index minus it plus 1.

### Complexity

- Time: O(n). A level-by-level pass visits each node once (the position labels are big integers up to `2^depth`).
- Space: O(w). `w` is the widest level, at most `n / 2`.
