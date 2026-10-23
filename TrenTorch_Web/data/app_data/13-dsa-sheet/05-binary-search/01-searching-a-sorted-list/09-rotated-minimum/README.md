---
name: sheet-rotated-minimum
title: 'Minimum of a Rotated List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
---

## Statement

A sorted list with **no repeated values** was rotated by some amount (possibly zero). Return its smallest value.

### Examples

**Example 1**

Input:

```python
rotated_minimum([4, 5, 6, 7, 0, 1, 2])
```

Output:

```text
0
```

**Example 2**

Input:

```python
rotated_minimum([1, 2, 3])
```

Output:

```text
1
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- All values are different.
- `-10**9 <= nums[i] <= 10**9`
- The big tests count how many values your code reads from the list (the limit is stated in the failure message). Reading every value, or using `in`, `.index`, `.count`, `min` or `sorted` on the whole list, fails them.

## Theory

The minimum of a rotated list sits at the **break point** where the list drops from its largest value back to its smallest. Binary search can find that point by comparing the middle value with the **last** value of the range.

If `nums[mid] > nums[hi]`, the drop is somewhere to the right of `mid` (the right part contains the wrap), so `lo = mid + 1`. Otherwise the right part up to `hi` is in order and the minimum is at `mid` or to its left, so `hi = mid`. Comparing with `nums[hi]` (not `nums[lo]`) also handles a list that was not rotated at all.

The loop ends when `lo == hi`: both point at the minimum. `O(log n)` reads.

## Explanation

`while lo < hi`: when the middle is bigger than the last value the minimum is strictly to the right, otherwise it is at `mid` or earlier, so `mid` stays a candidate. At the end `nums[lo]` is the minimum.
