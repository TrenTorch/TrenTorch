---
name: sheet-diameter-of-binary-tree
title: 'Diameter of a Binary Tree'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
---

## Statement

The **diameter** is the number of **edges** on the longest path between **any two nodes** of the tree. The path does not have to pass through the root.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 3, 4, 5]` the answer is `3` (the path `4 -> 2 -> 1 -> 3`).

### Examples

**Example 1**

Input:

```python
diameter(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
3
```

**Explanation:** The diameter is 3 because there is a path of three edges from node 4 through 2 and 3 to 1. This is the longest path in the tree.

**Example 2**

Input:

```python
diameter(root)  # root = [1, 2]
```

Output:

```text
1
```

**Explanation:** The diameter is 1 because the tree consists of only two nodes connected by a single edge.

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

The longest path has a **highest node** (the one closest to the root). Through that node the path goes down the left side as far as possible and down the right side as far as possible, so its length is `height(left) + height(right)` (heights counted in edges... or nodes, with the matching adjustment).

So the answer is the **maximum over all nodes** of `height(left) + height(right)`. Computing the height for every node separately would be `O(n²)`. Instead, compute the height **and update the best answer in the same recursion**: each call returns its height, and uses the heights of its children to update a running maximum. `O(n)`.

This pattern, "return one thing up the recursion and record another thing on the side", solves many tree questions.

## Explanation

`height(node)` returns the number of nodes on the longest downward path. `best` is updated with `left + right` at every node; with heights counted in nodes, that sum is exactly the number of edges.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line     | Variables                                                            |
| ------------------- | -------------------------------------------------------------------- |
| `best = 0`          | `best = 0`                                                           |
| `def height(node):` | `height = <function diameter.<locals>.height at 0x000001F4832A6F80>` |
| `height(root)`      | `best = 3`                                                           |
| `return`            | `returned = 3`                                                       |

### Complexity

- Time: O(n) where n is the number of nodes. The height function visits each node once to compute its depth, and the best diameter is updated during this traversal.
- Extra space: O(h) where h is the height of the tree. The space complexity is determined by the maximum depth of the recursive call stack, which corresponds to the height of the binary tree.
- The brute force takes O(n^2) because for each of the n nodes, we compute the height of its left and right subtrees, which involves traversing the entire tree or a significant portion of it, leading to a quadratic overall complexity.
