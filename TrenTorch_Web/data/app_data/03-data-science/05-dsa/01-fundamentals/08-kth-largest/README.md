---
name: dsa-kth-largest
title: 'Kth Largest Element'
tags: [dsa]
difficulty: Intermediate
---

## Statement

### The problem

Given a list `nums` of integers and an integer `k`, return the `k`-th largest element of `nums`. This is the k-th largest in sorted order, not the k-th distinct value, so duplicates count separately: in `[3, 2, 3, 1, 2, 4, 5, 5, 6]` the 4th largest is `4`.

Implement `solve(nums, k)`. The signature and docstring are already in the editor.

### Examples

`solve([3, 2, 1, 5, 6, 4], 2)` returns `5`.

`solve([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)` returns `4`.

### Constraints

- `1 <= k <= len(nums)`.
- `nums` may contain duplicates and negative numbers.
- Aim for O(n log k) time, which is better than sorting the whole list when `k` is small.

### Hints

<details>
<summary>Hint 1</summary>

Sorting works but does more than you need. You only care about the `k` biggest values.

</details>

<details>
<summary>Hint 2</summary>

Keep a min-heap that never holds more than `k` numbers. When it grows past `k`, pop the smallest. After one pass, the smallest value left in the heap is the k-th largest.

</details>

## Theory

### The simple version

Picture a podium with `k` places. Each number walks up and, if it beats the weakest person on the podium, takes their place. At the end, the weakest person on the podium is the k-th best overall.

### Key principles

- A min-heap of size `k` keeps the `k` largest values seen so far, with the smallest of them on top.
- Each push or pop costs O(log k), so one pass over `n` numbers is O(n log k) time and O(k) space.
- QuickSelect finds the answer in O(n) time on average by partitioning around a pivot, but O(n^2) in the worst case.
- Edge cases: `k = 1` (the maximum), `k = len(nums)` (the minimum), duplicates, negatives.

## Explanation

The solution pushes every number onto a min-heap and pops whenever the heap grows past `k` items. The heap then holds the `k` largest numbers, and its root, the smallest of them, is the k-th largest.
