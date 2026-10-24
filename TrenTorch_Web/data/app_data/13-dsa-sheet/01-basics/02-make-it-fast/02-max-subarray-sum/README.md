---
name: sheet-max-subarray-sum
title: 'Maximum Subarray Sum'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
---

## Statement

Given a non-empty list of integers `nums`, return the largest sum of a **contiguous** run of one or more elements (a subarray).

The starter code tries every start and end. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
```

Output:

```text
6
```

The best run is `[4, -1, 2, 1]` with sum 6.

**Example 2**

Input:

```python
max_subarray_sum([-3, -1, -2])
```

Output:

```text
-1
```

All values are negative, so the best run is the single element `-1`.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`
- The subarray must contain at least one element.

## Theory

Trying every start and every end is `O(n²)`. For a list of 200,000 numbers that is about `2 * 10¹⁰` additions.

There is a one-pass idea (Kadane's algorithm). Track the best sum of a subarray _ending at the current position_. At each element you either extend the previous best run or start fresh from this element, whichever is larger: `cur = max(x, cur + x)`. A negative running total can never help a later element, so it is dropped. The answer is the largest `cur` seen. That is `O(n)` time and `O(1)` memory.

## Explanation

`cur` is the best sum of a subarray that ends at the current element. Extending is `cur + x`; starting fresh is `x`. Take the larger, and keep the overall maximum in `best`.

Start from the first element (not `0`), so a list of all negative numbers returns its largest single element and not `0`.
