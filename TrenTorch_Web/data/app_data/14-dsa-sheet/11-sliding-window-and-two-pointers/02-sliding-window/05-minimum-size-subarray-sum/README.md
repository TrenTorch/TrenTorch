---
name: sheet-minimum-size-subarray-sum
title: 'Smallest Subarray With a Large Sum'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: the-shortest-block-with-a-large-sum
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

## Explanation

The `while` loop shrinks as long as the window is still big enough, recording each smaller valid length. If no window ever reached the target, `best` stays at infinity and `0` is returned.

### Complexity

- Time: O(n). Each index enters and leaves the window once (values are positive).
- Space: O(1). A few numbers.
