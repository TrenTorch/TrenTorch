---
name: sheet-remove-linked-list-elements
title: 'Remove Matching Nodes'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
---

## Statement

Remove **every node** whose value equals `val` and return the new head.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
remove_elements(head, 6)  # head = 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6
```

Output:

```text
[1, 2, 3, 4, 5]
```

**Example 2**

Input:

```python
remove_elements(head, 7)  # head = 7 -> 7 -> 7
```

Output:

```text
[]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `0 <= val, node value <= 1000`

## Theory

To delete a node you change the `next` of the node **before** it. So walk with a `prev` pointer: if the current node matches, set `prev.next = cur.next`; otherwise move `prev` forward. `cur` always moves forward.

The head is the awkward case: it has no node before it. A **dummy node** placed in front of the head fixes this, because then every real node has a predecessor. Return `dummy.next`.

Several matches in a row work correctly because `prev` stays where it is until a non-matching node appears.

## Explanation

`prev` is the last node we kept. A match is skipped by linking `prev` straight to the node after it; a non-match becomes the new `prev`.
