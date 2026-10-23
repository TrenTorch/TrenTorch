---
name: sheet-second-largest
title: 'Second Largest Value'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

Return the **second largest different value** in `nums`. Equal values count once, so in `[7, 7, 5]` the second largest is `5`. If there are fewer than two different values, return `-1`.

### Examples

**Example 1**

Input:

```python
second_largest([4, 9, 9, 6])
```

Output:

```text
6
```

The largest is 9, the second largest different value is 6.

**Example 2**

Input:

```python
second_largest([5, 5, 5])
```

Output:

```text
-1
```

Only one different value, so the answer is `-1`.

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- `0 <= nums[i] <= 10**9`

## Theory

Sorting the list finds the answer but costs `O(n log n)`. You can do it in one pass with two variables: the largest value so far and the second largest so far.

For each value `x`: if `x` beats the largest, the old largest becomes the second. Otherwise, if `x` is smaller than the largest but beats the second, it becomes the new second. A value equal to the largest changes nothing, which is how duplicates are skipped.

Keeping a few running values and updating them as you scan is the simplest kind of **single-pass** array algorithm: `O(n)` time, `O(1)` extra memory.

## Explanation

`largest` and `second` start as `None`. The branch `x > largest` shifts the old largest down. The branch `x < largest and (second is None or x > second)` updates the second. A value equal to `largest` matches neither branch, so duplicates of the maximum never become the second.

Because all values are at least `0`, the result `-1` can only mean "no second value".
