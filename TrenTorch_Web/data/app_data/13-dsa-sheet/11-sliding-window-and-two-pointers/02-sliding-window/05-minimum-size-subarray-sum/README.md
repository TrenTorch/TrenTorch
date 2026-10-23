---
name: sheet-minimum-size-subarray-sum
title: 'Smallest Subarray With a Large Sum'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
---

## Statement

`nums` contains **positive** whole numbers. Return the **length of the shortest contiguous subarray** whose sum is **at least `target`**, or `0` if there is none.

For `target = 7` and `nums = [2, 3, 1, 2, 4, 3]` the answer is `2` (`[4, 3]`).

The starter code tries every start. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
min_subarray_len(7, [2, 3, 1, 2, 4, 3])
```

Output:

```text
2
```

**Example 2**

Input:

```python
min_subarray_len(4, [1, 4, 4])
```

Output:

```text
1
```

### Constraints

- `0 <= len(nums) <= 200000`
- `1 <= nums[i] <= 10**4`
- `1 <= target <= 10**9`

## Theory

A **sliding window** is a range `[left, right]` of the data that grows on the right and shrinks on the left. Because each end only moves forward, the whole pass is `O(n)`, while the window always describes one candidate subarray or substring.

Because all numbers are **positive**, adding numbers only increases the sum and removing them only decreases it, so a window can be grown and shrunk greedily. Expand `right` and add `nums[right]` to the sum. While the sum is `>= target`, the window is valid: record its length and **shrink from the left** (subtract `nums[left]`, advance `left`) to look for something shorter.

Each index enters and leaves the window once: `O(n)`. With negative numbers this stops working (you saw the deque version in the queues topic).

## Explanation

The `while` loop shrinks as long as the window is still big enough, recording each smaller valid length. If no window ever reached the target, `best` stays at infinity and `0` is returned.
