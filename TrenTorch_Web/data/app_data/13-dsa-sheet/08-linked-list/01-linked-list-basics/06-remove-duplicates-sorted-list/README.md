---
name: sheet-remove-duplicates-sorted-list
title: 'Remove Duplicates From a Sorted List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
---

## Statement

`head` is a list sorted in increasing order. Delete duplicates so that **each value appears once** and return the list.

The tests show a list as a Python list of its values: `[1, 2, 3]` stands for `1 -> 2 -> 3`.

### Examples

**Example 1**

Input:

```python
remove_duplicates_sorted(head)  # head = 1 -> 1 -> 2
```

Output:

```text
[1, 2]
```

**Explanation:** The two adjacent 1s are duplicates; the second 1 is skipped, leaving 1 then 2.

**Example 2**

Input:

```python
remove_duplicates_sorted(head)  # head = 1 -> 1 -> 2 -> 3 -> 3
```

Output:

```text
[1, 2, 3]
```

**Explanation:** The duplicate 1s and 3s are removed so each value appears once in order.

### Constraints

- `0 <= number of nodes <= 100000`
- The list is sorted in increasing order.

## Theory

Because the list is sorted, equal values are next to each other. Stand on a node and look at the next one: if it has the same value, **unlink it** (`cur.next = cur.next.next`) and stay on the same node, since the new next might be a duplicate too; otherwise move forward.

No dummy node is needed here: the first node is always kept, so the head never changes.

This is `O(n)` time and `O(1)` memory. Contrast it with an unsorted list, where you would need a set to remember seen values.

## Explanation

The loop compares `cur` with the node after it. A repeat is cut out; a different value lets `cur` advance.

### Complexity

- Time: O(n), n = number of nodes.
- Extra space: O(1), constant extra space.
- The brute force takes O(n log n), n = number of nodes.
