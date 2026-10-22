---
name: sheet-kth-largest
title: 'Kth Largest Value'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
---

## Statement

Return the `k`-th largest value in `nums`, where `k = 1` is the largest. Equal values count separately: in `[5, 5, 3]` the 2nd largest is `5` and the 3rd largest is `3`.

Sorting the whole list works, but you only need one value. See if you can do it faster.

### Examples

**Example 1**

Input:

```python
kth_largest([3, 2, 1, 5, 6, 4], 2)
```

Output:

```text
5
```

Sorted from largest: 6, 5, 4, 3, 2, 1. The 2nd is 5.

**Example 2**

Input:

```python
kth_largest([5, 5, 3], 3)
```

Output:

```text
3
```

Sorted from largest: 5, 5, 3. The 3rd is 3.

### Constraints

- `1 <= k <= len(nums) <= 2 * 10**5`
- `-10**9 <= nums[i] <= 10**9`

## Theory

Sorting finds the `k`-th largest in `O(n log n)`, but it puts _every_ value in order when you want just one. **Quickselect** borrows quicksort's partition step and recurses into only the side that holds the answer, so on average it does `n + n/2 + n/4 + ... = O(n)` work.

Pick a pivot and split the values into smaller, equal and bigger. If `k` falls in the bigger group, continue there. If it falls in the equal group, the pivot is the answer. Otherwise continue in the smaller group with `k` reduced by the sizes you skipped. Splitting into three groups (not two) keeps lists with many equal values fast.

The worst case is `O(n²)` if the pivots are always bad, so real code picks them at random or uses the median-of-medians method. A heap of size `k` (`heapq.nlargest`) is another good choice, at `O(n log k)`.

## Explanation

Convert to an ascending index: the `k`-th largest is at index `len - k` in sorted order. Pick the middle value as pivot and split into `less`, `equal` count, and `greater`. If the target index is inside `less`, loop on `less`. If it is inside the equal block, return the pivot. Otherwise subtract the sizes of `less` and the equal block from the target and loop on `greater`.
