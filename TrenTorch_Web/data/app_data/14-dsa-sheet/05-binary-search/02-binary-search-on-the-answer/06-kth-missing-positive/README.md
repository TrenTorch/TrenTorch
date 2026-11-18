---
name: sheet-kth-missing-positive
title: 'Kth Missing Positive Number'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Advanced
theory: counting-the-missing-numbers
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

## Explanation

`nums[mid] - (mid + 1) < k` means fewer than `k` numbers are missing before `nums[mid]`, so the answer is beyond it: `lo = mid + 1`. Otherwise the answer is before `nums[mid]`: `hi = mid`. At the end `lo` list values lie before the answer, so the answer is `lo + k`.

### Complexity

- Time: O(log n). `nums[i] - (i + 1)` is the count of missing numbers before index `i` and never decreases, so binary search finds where the `k`-th missing number sits.
- Space: O(1). Two indices.
