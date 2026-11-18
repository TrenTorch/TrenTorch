---
name: sheet-remove-linked-list-elements
title: 'Remove Matching Nodes'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
theory: delete-every-match
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

## Explanation

`prev` is the last node we kept. A match is skipped by linking `prev` straight to the node after it; a non-match becomes the new `prev`.

### Complexity

- Time: O(n). One pass; a matching node is skipped by relinking.
- Space: O(1). Two pointers.
