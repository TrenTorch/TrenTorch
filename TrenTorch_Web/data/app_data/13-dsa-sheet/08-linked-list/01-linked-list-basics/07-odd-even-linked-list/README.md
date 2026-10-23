---
name: sheet-odd-even-linked-list
title: 'Odd Even Linked List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Intermediate
---

## Statement

Group all nodes at **odd positions** (1st, 3rd, 5th, ...) first, followed by all nodes at **even positions** (2nd, 4th, ...). Keep the original order inside each group. Use `O(1)` extra memory and re-use the nodes.

For `1 -> 2 -> 3 -> 4 -> 5` the answer is `1 -> 3 -> 5 -> 2 -> 4`. The position counts, not the value.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
odd_even_list(head)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[1, 3, 5, 2, 4]
```

**Example 2**

Input:

```python
odd_even_list(head)  # head = 2 -> 1 -> 3 -> 5 -> 6 -> 4 -> 7
```

Output:

```text
[2, 3, 6, 7, 1, 5, 4]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `-10**9 <= val <= 10**9`

## Theory

Build **two chains while walking once**: an odd chain and an even chain, then join the end of the odd chain to the head of the even chain.

Keep `odd` (the last node of the odd chain) and `even` (the last node of the even chain), and remember `even_head`. In each round, link `odd.next` to the node after `even`, move `odd`, then link `even.next` to the node after the new `odd`, move `even`. At the end, `odd.next = even_head`.

The loop condition `while even and even.next` stops when there is no next odd node to take.

## Explanation

`odd` and `even` leapfrog down the list, each skipping over the other. `even_head` was saved before any pointer changed, so the final join `odd.next = even_head` puts the even group after the odd group.
