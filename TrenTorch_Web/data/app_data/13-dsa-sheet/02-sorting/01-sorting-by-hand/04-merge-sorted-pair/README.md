---
name: sheet-merge-sorted-pair
title: 'Merge Two Sorted Lists'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
---

## Statement

You get two lists `a` and `b`, each sorted in increasing order. Merge them with the standard two-pointer method:

1. Keep a position in each list, both starting at `0`.
2. While both lists still have values left, **compare** the two current values. Take the smaller one into the result and move that list's position forward. If they are equal, take the one from `a`.
3. When one list runs out, add everything left in the other list **without comparing**.

Return a list of two things: `[merged, comparisons]`, where `merged` is the combined sorted list and `comparisons` is how many comparisons step 2 made.

### Examples

**Example 1**

Input:

```python
merge_sorted_pair([1, 4, 7], [2, 3, 9])
```

Output:

```text
[[1, 2, 3, 4, 7, 9], 5]
```

Comparisons: 1v2, 4v2, 4v3, 4v9, 7v9. Then `9` is left over and added without a comparison.

**Example 2**

Input:

```python
merge_sorted_pair([], [5, 6])
```

Output:

```text
[[5, 6], 0]
```

`a` is empty, so no comparisons are made.

### Constraints

- `0 <= len(a), len(b) <= 3 * 10**5`
- Both lists are sorted in increasing order.
- `-10**9 <= value <= 10**9`

## Theory

Merging is the building block of **merge sort**. Because both inputs are already sorted, the next smallest value overall must be at the front of one of them, so one comparison decides each output value. No looking back is ever needed.

Merging lists of total length `n` costs at most `n - 1` comparisons and `O(n)` time. That is far cheaper than sorting the combined list from scratch, which is the whole point.

Taking from `a` on ties keeps the merge **stable**: equal values stay in the order they came in. Stability matters when you sort records by one field and want earlier orderings kept.

## Explanation

Two indexes `i` and `j` walk the lists. While both are in range, count one comparison and append the smaller value (using `<=` so ties come from `a`). After the loop, `a[i:]` and `b[j:]` are sorted and at most one of them is non-empty, so extend the result with both.
