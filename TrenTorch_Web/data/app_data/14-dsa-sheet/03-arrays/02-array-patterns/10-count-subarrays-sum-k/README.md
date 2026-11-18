---
name: sheet-count-subarrays-sum-k
title: 'Subarrays With Sum K'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
theory: prefix-sums-and-counting
---

## Statement

Return how many **contiguous runs** of `nums` (subarrays) add up to exactly `k`. Values can be negative or zero. Runs at different positions count separately even if they hold the same values.

The starter code tries every start and end. It is correct but too slow for long lists. Make it fast.

### Examples

**Example 1**

Input:

```python
count_subarrays_sum_k([1, 1, 1], 2)
```

Output:

```text
2
```

The runs are positions 0 to 1 and positions 1 to 2.

**Example 2**

Input:

```python
count_subarrays_sum_k([1, -1, 0], 0)
```

Output:

```text
3
```

The runs `[1, -1]`, `[0]` and `[1, -1, 0]` all add to 0.

### Constraints

- `0 <= len(nums) <= 2 * 10**5`
- `-10**4 <= nums[i] <= 10**4`
- `-10**9 <= k <= 10**9`

## Explanation

`seen[0] = 1` accounts for the empty prefix. For each value update `prefix`, add `seen[prefix - k]` (runs ending at this value), then increment `seen[prefix]`. The lookup happens **before** recording the current prefix, so a run of length zero is never counted when `k = 0`.

### Complexity

- Time: O(n). One pass; a subarray ending here has sum `k` when an earlier prefix equals `prefix - k`, found with one dictionary lookup.
- Space: O(n). The dictionary of prefix sums seen so far.
