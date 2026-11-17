---
name: sheet-max-consecutive-ones-iii
title: 'Longest Run of Ones After K Flips'
tags: [dsa-sheet, sliding-window, sliding-window]
difficulty: Intermediate
theory: flipping-zeros
---

## Statement

`nums` contains only `0`s and `1`s. You may flip **at most `k` zeros** to ones. Return the length of the **longest run of ones** you can get.

For `nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]` and `k = 2` the answer is `6`.

### Examples

**Example 1**

Input:

```python
longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2)
```

Output:

```text
6
```

**Example 2**

Input:

```python
longest_ones([0, 0, 1, 1, 1], 0)
```

Output:

```text
3
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= k <= len(nums)`

## Explanation

`zeros` is the number of zeros in the window. Moving `left` past a zero reduces it.

### Complexity

- Time: O(n). Each index enters and leaves the window once.
- Space: O(1). A few numbers.
