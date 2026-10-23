---
name: sheet-kth-missing-positive
title: 'Kth Missing Positive Number'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
---

## Statement

`nums` is sorted in increasing order with different positive values. Return the **`k`-th positive whole number that is missing** from `nums` (counting `1, 2, 3, ...` and skipping the numbers in the list).

For example with `nums = [2, 3, 4, 7, 11]` the missing numbers are `1, 5, 6, 8, 9, 10, 12, ...`, so the 5th missing is `9`.

### Examples

**Example 1**

Input:

```python
kth_missing_positive([2, 3, 4, 7, 11], 5)
```

Output:

```text
9
```

**Example 2**

Input:

```python
kth_missing_positive([1, 2, 3, 4], 2)
```

Output:

```text
6
```

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `nums` is sorted in increasing order with different positive values up to `10**9`.
- `1 <= k <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

Counting the missing numbers by walking through the list is `O(n)`. But the list is sorted, so the **number of missing values before index `i`** is easy to compute without looking at anything else: if the list had no gaps, `nums[i]` would equal `i + 1`. So `nums[i] - (i + 1)` is exactly how many positive numbers are missing before `nums[i]`.

That count never decreases as `i` grows, so you can binary search for the first index where the missing count reaches `k`: let `lo` be the number of list values that are **before** the answer. The answer then lies after exactly `lo` list values and `k` missing numbers, so it is `lo + k`.

## Explanation

`nums[mid] - (mid + 1) < k` means fewer than `k` numbers are missing before `nums[mid]`, so the answer is beyond it: `lo = mid + 1`. Otherwise the answer is before `nums[mid]`: `hi = mid`. At the end `lo` list values lie before the answer, so the answer is `lo + k`.
