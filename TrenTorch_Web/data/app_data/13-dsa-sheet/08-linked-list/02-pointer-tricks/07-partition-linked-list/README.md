---
name: sheet-partition-linked-list
title: 'Partition a Linked List'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
---

## Statement

Rearrange the list so that **all nodes with a value less than `x` come before** nodes with a value greater than or equal to `x`. Keep the **original relative order** inside each of the two groups.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
partition_list(head, 3)  # head = 1 -> 4 -> 3 -> 2 -> 5 -> 2
```

Output:

```text
[1, 2, 2, 4, 3, 5]
```

**Example 2**

Input:

```python
partition_list(head, 2)  # head = 2 -> 1
```

Output:

```text
[1, 2]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-1000 <= val, x <= 1000`

## Theory

Build two separate lists in one walk: a **small** list and a **large** list, each with its own dummy head and tail. Append each node to the one it belongs to. At the end, link the small list's tail to the large list's head, and set the large list's tail `next` to `None`.

That last step is easy to forget. The last large node may still point to some node that is now in the small list, which would create a **cycle**. Always end the combined list explicitly.

The same "split into chains, then join" idea solves the odd-even list question.

## Explanation

`small_tail` and `large_tail` grow two chains. `large_tail.next = None` cuts any stale pointer; `small_tail.next = large_dummy.next` joins them.
