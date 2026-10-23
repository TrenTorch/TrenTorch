---
name: sheet-shortest-subarray-with-sum-at-least-k
title: 'Shortest Subarray With Sum at Least K'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Mastery
---

## Statement

Return the **length of the shortest non-empty contiguous subarray** of `nums` whose sum is **at least `k`**, or `-1` if there is none. The numbers can be **negative**, so the usual sliding window does not work.

For `nums = [2, -1, 2]` and `k = 3` the answer is `3`.

The starter code tries every start. It is correct but too slow for long arrays.

### Examples

**Example 1**

Input:

```python
shortest_subarray_sum_k([2, -1, 2], 3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
shortest_subarray_sum_k([1], 2)
```

Output:

```text
-1
```

### Constraints

- `1 <= len(nums) <= 200000`
- `-10**5 <= nums[i] <= 10**5`
- `1 <= k <= 10**9`

## Theory

With **prefix sums** `P` (`P[0] = 0`, `P[i] = nums[0] + ... + nums[i - 1]`), the sum of `nums[a..b-1]` is `P[b] - P[a]`. We want the smallest `b - a` with `P[b] - P[a] >= k`.

Why a sliding window fails: with negative numbers, extending a window can lower the sum, so you cannot grow and shrink greedily. Use a **monotonic deque of indices with increasing prefix sums**:

- For each `b`, while the **front** `a` satisfies `P[b] - P[a] >= k`, record `b - a` and **pop it from the front**: any later `b` would give a longer length with this `a`.
- Before adding `b`, **pop from the back** all indices with `P[back] >= P[b]`: a later `b'` prefers the later and smaller `P[b]` (it is closer and has a smaller subtraction).
- Append `b`.

Every index is added and removed once: `O(n)`.

## Explanation

The deque holds candidate start indices whose prefix sums increase. The front is the best start (smallest prefix) for the current end; it is removed once used because a later end would only make the subarray longer.
