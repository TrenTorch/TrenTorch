---
name: sheet-shortest-subarray-with-sum-at-least-k
title: 'Shortest Subarray With Sum at Least K'
tags: [dsa-sheet, stack-and-queue, queues-and-deques]
difficulty: Mastery
theory: negative-numbers-and-prefix-sums
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

## Explanation

The deque holds candidate start indices whose prefix sums increase. The front is the best start (smallest prefix) for the current end; it is removed once used because a later end would only make the subarray longer.

### Complexity

- Time: O(n). Each prefix index enters and leaves the deque at most once.
- Space: O(n). The prefix sums and the deque.
