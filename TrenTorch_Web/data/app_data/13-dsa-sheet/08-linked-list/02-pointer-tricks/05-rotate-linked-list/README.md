---
name: sheet-rotate-linked-list
title: 'Rotate a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
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

## Theory

Rotating by the length gives the same list back, so only `k % length` matters. You need the length first: walk to the **tail** while counting. Then the new tail is the node at position `length - k - 1`, the new head is the node after it.

The plan: (1) find the length and the tail, (2) set `k %= length`; if it is `0`, return the list unchanged, (3) walk `length - k - 1` steps to the new tail, (4) cut: `new_head = new_tail.next; new_tail.next = None`, and (5) connect the old tail to the old head: `tail.next = head`.

Rotating one step `k` times, which is what a literal reading suggests, costs `O(n * k)`: far too slow for `k = 10**9`.

## Explanation

After `k %= length`, the cut point is `length - k` nodes from the front. The old tail is linked to the old head to close the circle, and the circle is cut after the new tail.
