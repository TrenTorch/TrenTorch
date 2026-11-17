---
name: sheet-nodes-at-distance-k
title: 'Nodes at Distance K'
tags: [dsa-sheet, binary-trees, build-and-transform]
difficulty: Advanced
theory: nodes-at-distance-k
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

**Example 2**

Input:

```python
distance_k(root, 1, 3)  # root = [1]
```

Output:

```text
[]
```

### Constraints

- `1 <= number of nodes <= 100000`
- The tree is not deeper than 800 levels.
- All values are different; `0 <= k <= 100000`.

## Explanation

`parent` is built with one DFS. The BFS visits neighbours (children and parent) that are not yet seen; after `k` rounds the frontier is exactly the nodes at distance `k`.

### Complexity

- Time: O(n). One pass records every parent, then a breadth-first search of at most `k` levels visits each node once.
- Space: O(n). The parent table and the visited set.
