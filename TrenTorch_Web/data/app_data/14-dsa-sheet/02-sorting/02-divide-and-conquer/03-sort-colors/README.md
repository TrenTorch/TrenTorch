---
name: sheet-sort-colors
title: 'Sort Zeros, Ones and Twos'
tags: [dsa-sheet, sorting, divide-and-conquer]
difficulty: Intermediate
theory: the-one-pass-code
---

## Statement

A list contains only the values `0`, `1` and `2` (think of three paint colours). Return it sorted in increasing order, without using a general-purpose sort.

A fast solution reads the list **once**. The tests can only check the answer, not how you got it, so the walkthrough after you solve it shows the one-pass idea. Aim for it anyway: it is a classic.

### Examples

**Example 1**

Input:

```python
sort_colors([2, 0, 2, 1, 1, 0])
```

Output:

```text
[0, 0, 1, 1, 2, 2]
```

**Example 2**

Input:

```python
sort_colors([1, 0])
```

Output:

```text
[0, 1]
```

### Constraints

- `0 <= len(nums) <= 3 * 10**5`
- Every `nums[i]` is `0`, `1` or `2`.

## Explanation

The counting version is shortest in Python: `counts = [nums.count(0), nums.count(1), nums.count(2)]` and rebuild with `[0] * c0 + [1] * c1 + [2] * c2`. Each `count` is a fast built-in pass.

The one-pass version: `low = i = 0`, `high = n - 1`. While `i <= high`: if `nums[i] == 0` swap it with `nums[low]` and advance both `low` and `i`; if it is `2` swap it with `nums[high]` and decrease `high` (do not advance `i`, the swapped-in value is not checked yet); if it is `1` just advance `i`.

### Complexity

- Time: O(n). Three counting passes; counting sort beats `n log n` because there are only three values.
- Space: O(n). The output list.
