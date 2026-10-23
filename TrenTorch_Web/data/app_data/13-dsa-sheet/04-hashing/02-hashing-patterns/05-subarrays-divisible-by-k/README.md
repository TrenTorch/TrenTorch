---
name: sheet-subarrays-divisible-by-k
title: 'Subarrays Divisible by K'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Advanced
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

## Theory

A run's sum is `prefix[b] - prefix[a]`. That difference is divisible by `k` exactly when the two prefix sums have the **same remainder** modulo `k`. So you only need to count how many earlier prefixes share the current prefix's remainder.

Keep a dictionary (or list of size `k`) counting the remainders seen so far, starting with remainder `0` counted once for the empty prefix. For each new prefix compute `prefix % k`, add `seen[remainder]` to the answer, then record the remainder.

Python's `%` always gives a result in `0..k-1` even for negative numbers (`-1 % 5 == 4`). In languages like C or Java a negative number can give a negative remainder, so you must fix it up there; Python spares you this classic bug.

## Explanation

`seen[r]` counts earlier prefixes with remainder `r`; it starts as `{0: 1}`. Each new prefix remainder `r = prefix % k` forms a divisible run with every earlier prefix of remainder `r`, so add `seen[r]`, then `seen[r] += 1`.
