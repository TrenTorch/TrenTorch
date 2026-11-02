---
name: dsa-binary-search
title: 'Binary Search'
tags: [dsa]
difficulty: Intermediate
---

## Statement

### The problem

Given a list `arr` of integers sorted in ascending order and an integer `target`, return the index of `target` in `arr`, or `-1` if it is not there. Your solution must run in O(log n) time, so scanning the list one element at a time will not do.

Implement `solve(arr, target)`. The signature and docstring are already in the editor.

### Constraints

- `arr` is sorted ascending and has no duplicates; it may be empty.
- `target` may be smaller or larger than every element.

### Hints

<details>
<summary>Hint 1</summary>

Keep two indices, `lo` and `hi`, that bound the part of the list that could still hold `target`. Look at the middle element each round.

</details>

<details>
<summary>Hint 2</summary>

If the middle element is too small, `target` can only be to its right, so move `lo` past it. If it is too big, move `hi` before it. Stop when `lo > hi`.

</details>

## Theory

### The simple version

Looking up a word in a dictionary, you open it near the middle, see whether your word comes before or after that page, and throw away the half that cannot contain it. Repeat, and a thousand pages take about ten looks. Binary search does exactly this on a sorted list.

### Key principles

- Each comparison halves the remaining range, so the search takes O(log n) time and O(1) extra space.
- It only works because the list is sorted: the middle element tells you which half to discard.
- Edge cases: empty list, one element, target below the first or above the last element.
- Loop invariant: if `target` is in `arr`, its index is always in `[lo, hi]`.

## Explanation

The solution keeps `lo` and `hi` as the inclusive bounds of the search range. Each round it compares `arr[mid]` with `target`: equal returns `mid`, smaller moves `lo` to `mid + 1`, larger moves `hi` to `mid - 1`. When `lo` passes `hi` the range is empty and the target is not present, so it returns `-1`.
