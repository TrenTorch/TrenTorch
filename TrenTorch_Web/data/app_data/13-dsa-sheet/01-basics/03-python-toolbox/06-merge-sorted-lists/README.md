---
name: sheet-merge-sorted-lists
title: 'Merge Sorted Lists'
tags: [dsa-sheet, basics, python-toolbox]
difficulty: Intermediate
---

## Statement

You are given a list of lists, and each inner list is already sorted in increasing order. Return one list with all the numbers, sorted in increasing order.

### Examples

**Example 1**

Input:

```python
merge_sorted_lists([[1, 4, 7], [2, 5], [3, 6, 9]])
```

Output:

```text
[1, 2, 3, 4, 5, 6, 7, 9]
```

**Example 2**

Input:

```python
merge_sorted_lists([[], [1], []])
```

Output:

```text
[1]
```

### Constraints

- `0 <= len(lists) <= 100`
- The total number of values is at most `5 * 10**5`.
- Inner lists can be empty.

## Theory

Because every list is already sorted, the next smallest value overall must be at the front of one of the lists. A **heap** of "the current front of each list" gives you that minimum quickly: pop it, then push the next value from the same list. With `k` lists and `n` values in total this is `O(n log k)`.

`heapq.merge(*lists)` does exactly this lazily, one value at a time, using almost no extra memory. Plain `sorted(sum(lists, []))` also works here because Python's sort detects existing sorted runs, but it needs to build the full combined list first.

## Explanation

`heapq.merge(*lists)` returns an iterator over the merged values in order. Wrap it in `list(...)`.

`*lists` unpacks the list of lists into separate arguments. An empty `lists` gives an empty result.
