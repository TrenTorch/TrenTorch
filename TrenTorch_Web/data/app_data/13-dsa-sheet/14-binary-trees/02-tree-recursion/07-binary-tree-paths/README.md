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

**Explanation:** The tree has two leaves, one at the end of the left path and one at the end of the right path. The solution builds the paths by appending the values of the nodes along the way and joining them with arrows.

**Example 2**

Input:

```python
root_to_leaf_paths(root)  # root = [1]
```

Output:

```text
['1']
```

**Explanation:** The tree has only one node, which is both the root and the leaf. The solution appends the root's value to the path and returns it as the only path.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line       | Variables                                                           |
| --------------------- | ------------------------------------------------------------------- |
| `out = []`            | `out = []`                                                          |
| `def go(node, path):` | `go = <function root_to_leaf_paths.<locals>.go at 0x000001F4832...` |
| `go(root, [])`        | `out = ['1->2->5', '1->3']`                                         |
| `return`              | `returned = ['1->2->5', '1->3']`                                    |

### Complexity

- Time: O(n).
- Extra space: O(h), where h is the height of the tree, for the recursion stack and the current path string.
- The brute force takes O(n), where n is the number of nodes, as the brute-force algorithm performs a depth-first search to find and concatenate all root-to-leaf paths.
