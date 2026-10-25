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

**Explanation:** First two nodes 1,2 are reversed to 2,1 and next two 3,4 to 4,3, leaving 5 alone because fewer than k remain.

**Example 2**

Input:

```python
reverse_k_group(head, 3)  # head = 1 -> 2 -> 3 -> 4 -> 5
```

Output:

```text
[3, 2, 1, 4, 5]
```

**Explanation:** First three nodes 1,2,3 are reversed to 3,2,1 and the remaining nodes 4,5 stay in place because the final group has fewer than k elements.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                           | Variables                                                                                                                                                                                                            |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dummy = ListNode(0, head)`               | `dummy = <12-reverse-nodes-in-k-group_solution.ListNode object at ...`                                                                                                                                               |
| `kth = group_prev`                        | `group_prev = <12-reverse-nodes-in-k-group_solution.ListNode object at ..., kth = <12-reverse-nodes-in-k-group_solution.ListNode object at ...`                                                                      |
| `for _ in range(k):`                      | `_ = 1`                                                                                                                                                                                                              |
| `prev, cur = group_next, group_prev.next` | `group_next = <12-reverse-nodes-in-k-group_solution.ListNode object at ..., prev = <12-reverse-nodes-in-k-group_solution.ListNode object at ..., cur = <12-reverse-nodes-in-k-group_solution.ListNode object at ...` |
| `first = group_prev.next`                 | `after = <12-reverse-nodes-in-k-group_solution.ListNode object at ..., first = <12-reverse-nodes-in-k-group_solution.ListNode object at ...`                                                                         |
| `for _ in range(k):`                      | `(no change)`                                                                                                                                                                                                        |
| `for _ in range(k):`                      | `(no change)`                                                                                                                                                                                                        |
| `return`                                  | `returned = <12-reverse-nodes-in-k-group_solution.ListNode object at ...`                                                                                                                                            |

### Complexity

- Time: O(n) time where n is number of nodes.
- Extra space: O(1) extra space for pointers.
- The brute force takes O(n) time where n is number of nodes.
