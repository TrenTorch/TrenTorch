---
name: sheet-linked-list-cycle-length
title: 'Length of the Cycle'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Intermediate
---

## Statement

Return the **number of nodes in the cycle**, or `0` if the list has no cycle.

A list can have a **cycle**: the last node's `next` points back at an earlier node. The tests give such a list as `{"values": [...], "cycle": k}`, where the last node points back at node `k` (counting from 0), and `k = -1` means no cycle.

### Examples

**Example 1**

Input:

```python
cycle_length(head)  # head = 3 -> 2 -> 0 -> -4, and -4 points back at 2
```

Output:

```text
3
```

**Explanation:** The list has four nodes and a cycle starting at index 1, so the cycle contains nodes 2, 0, and -4 giving length 3.

**Example 2**

Input:

```python
cycle_length(head)  # head = 1 -> 2, no cycle
```

Output:

```text
0
```

**Explanation:** The list has two nodes and no cycle because cycle is -1, so the cycle length is 0.

### Constraints

- `0 <= number of nodes <= 100000`
- The cycle position `k` is `-1` or a valid index.

## Theory

Once slow and fast pointers **meet**, they are both inside the cycle. Leave `fast` where it is and walk another pointer around the cycle until it returns to the meeting node, counting the steps. That count is the cycle length.

If `fast` falls off the end instead, there is no cycle: return `0`.

This is the same tortoise and hare idea, finished with a short counting loop.

## Explanation

After the meeting, `node = slow.next` and `length = 1` start the count; each step moves one node, and the loop ends back at `slow`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line      | Variables                                                                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `slow = fast = head` | `slow = <03-linked-list-cycle-length_solution.ListNode object at ..., fast = <03-linked-list-cycle-length_solution.ListNode object at ...` |
| `length = 1`         | `length = 1`                                                                                                                               |
| `node = slow.next`   | `node = <03-linked-list-cycle-length_solution.ListNode object at ...`                                                                      |
| `length += 1`        | `length = 2`                                                                                                                               |
| `length += 1`        | `length = 3`                                                                                                                               |
| `return`             | `returned = 3`                                                                                                                             |

### Complexity

- Time: O(n) where n is number of nodes.
- Extra space: O(1) extra memory.
- The brute force takes O(n) where n is number of nodes.
