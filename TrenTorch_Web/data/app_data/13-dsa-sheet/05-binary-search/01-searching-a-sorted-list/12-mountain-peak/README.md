---
name: sheet-mountain-peak
title: 'Peak of a Mountain List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
---

## Statement

`nums` is a **mountain**: its values are all different and strictly increase up to a peak, then strictly decrease (the peak can be the first or the last value, for example `[1, 2, 3]` or `[3, 2, 1]`). Return the **index of the peak**, which is also the position of the largest value.

### Examples

**Example 1**

Input:

```python
mountain_peak([1, 3, 5, 4, 2])
```

Output:

```text
2
```

**Example 2**

Input:

```python
mountain_peak([1, 2, 3])
```

Output:

```text
2
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- Strictly increasing to one peak, then strictly decreasing.
- `0 <= nums[i] <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

Finding the maximum with `max(nums)` reads every value. A mountain has structure you can use: to the **left** of the peak the list is rising, to the **right** it is falling. So comparing a value with its **right neighbour** tells you which side of the peak you are on.

If `nums[mid] < nums[mid + 1]` you are on the rising side, so the peak is to the right: `lo = mid + 1`. Otherwise you are at the peak or on the falling side, so the peak is at `mid` or to its left: `hi = mid`. Each step halves the range: `O(log n)`.

This is binary search on a **condition that changes once** (rising, then not rising), not on a target value. Many real problems have that shape.

## Explanation

`nums[mid] < nums[mid + 1]` means the peak is strictly right of `mid`; otherwise `mid` could be the peak, so keep it with `hi = mid`. The loop ends with `lo == hi` at the peak index. `mid + 1` is always valid inside `while lo < hi`.
