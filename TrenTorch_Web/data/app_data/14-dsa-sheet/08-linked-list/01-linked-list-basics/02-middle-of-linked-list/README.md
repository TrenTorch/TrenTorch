---
name: sheet-middle-of-linked-list
title: 'Middle of a Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
theory: two-runners
---

## Statement

Return the **middle node** of the list. When the list has an even number of nodes there are two middle nodes: return the **second** one. The answer is the node together with all nodes after it.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
middle_node(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[3, 4, 5]
```

**Example 2**

Input:

```python
middle_node(head)  # head = 1 -> 2 -> 3 -> 4
```

Output:

```text
[3, 4]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Explanation

`fast` moves twice as fast as `slow`. When `fast` can no longer take two steps, `slow` is exactly halfway. For `1 -> 2 -> 3 -> 4` the loop ends with `slow` on `3`, the second middle.

### Complexity

- Time: O(n). `fast` moves two nodes for every one of `slow`, so `slow` stops in the middle after `n / 2` steps.
- Space: O(1). Two pointers.
