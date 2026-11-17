---
name: sheet-smallest-divisor
title: 'Smallest Divisor Within a Threshold'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
theory: same-pattern-new-stories
---

## Statement

Choose a positive whole number `d`. Divide every value of `nums` by `d`, **round each result up** to the next whole number, and add them. Return the **smallest `d`** for which that sum is at most `threshold`.

### Examples

**Example 1**

Input:

```python
smallest_divisor([1, 2, 5, 9], 6)
```

Output:

```text
5
```

`d = 5` gives 1 + 1 + 1 + 2 = 5, which is within 6, and `d = 4` gives 1 + 1 + 2 + 3 = 7.

**Example 2**

Input:

```python
smallest_divisor([44, 22, 33, 11, 1], 5)
```

Output:

```text
44
```

Five values need threshold 5, so `d` must be the biggest value, 44.

### Constraints

- `1 <= len(nums) <= 2 * 10**4`
- `len(nums) <= threshold <= 10**9`
- `1 <= nums[i] <= 10**6`
- Trying every divisor one by one is too slow for the large tests.

## Explanation

`lo = 1`, `hi = max(nums)`. If the rounded-up sum for `mid` is within the threshold, `mid` works and a smaller one might: `hi = mid`. Otherwise `lo = mid + 1`. The search ends at the smallest valid divisor.

### Complexity

- Time: O(n log M). Binary search over divisors `1..M` (`M` = largest value) costs `log M` probes, and each probe sums `n` ceilings.
- Space: O(1). Two bounds and a running sum.
