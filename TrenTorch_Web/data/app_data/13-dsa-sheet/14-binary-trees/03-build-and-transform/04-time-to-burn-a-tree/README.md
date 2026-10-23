---
name: sheet-time-to-burn-a-tree
title: 'Time to Burn a Tree'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
---

## Statement

A fire starts at the node with value `start` (all values are different). Each minute, the fire spreads from every burning node to its **neighbours**: its parent and its two children. Return the **number of minutes** until the whole tree is burning (`0` if the tree has only that node).

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`.

For `[1, 5, 3, None, 4, 10, 6, 9, 2]` and `start = 3` the answer is `4`.

### Examples

**Example 1**

Input:

```python
burn_time(root, 3)  # root = [1, 5, 3, None, 4, 10, 6, 9, 2]
```

Output:

```text
4
```

**Example 2**

Input:

```python
burn_time(root, 1)  # root = [1]
```

Output:

```text
0
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- All values are different and `start` is in the tree.

## Theory

A **binary tree** is made of nodes; each node has a value and up to two children, `left` and `right`. The first node is the **root**; a node with no children is a **leaf**. A tree is a recursive structure: the left child of a node is the root of a smaller tree, so most tree questions can be solved by solving the same question for the left and right subtrees and combining the answers.

The fire moves along the edges one step per minute, so the time to burn the tree is the **largest distance** from the start node to any node: the **farthest node**. This is the same setup as "nodes at distance k": record the parent of every node, then run a **BFS** from the start in all three directions, and count the number of levels.

The answer is the number of BFS rounds needed to reach the last node (the depth of the BFS minus... count rounds after the first). `O(n)`.

## Explanation

Each round of the BFS is one minute. The loop stops when no new node can be reached; the number of completed rounds that reached new nodes is the answer.
