---
name: sheet-minimum-height-trees
title: 'Minimum Height Trees'
tags: [dsa-sheet, graphs, spanning-trees-and-components]
difficulty: Advanced
theory: minimum-height-trees
---

## Statement

The `edges` form a **tree** on the nodes `0` to `n - 1`. Any node can be chosen as the root, giving a rooted tree with some **height** (the number of edges on the longest path down from the root). Return all the roots that give the **smallest height**, in increasing order.

For `n = 6` and `edges = [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]` the answer is `[3, 4]`.

The starter code measures the height from every possible root. It is correct but too slow for a big tree.

### Examples

**Example 1**

Input:

```python
min_height_trees(6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])
```

Output:

```text
[3, 4]
```

**Example 2**

Input:

```python
min_height_trees(4, [[1, 0], [1, 2], [1, 3]])
```

Output:

```text
[1]
```

### Constraints

- `1 <= n <= 100000`
- `len(edges) == n - 1` and the edges form a tree.

## Explanation

`remaining` is the number of nodes still in the tree; every round removes the current leaves and exposes new ones.

### Complexity

- Time: O(n). Peeling leaves layer by layer removes every node once.
- Space: O(n). The adjacency lists and the degrees.
