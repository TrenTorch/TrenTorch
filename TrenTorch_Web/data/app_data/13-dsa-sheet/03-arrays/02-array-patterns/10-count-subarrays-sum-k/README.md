---
name: sheet-count-subarrays-sum-k
title: 'Subarrays With Sum K'
tags: [dsa-sheet, arrays, array-patterns]
difficulty: Intermediate
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

## Theory

With negative values you cannot slide a window (the sum is no longer monotonic), so use **prefix sums**. Let `prefix[i]` be the sum of the first `i` values. The run from position `a` up to (not including) position `b` has sum `prefix[b] - prefix[a]`. It equals `k` exactly when `prefix[a] == prefix[b] - k`.

So scan once, keeping a dictionary `seen` that counts how many times each prefix sum has appeared. At each position the number of runs **ending here** that add to `k` is `seen[prefix - k]`: add that to the answer, then record the current prefix. Start with `seen = {0: 1}` for the empty prefix, so runs starting at the very beginning are counted.

One pass, one dictionary: `O(n)` time and memory.

## Explanation

`seen[0] = 1` accounts for the empty prefix. For each value update `prefix`, add `seen[prefix - k]` (runs ending at this value), then increment `seen[prefix]`. The lookup happens **before** recording the current prefix, so a run of length zero is never counted when `k = 0`.
