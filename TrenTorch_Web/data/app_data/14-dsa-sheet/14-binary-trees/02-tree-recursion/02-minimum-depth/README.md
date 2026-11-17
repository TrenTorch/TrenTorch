---
name: sheet-minimum-depth
title: 'Minimum Depth'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Beginner
theory: minimum-depth
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

**Example 2**

Input:

```python
min_depth(root)  # root = [2, None, 3, None, 4]
```

Output:

```text
3
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Explanation

The BFS returns the depth of the first node without children. For a tree that is deep on one side only, the recursion would otherwise visit everything.

### Complexity

- Time: O(n). A level-by-level search stops at the first leaf, so it visits no more than `n` nodes.
- Space: O(w). `w` is the widest level, at most `n / 2`.
