---
name: sheet-nodes-at-distance-k
title: 'Nodes at Distance K'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
---

## Statement

The tree has **different values**. Return the values of all nodes that are exactly `k` edges away from the node with value `target` (moving up or down any edges), as a **sorted** list. The `target` is in the tree.

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]`, `target = 5` and `k = 2` the answer is `[1, 4, 7]`.

### Examples

**Example 1**

Input:

```python
distance_k(root, 5, 2)  # root = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
```

Output:

```text
[1, 4, 7]
```

**Explanation:** From node 5, distance 2 nodes are its grandparent 1 and grandchildren 4 and 7 via its child 2, sorted gives [1,4,7].

**Example 2**

Input:

```python
distance_k(root, 1, 3)  # root = [1]
```

Output:

```text
[]
```

**Explanation:** The tree has only node 1, so no node exists at distance 3, returning empty list.

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- All values are different; `0 <= k <= 100000`.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

A node only knows its children, but the nodes at distance `k` can also be reached **through the parent**. The fix is to turn the tree into an **undirected graph**: first walk the tree once and record each node's **parent** (a dictionary `node -> parent`). Now you can move to `left`, `right` and `parent`.

Then run a **BFS from the target**: start at distance 0, and expand level by level for `k` rounds, remembering visited nodes so you do not go back. The nodes still in the queue after `k` rounds are the answer.

This "give nodes a parent pointer" step is the standard way to make tree questions about distances solvable. `O(n)`.

## Explanation

`parent` is built with one DFS. The BFS visits neighbours (children and parent) that are not yet seen; after `k` rounds the frontier is exactly the nodes at distance `k`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parent = {}`                    | `parent = {}`                                                                                                                                        |
| `node, par = stack.pop()`        | `start = None, stack = [], node = <03-nodes-at-distance-k_solution.TreeNode object at 0x000..., par = None`                                          |
| `node, par = stack.pop()`        | `parent = {<03-nodes-at-distance-k_solution.TreeNode object at 0x00..., par = <03-nodes-at-distance-k_solution.TreeNode object at 0x000...`          |
| `node, par = stack.pop()`        | `start = <03-nodes-at-distance-k_solution.TreeNode object at 0x000...`                                                                               |
| `node = frontier.popleft()`      | `seen = {<03-nodes-at-distance-k_solution.TreeNode object at 0x00..., frontier = deque([]), _ = 0`                                                   |
| `for _ in range(k):`             | `frontier = deque([<03-nodes-at-distance-k_solution.TreeNode object a..., _ = 1, nxt = <03-nodes-at-distance-k_solution.TreeNode object at 0x000...` |
| `for _ in range(len(frontier)):` | `(no change)`                                                                                                                                        |
| `return`                         | `returned = [1, 4, 7]`                                                                                                                               |
