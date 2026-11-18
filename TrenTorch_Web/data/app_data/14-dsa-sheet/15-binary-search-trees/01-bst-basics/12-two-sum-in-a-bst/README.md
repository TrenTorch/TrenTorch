---
name: sheet-two-sum-in-a-bst
title: 'Two Sum in a BST'
tags: [dsa-sheet, binary-search-trees, bst-basics]
difficulty: Intermediate
theory: two-sum-with-two-iterators
---

## Statement

The tests write a tree as a **level-order list** (row by row, left to right) with `None` for a missing child: `[3, 9, 20, None, None, 15, 7]` is a root `3` with children `9` and `20`, where `20` has children `15` and `7`. All trees in this topic that are called BSTs have different values.

Return `True` if there are **two different nodes** whose values add up to `k`.

For `[5, 3, 6, 2, 4, None, 7]` and `k = 9` the answer is `True` (`3 + 6`); for `k = 28` it is `False`.

### Examples

**Example 1**

Input:

```python
find_target(root, 9)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
True
```

**Example 2**

Input:

```python
find_target(root, 28)  # root = [5, 3, 6, 2, 4, None, 7]
```

Output:

```text
False
```

### Constraints

- `0 <= number of nodes <= 100000`
- The tree is a BST, not deeper than 800 levels.
- `-10**9 <= k <= 2 * 10**9`

## Explanation

An in-order walk lists the values of a BST in increasing order, so this is "two sum on a sorted list" without building the list. Use two walkers: one produces the values in increasing order (go left, then visit, then right) and the other in decreasing order (go right, then visit, then left), each with its own stack.

Take the smallest `lo` and the largest `hi`. If `lo + hi` equals `k` return `True`; if it is smaller, advance the increasing walker; if it is larger, advance the decreasing walker. Stop when `lo >= hi`. Each node is visited at most once by each walker and the stacks hold one path each, so the extra memory is `O(h)` instead of `O(n)`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables                                                                                                                                |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `def ascending(node):`                         | `ascending = <function find_target.<locals>.ascending at 0x000002BDE6F...`                                                               |
| `def descending(node):`                        | `descending = <function find_target.<locals>.descending at 0x000002BDE6...`                                                              |
| `up, down = ascending(root), descending(root)` | `up = <generator object find_target.<locals>.ascending at 0x000..., down = <generator object find_target.<locals>.descending at 0x00...` |
| `lo, hi = next(up, None), next(down, None)`    | `lo = 2, hi = 7`                                                                                                                         |
| `total = lo + hi`                              | `total = 9`                                                                                                                              |
| `return`                                       | `returned = True`                                                                                                                        |

### Complexity

- Time: O(n). Two in-order iterators, one ascending and one descending, walk toward each other; every node is visited at most once by each.
- Space: O(h). `h` is the height of the tree (`O(n)` in the worst case, `O(log n)` if it is balanced) for the two stacks.
