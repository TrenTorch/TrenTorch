---
name: sheet-insert-into-a-bst
title: 'Insert into a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
theory: inserting-a-new-leaf
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Insert the value `val` (it is not in the tree yet) as a **new leaf** so that the tree is still a BST, and return the root. Walk down as in a search, and attach the new node where the search falls off the tree.

For `[4, 2, 7, 1, 3]` and `val = 5` the answer is `[4, 2, 7, 1, 3, 5]`.

### Examples

**Example 1**

Input:

```python
insert_into_bst(root, 5)  # root = [4, 2, 7, 1, 3]
```

Output:

```text
[4, 2, 7, 1, 3, 5]
```

**Example 2**

Input:

```python
insert_into_bst(root, 5)  # root = []
```

Output:

```text
[5]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `val` is not already in the tree.

## Explanation

The loop keeps `parent` one step behind `node`. When `node` is `None` the new leaf is attached to the correct side of `parent`.

### Complexity

- Time: O(h). The new value follows one root-to-leaf path.
- Space: O(1). One pointer (one new node); `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced).
