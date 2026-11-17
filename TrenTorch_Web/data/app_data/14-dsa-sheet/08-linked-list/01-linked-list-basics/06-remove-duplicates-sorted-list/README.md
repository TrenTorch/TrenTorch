---
name: sheet-remove-duplicates-sorted-list
title: 'Remove Duplicates From a Sorted List'
tags: [dsa-sheet, linked-list, linked-list-basics]
difficulty: Beginner
theory: sorted-lists-and-duplicates
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

**Example 2**

Input:

```python
remove_duplicates_sorted(head)  # head = 1 -> 1 -> 2 -> 3 -> 3
```

Output:

```text
[1, 2, 3]
```

### Constraints

- `0 <= number of nodes <= 100000`
- The list is sorted in increasing order.

## Explanation

The loop compares `cur` with the node after it. A repeat is cut out; a different value lets `cur` advance.

### Complexity

- Time: O(n). One pass; equal neighbours are skipped by relinking.
- Space: O(1). One pointer.
