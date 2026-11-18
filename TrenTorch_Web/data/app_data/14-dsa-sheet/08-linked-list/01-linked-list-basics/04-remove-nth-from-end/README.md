---
name: sheet-remove-nth-from-end
title: 'Remove the Nth Node From the End'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
theory: two-runners-with-a-gap
---

## Statement

Remove the **`n`-th node from the end** of the list (the last node is `n = 1`) and return the head. Do it in **one pass**.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
remove_nth_from_end(head, 2)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 2, 3, 5]
```

**Example 2**

Input:

```python
remove_nth_from_end(head, 1)  # head = 1
```

Output:

```text
[]
```

### Constraints

- `1 <= number of nodes <= 100000`
- `1 <= n <= number of nodes`
- `-10**9 <= val <= 10**9`

## Explanation

`fast` starts `n` steps ahead of `slow`. Both move until `fast.next` is `None`, which leaves `slow` on the node before the one to remove. `slow.next = slow.next.next` unlinks it.

### Complexity

- Time: O(n). One pass: `fast` starts `n` nodes ahead, so when it reaches the end `slow` is just before the node to remove.
- Space: O(1). Three pointers.
