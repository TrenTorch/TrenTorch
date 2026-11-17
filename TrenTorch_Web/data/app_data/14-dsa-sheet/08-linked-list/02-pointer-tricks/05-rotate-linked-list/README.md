---
name: sheet-rotate-linked-list
title: 'Rotate a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
theory: rotating-with-a-ring
---

## Statement

Rotate the list to the **right by `k` places**: the last `k` nodes move to the front. `1 -> 2 -> 3 -> 4 -> 5` rotated by 2 is `4 -> 5 -> 1 -> 2 -> 3`. `k` can be much larger than the length.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
rotate_list(head, 2)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[4, 5, 1, 2, 3]
```

**Example 2**

Input:

```python
rotate_list(head, 4)  # head = 0 -> 1 -> 2
```

Output:

```text
[2, 0, 1]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `0 <= k <= 10**9`

## Explanation

After `k %= length`, the cut point is `length - k` nodes from the front. The old tail is linked to the old head to close the circle, and the circle is cut after the new tail.

### Complexity

- Time: O(n). One pass to find the length and the tail, one pass to the new tail.
- Space: O(1). A few pointers.
