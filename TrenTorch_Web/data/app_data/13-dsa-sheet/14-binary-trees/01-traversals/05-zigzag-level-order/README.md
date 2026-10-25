---
name: sheet-zigzag-level-order
title: 'Zigzag Level Order'
tags: [dsa-sheet, binary-trees, traversals]
difficulty: Intermediate
---

## Statement

Return the values level by level, but **alternate the direction**: the first level left to right, the second right to left, the third left to right again, and so on.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 9, 20, None, None, 15, 7]` the answer is `[[3], [20, 9], [15, 7]]`.

### Examples

**Example 1**

Input:

```python
zigzag_level_order(root)  # root = [3, 9, 20, None, None, 15, 7]
```

Output:

```text
[[3], [20, 9], [15, 7]]
```

**Explanation:** For the input [3, 9, 20, None, None, 15, 7], the first level is [3], the second level is [20, 9] (right to left), and the third level is [15, 7] (left to right).

**Example 2**

Input:

```python
zigzag_level_order(root)  # root = [1, 2, 3, 4, None, None, 5]
```

Output:

```text
[[1], [3, 2], [4, 5]]
```

**Explanation:** For the input [1, 2, 3, 4, None, None, 5], the first level is [1], the second level is [3, 2] (right to left), and the third level is [4, 5] (left to right).

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

This is the level order traversal with one twist. Do the normal BFS (always push the left child before the right child), and **reverse every other level's list** before adding it to the answer. A counter or a boolean flag that flips after each level says which levels to reverse.

The queue order stays the same; only the output order of alternate levels changes. `O(n)`.

## Explanation

`left_to_right` flips after every level. A level is reversed (`level[::-1]`) when it is false.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line               | Variables                                                                                                       |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- |
| `out = []`                    | `out = []`                                                                                                      |
| `for _ in range(len(queue)):` | `queue = deque([<05-zigzag-level-order_solution.TreeNode object at..., left_to_right = True, level = [], _ = 0` |
| `queue.append(node.left)`     | `level = [3], node = <05-zigzag-level-order_solution.TreeNode object at 0x0000...`                              |
| `level.append(node.val)`      | `out = [[3]], left_to_right = False, level = [9]`                                                               |
| `queue.append(node.left)`     | `level = [9, 20], _ = 1`                                                                                        |
| `for _ in range(len(queue)):` | `out = [[3], [20, 9]], left_to_right = True, level = [], _ = 0`                                                 |
| `node = queue.popleft()`      | `queue = deque([]), level = [15], _ = 1`                                                                        |
| `return`                      | `returned = [[3], [20, 9], [15, 7]]`                                                                            |

### Complexity

- Time: O(n).
- Extra space: O(n).
- The brute force takes O(n).
