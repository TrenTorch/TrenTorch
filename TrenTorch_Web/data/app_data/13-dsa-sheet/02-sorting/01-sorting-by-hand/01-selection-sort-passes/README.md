---
name: sheet-selection-sort-passes
title: 'Selection Sort, Pass by Pass'
tags: [dsa-sheet, sorting, sorting-by-hand]
difficulty: Beginner
---

## Statement

**Selection sort** builds the sorted part of a list from the left. On pass `i` it finds the smallest value in `nums[i:]`, swaps it into position `i`, and moves on.

Run selection sort on `nums` and return the list as it looks **after every pass**, in order. There is one pass for each position except the last, so a list of length `n` gives `n - 1` snapshots. A list with fewer than two items gives `[]`.

Two rules make the answer exact:

- If the smallest value appears more than once, take the leftmost one.
- Always swap, even when the smallest value is already at position `i`. Record the snapshot either way.

Do not change `nums`.

### Examples

**Example 1**

Input:

```python
selection_sort_passes([64, 25, 12, 22, 11])
```

Output:

```text
[[11, 25, 12, 22, 64], [11, 12, 25, 22, 64], [11, 12, 22, 25, 64], [11, 12, 22, 25, 64]]
```

After pass 0 the smallest value, 11, is first. The last pass swaps 25 with itself.

**Example 2**

Input:

```python
selection_sort_passes([3, 1, 3, 1])
```

Output:

```text
[[1, 3, 3, 1], [1, 1, 3, 3], [1, 1, 3, 3]]
```

Pass 0 takes the leftmost 1 (index 1). Pass 1 takes the other 1. Pass 2 swaps 3 with itself.

### Constraints

- `0 <= len(nums) <= 300`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Selection sort repeats one idea: _the next smallest value belongs at the front of the unsorted part_. After pass `i` the first `i + 1` positions hold the `i + 1` smallest values in their final places.

Finding the smallest of `m` items takes `m - 1` comparisons, so the passes cost `(n-1) + (n-2) + ... + 1 = n(n-1)/2` comparisons. That is `O(n²)` no matter how the input looks, even if it is already sorted. It never does more than `n - 1` swaps, which is why it is used when writing to memory is expensive.

It is not **stable**: swapping the minimum across the list can jump an equal value over another one and change their original order.

## Explanation

Copy the list so the input is untouched. For each `i` from `0` to `n - 2`, scan `i + 1 .. n - 1` for the index of the smallest value, using `<` so the leftmost smallest wins. Swap it into place and append a copy of the list to the result.

Appending `list(a)` and not `a` matters: otherwise every snapshot would be the same list object and show only the final state.
