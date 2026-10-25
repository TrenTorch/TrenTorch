---
name: sheet-postorder-traversal
title: 'Postorder Traversal'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
---

## Statement

Return the values of the tree in **postorder**: visit the left subtree, then the right subtree, then the node itself.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, None, 2, 3]` the answer is `[3, 2, 1]`.

### Examples

**Example 1**

Input:

```python
postorder_traversal(root)  # root = [1, None, 2, 3]
```

Output:

```text
[3, 2, 1]
```

**Explanation:** The tree has root 1, right child 2, and 2's left child 3; postorder visits 3, then 2, then 1, producing [3, 2, 1].

**Example 2**

Input:

```python
postorder_traversal(root)  # root = [1, 2, 3, 4, 5]
```

Output:

```text
[4, 5, 2, 3, 1]
```

**Explanation:** The tree is root 1 with left child 2 (children 4 and 5) and right child 3; postorder yields 4, 5, 2 from the left subtree, then 3, then 1, so [4, 5, 2, 3, 1].

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

**Postorder** visits a node **after** its children. It is the order for deleting a tree, or for computing something that depends on both subtrees (the height, the size, the sum).

A short iterative trick: postorder is the **reverse** of "node, right, left". So run the preorder loop with the children pushed in the opposite order (left, then right), which visits node, right, left, and reverse the result at the end.

## Explanation

The loop produces node, right, left; reversing it gives left, right, node.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                    |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| `out = []`                       | `out = []`                                                                                   |
| `stack = [root] if root else []` | `stack = [<03-postorder-traversal_solution.TreeNode object at 0x00...`                       |
| `out.append(node.val)`           | `out = [1], stack = [], node = <03-postorder-traversal_solution.TreeNode object at 0x000...` |
| `stack.append(node.right)`       | `stack = [<03-postorder-traversal_solution.TreeNode object at 0x00...`                       |
| `out.append(node.val)`           | `out = [1, 2], stack = []`                                                                   |
| `stack.append(node.left)`        | `stack = [<03-postorder-traversal_solution.TreeNode object at 0x00...`                       |
| `out.append(node.val)`           | `out = [1, 2, 3], stack = []`                                                                |
| `return`                         | `returned = [3, 2, 1]`                                                                       |

### Complexity

- Time: O(n) where n is number of nodes.
- Extra space: O(n), for the stack and output list.
- The brute force takes O(n), where n is the number of nodes in the tree.
