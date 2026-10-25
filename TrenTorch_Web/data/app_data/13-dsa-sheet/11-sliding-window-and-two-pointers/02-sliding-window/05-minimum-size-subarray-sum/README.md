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

**Explanation:** The subarray [4, 3] sums to 7, which is the target, and it is the shortest such subarray.

**Example 2**

Input:

```python
min_subarray_len(4, [1, 4, 4])
```

Output:

```text
1
```

**Explanation:** The subarray [4] sums to 4, which is the target, and it is the shortest such subarray.

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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line        | Variables                               |
| ---------------------- | --------------------------------------- |
| `best = len(nums) + 1` | `best = 7`                              |
| `total += x`           | `total = 2, left = 0, right = 0, x = 2` |
| `total += x`           | `total = 6, right = 2, x = 1`           |
| `total -= nums[left]`  | `best = 4, right = 3, x = 2`            |
| `total -= nums[left]`  | `total = 7, left = 1, right = 4, x = 4` |
| `left += 1`            | `best = 3, total = 6, left = 3`         |
| `left += 1`            | `total = 7, left = 4, right = 5, x = 3` |
| `return`               | `returned = 2`                          |

### Complexity

- Time: O(n), where n is the length of nums.
- Extra space: O(1), no extra memory.
- The brute force takes O(n^2), where n is the length of nums.
