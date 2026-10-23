---
name: sheet-binary-tree-paths
title: 'All Root-to-Leaf Paths'
tags: [dsa-sheet, binary-trees, tree-recursion]
difficulty: Intermediate
---

## Statement

Return every **root-to-leaf path** as a string like `"1->2->5"`. List the paths from left to right: all the paths through the left subtree come before the paths through the right subtree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 2, 3, None, 5]` the answer is `["1->2->5", "1->3"]`.

### Examples

**Example 1**

Input:

```python
root_to_leaf_paths(root)  # root = [1, 2, 3, None, 5]
```

Output:

```text
['1->2->5', '1->3']
```

**Example 2**

Input:

```python
root_to_leaf_paths(root)  # root = [1]
```

Output:

```text
['1']
```

### Constraints

- `0 <= number of nodes <= 20000`
- The tree is not deeper than 800 levels.
- `-100 <= val <= 100`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

This question needs **all** answers, not one number. Carry the path so far down the recursion (a list or a string). At a leaf, record the finished path; at an inner node, recurse into the children with the path extended by the node.

Passing the list and appending/popping (**backtracking**) avoids building a new list at each step; passing an immutable string builds a new one each time, which is simpler to read.

The total output size can be large (a deep tree has long paths), which is why the node limit is lower here.

## Explanation

`go(node, path)` extends the path with the node's value. When a node has no children, `"->".join(path)` is a finished answer. Visiting left before right gives the left-to-right order.
