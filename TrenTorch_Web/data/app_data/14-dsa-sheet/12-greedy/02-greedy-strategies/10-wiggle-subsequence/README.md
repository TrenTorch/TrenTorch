---
name: sheet-wiggle-subsequence
title: 'Longest Wiggle Subsequence'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
theory: longest-wiggle
---

## Statement

A **wiggle sequence** has differences between neighbours that **alternate** between positive and negative (a single value, or two different values, also count). Return the **length of the longest wiggle subsequence** of `nums` (a subsequence keeps the order but may skip values).

For `[1, 7, 4, 9, 2, 5]` the answer is `6`; for `[1, 17, 5, 10, 13, 15, 10, 5, 16, 8]` it is `7`.

The starter code compares every value with all earlier ones. It is correct but too slow for long lists.

### Examples

**Example 1**

Input:

```python
wiggle_length([1, 7, 4, 9, 2, 5])
```

Output:

```text
6
```

**Example 2**

Input:

```python
wiggle_length([1, 17, 5, 10, 13, 15, 10, 5, 16, 8])
```

Output:

```text
7
```

### Constraints

- `0 <= len(nums) <= 200000`
- `0 <= nums[i] <= 10**9`

## Explanation

`direction` is the sign of the last counted difference. A difference with the opposite sign is a new turn and extends the wiggle by one.

### Complexity

- Time: O(n). One pass counting the turns of direction.
- Space: O(1). Two numbers.
