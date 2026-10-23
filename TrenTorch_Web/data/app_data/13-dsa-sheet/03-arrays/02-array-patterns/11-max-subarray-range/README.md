---
name: sheet-max-subarray-range
title: 'Maximum Subarray With Its Range'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
---

## Statement

Find the contiguous run of `nums` with the **largest sum** and return `[best_sum, start, end]`, where `start` and `end` are the first and last positions of the run (both included).

If several runs share the largest sum, return the one that **starts earliest**, and among those the **shortest**. `nums` is not empty.

### Examples

**Example 1**

Input:

```python
max_subarray_range([-2, 1, -3, 4, -1, 2, 1, -5, 4])
```

Output:

```text
[6, 3, 6]
```

The best run is `[4, -1, 2, 1]` from position 3 to 6 with sum 6.

**Example 2**

Input:

```python
max_subarray_range([-3, -1, -2])
```

Output:

```text
[-1, 1, 1]
```

All values are negative, so the best run is the single `-1` at position 1.

### Constraints

- `1 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`

## Theory

You already know Kadane's algorithm for the best sum. To also report _where_ the best run is, track where the current run started. The rule that makes Kadane work is: **if the running sum before a value is negative, drop it and start a new run at that value**; otherwise extend the run.

Keep `start` (where the current run began) next to the running sum. Whenever the running sum beats the best **strictly**, record the new best together with `start` and the current position as `end`. Using a strict comparison keeps the earliest and shortest run when there are ties, because a later run that only equals the best never replaces it.

Still one pass, still `O(n)`.

## Explanation

`current` is the sum of the run ending at position `i`, and `begin` is where it started. If `current` was negative before adding `nums[i]`, reset it: `current = nums[i]`, `begin = i`; otherwise add. Then `if current > best`, store `[current, begin, i]`.
