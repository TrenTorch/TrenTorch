---
name: sheet-mountain-peak
title: 'Peak of a Mountain List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
theory: the-peak-of-a-mountain
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

## Explanation

`nums[mid] < nums[mid + 1]` means the peak is strictly right of `mid`; otherwise `mid` could be the peak, so keep it with `hi = mid`. The loop ends with `lo == hi` at the peak index. `mid + 1` is always valid inside `while lo < hi`.

### Complexity

- Time: O(log n). Comparing a value with its right neighbour tells on which side of the peak it is, so the range halves.
- Space: O(1). Two indices.
