---
name: sheet-intersection-of-two-lists
title: 'Intersection of Two Lists'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
---

## Statement

Two lists can **merge into one chain**: from some node on, both lists are the very same nodes (not just equal values). Return the **first shared node**, or `None` if the lists never meet. Do not change the lists and use `O(1)` extra memory.

The tests build `list_b` from its own nodes followed by a join: `{"values": [...], "join": {"param": "list_a", "index": k}}` means its last node points at node `k` of `list_a` (`k = -1` means no join). The tests check the position of the node you returned in `list_a`.

The starter code compares every pair of nodes. It is correct but too slow.

### Examples

**Example 1**

Input:

```python
intersection_node(list_a, list_b)  # list_a = 4 -> 1 -> 8 -> 4 -> 5, list_b = 5 -> 6 -> 1 -> 8 -> 4 -> 5
```

Output:

```text
2
```

The lists meet at the node with value 8 (position 2 of `list_a`).

**Example 2**

Input:

```python
intersection_node(list_a, list_b)  # list_a = 2 -> 6 -> 4, list_b = 1 -> 5, no shared node
```

Output:

```text
-1
```

No shared node: the answer is `None`, shown as `-1`.

### Constraints

- `0 <= number of nodes <= 100000` in each list
- Neither list has a cycle.

## Theory

If one list is longer, the two start at different distances from the shared tail. Two ways to fix that: measure both lengths, skip the extra nodes of the longer one, then walk together; or use a neat trick with **two pointers that switch lists**.

Let `pa` walk list A and, when it falls off the end, continue on list B. Let `pb` do the same the other way around. Both pointers walk `len(A) + len(B)` steps in total, so after changing lists they are **aligned**: they reach the shared node at the same moment. If there is no shared node, both become `None` together at the very end, and the loop stops with `None`.

Compare nodes with `is`, never by value.

## Explanation

Each pointer travels its own list and then the other one. The shorter list's pointer switches earlier, which removes the length difference. The loop ends when the pointers are the same node or both `None`.
