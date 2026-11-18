---
name: sheet-subarrays-divisible-by-k
title: 'Subarrays Divisible by K'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Advanced
theory: remainders-instead-of-sums
---

## Statement

Return how many **contiguous runs** of `nums` have a sum that is divisible by `k` (the sum can be `0`, and it can be negative). Runs at different positions count separately.

The starter code tries every start and end. It is correct but too slow. Make it fast.

### Examples

**Example 1**

Input:

```python
subarrays_divisible_by_k([4, 5, 0, -2, -3, 1], 5)
```

Output:

```text
7
```

Seven runs have a sum divisible by 5.

**Example 2**

Input:

```python
subarrays_divisible_by_k([5], 9)
```

Output:

```text
0
```

The only run has sum 5, not divisible by 9.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`
- `1 <= k <= 10**4`

## Explanation

`seen[r]` counts earlier prefixes with remainder `r`; it starts as `{0: 1}`. Each new prefix remainder `r = prefix % k` forms a divisible run with every earlier prefix of remainder `r`, so add `seen[r]`, then `seen[r] += 1`.

### Complexity

- Time: O(n). One pass; two prefixes with the same remainder bound a divisible subarray.
- Space: O(min(n, k)). The dictionary has at most one entry per remainder.
