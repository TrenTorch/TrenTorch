---
name: sheet-range-sum-of-a-bst
title: 'Range Sum of a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Beginner
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return the **sum of the values** in the tree that are between `low` and `high` (both included).

For `[10, 5, 15, 3, 7, None, 18]`, `low = 7` and `high = 15` the answer is `32` (`7 + 10 + 15`).

### Examples

**Example 1**

Input:

```python
range_sum_bst(root, 7, 15)  # root = [10, 5, 15, 3, 7, None, 18]
```

Output:

```text
32
```

**Explanation:** The sum of nodes between 7 and 15 is 32, consisting of the nodes with values 7, 10, and 15. The traversal starts from the left subtree where the first node in range (7) is found, followed by the root (10), and finally the right child of the root (15).

**Example 2**

Input:

```python
range_sum_bst(root, 6, 10)  # root = [10, 5, 15, 3, 7, 13, 18, 1, None, 6]
```

Output:

```text
23
```

**Explanation:** The sum of nodes between 6 and 10 is 23, including nodes with values 6, 7, and 10. The traversal explores the left subtree, finding the node with value 6, then moves up to the root node at 10, while also checking the right subtree to find the node at 7.

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `0 <= low <= high <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A **binary search tree (BST)** is a binary tree where, for every node, all values in its **left** subtree are **smaller** and all values in its **right** subtree are **larger** (values are different). That one rule makes searching fast: at each node you can throw away half of the tree. In a reasonably balanced tree the height is `O(log n)`, so search, insert and delete take `O(log n)`; in a thin tree (a chain) they degrade to `O(n)`. The **inorder** traversal of a BST visits the values in sorted order.

You can **skip subtrees** that cannot hold values in the range. If `node.val < low`, the whole left subtree is smaller still: ignore it and go right. If `node.val > high`, the whole right subtree is larger still: ignore it and go left. Otherwise the node counts, and both subtrees may contain more.

When the range is narrow, this visits only the nodes near the range: `O(h + number of nodes in the range)` instead of `O(n)`.

## Explanation

The two `if` branches prune; the last line adds the node and explores both sides.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                              | Variables       |
| -------------------------------------------- | --------------- |
| `+ range_sum_bst(root.left, low, high)`      | `root = None`   |
| `return 0`                                   | `(no change)`   |
| `return 0`                                   | `(no change)`   |
| `return`                                     | `returned = 7`  |
| `return`                                     | `returned = 0`  |
| `return range_sum_bst(root.left, low, high)` | `root = None`   |
| `return 0`                                   | `(no change)`   |
| `return`                                     | `returned = 32` |

### Complexity

- Time: O(n), where n is the number of nodes in the tree. The algorithm performs a single-pass traversal, visiting each node once to check if its value falls within the specified range.
- Extra space: O(h), where h is the height of the tree. The space complexity is determined by the depth of the recursion stack or the size of the stack used for iterative traversal, which is proportional to the height of the BST.
- The brute force takes O(n), where n is the number of nodes in the tree. The brute-force method also performs a complete traversal of the tree, checking each node against the provided range limits.
