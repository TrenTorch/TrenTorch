---
name: sheet-wiggle-subsequence
title: 'Longest Wiggle Subsequence'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Look at the list as a line chart. A wiggle subsequence picks the **turning points**: peaks and valleys. A long rise (`1, 2, 3, 4`) only needs its two ends: any value in the middle can be skipped without losing a turn.

So the answer is `1 +` the number of times the direction (sign of the difference) **changes**, ignoring equal neighbours. Keep the last non-zero direction; each time a new difference has the **opposite** sign, count one more element.

A dynamic programming solution in `O(n²)` exists (the starter), but this greedy view needs a single pass.

## Explanation

`direction` is the sign of the last counted difference. A difference with the opposite sign is a new turn and extends the wiggle by one.
