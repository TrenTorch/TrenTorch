---
name: sheet-reverse-nodes-in-k-group
title: 'Reverse Nodes in K-Groups'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Mastery
---

## Statement

Reverse the nodes of the list **`k` at a time** and return the head. If the number of nodes left at the end is less than `k`, leave that last group as it is. Change the pointers, not the values.

For `1 -> 2 -> 3 -> 4 -> 5` and `k = 2` the answer is `2 -> 1 -> 4 -> 3 -> 5`.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
reverse_k_group(head, 2)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[2, 1, 4, 3, 5]
```

**Example 2**

Input:

```python
reverse_k_group(head, 3)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[3, 2, 1, 4, 5]
```

### Constraints

- `0 <= number of nodes <= 100000`
- `1 <= k <= 100000`

## Theory

This is "reverse a list" applied to every block of `k` nodes, and then the blocks have to be **reconnected**. Process one block at a time:

1. From `group_prev` (the node before the block), walk `k` steps to find the block's last node `kth`. If you run out of nodes, the rest is too short: stop.
2. Remember `group_next = kth.next`.
3. Reverse the block, with `prev` starting at `group_next` so the first node of the block automatically ends up pointing at the rest of the list.
4. Hook the block in: `group_prev.next = kth`. The block's old first node is now its last node, so it becomes the next `group_prev`.

A dummy head makes the first block like all the others. The total work is `O(n)`, because every node is walked a constant number of times.

## Explanation

Reversing with `prev = group_next` means the old first node of the block points at the node after the block. `first` (the old first node) is now the block's tail, and it is the `group_prev` for the next block.
