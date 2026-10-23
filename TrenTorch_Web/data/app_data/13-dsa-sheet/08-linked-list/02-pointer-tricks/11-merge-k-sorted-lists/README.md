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

**Example 2**

Input:

```python
merge_k_lists(lists)  # lists = []
```

Output:

```text
[]
```

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
