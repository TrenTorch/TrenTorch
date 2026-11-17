---
name: sheet-rotated-minimum
title: 'Minimum of a Rotated List'
tags: [dsa-sheet, binary-search, searching-a-sorted-list]
difficulty: Intermediate
theory: finding-the-smallest-value
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

## Explanation

`while lo < hi`: when the middle is bigger than the last value the minimum is strictly to the right, otherwise it is at `mid` or earlier, so `mid` stays a candidate. At the end `nums[lo]` is the minimum.

### Complexity

- Time: O(log n). Comparing the middle with the last value shows which half holds the minimum.
- Space: O(1). Two indices.
