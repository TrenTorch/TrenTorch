---
name: sheet-merge-k-sorted-lists
title: 'Merge K Sorted Lists'
tags: [dsa-sheet, linked-list, pointer-tricks]
difficulty: Advanced
---

## Statement

`lists` is a list of `k` linked lists, each sorted in increasing order. **Merge them all** into one sorted list and return its head.

The starter code merges the lists into a growing result one after another. It is correct but too slow when there are many lists.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`. Here `lists` is shown as a list of such lists.

### Examples

**Example 1**

Input:

```python
merge_k_lists(lists)  # lists = [1 -> 4 -> 5, 1 -> 3 -> 4, 2 -> 6]
```

Output:

```text
[1, 1, 2, 3, 4, 4, 5, 6]
```

**Explanation:** The priority queue tracks the smallest current element across the three lists, yielding values in non decreasing order: 1, 1, 2, 3, 4, 4, 5, 6.

**Example 2**

Input:

```python
merge_k_lists(lists)  # lists = []
```

Output:

```text
[]
```

**Explanation:** An empty input list contains no nodes to merge, resulting in an empty linked list.

### Constraints

- `0 <= k <= 10000`
- `0 <= total number of nodes <= 100000`
- `-10**9 <= val <= 10**9`
- Each list is sorted in increasing order (a list may be empty).

## Theory

Merging the lists one by one repeats work: the growing result is walked again for every new list, so with `k` lists it costs `O(N * k)` for `N` nodes in total.

Better: always pick the **smallest front node among all lists**. A **min-heap** gives that in `O(log k)`. Put the first node of each list in the heap as `(value, list_index, node)`; pop the smallest, append it to the answer, and push its successor. The `list_index` in the tuple breaks ties so Python never has to compare two nodes (which would be an error).

Total time is `O(N log k)`. An alternative with the same cost is to merge the lists **in pairs**, like a tournament, `log k` rounds.

## Explanation

The heap always holds at most one node per list: the front of each list that is not yet used. Each pop outputs the globally smallest remaining value.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                                        | Variables                                                                                                                                                |
| ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `heap = [(node.val, i, node) for i, node in enumerate(lists) if node]` | `heap = [(1, 0, <11-merge-k-sorted-lists_solution.ListNode object...`                                                                                    |
| `tail = dummy`                                                         | `dummy = <11-merge-k-sorted-lists_solution.ListNode object at 0x00..., tail = <11-merge-k-sorted-lists_solution.ListNode object at 0x00...`              |
| `_, i, node = heapq.heappop(heap)`                                     | `heap = [(1, 1, <11-merge-k-sorted-lists_solution.ListNode object..., _ = 1, i = 0, node = <11-merge-k-sorted-lists_solution.ListNode object at 0x00...` |
| `_, i, node = heapq.heappop(heap)`                                     | `heap = [(3, 1, <11-merge-k-sorted-lists_solution.ListNode object..., _ = 2, i = 2`                                                                      |
| `_, i, node = heapq.heappop(heap)`                                     | `heap = [(4, 0, <11-merge-k-sorted-lists_solution.ListNode object..., _ = 3, i = 1`                                                                      |
| `_, i, node = heapq.heappop(heap)`                                     | `heap = [(5, 0, <11-merge-k-sorted-lists_solution.ListNode object..., _ = 4`                                                                             |
| `_, i, node = heapq.heappop(heap)`                                     | `heap = [(6, 2, <11-merge-k-sorted-lists_solution.ListNode object..., _ = 5, i = 0`                                                                      |
| `return`                                                               | `returned = <11-merge-k-sorted-lists_solution.ListNode object at 0x00...`                                                                                |

### Complexity

- Time: O(N log k), where N is the total number of nodes and k is the number of linked lists.
- Extra space: O(k), where k is the number of linked lists stored in the priority queue.
- The brute force takes O(N log N), where N is the total number of nodes across all lists.
