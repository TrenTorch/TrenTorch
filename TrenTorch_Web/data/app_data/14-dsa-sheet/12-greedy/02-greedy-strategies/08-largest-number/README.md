---
name: sheet-largest-number
title: 'Largest Number'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
theory: largest-number-from-a-list
---

## Statement

Arrange the numbers in `nums` in some order and join them into one number written as a string. Return the **largest** one. Because the result can be huge, return it as a string. If all numbers are zero, return `"0"`.

For `[3, 30, 34, 5, 9]` the answer is `"9534330"`.

### Examples

**Example 1**

Input:

```python
largest_number([10, 2])
```

Output:

```text
'210'
```

**Example 2**

Input:

```python
largest_number([3, 30, 34, 5, 9])
```

Output:

```text
'9534330'
```

### Constraints

- `0 <= len(nums) <= 30000`
- `0 <= nums[i] <= 10**9`

## Explanation

`key=cmp_to_key(compare)` sorts with `a + b` versus `b + a`. A leading `"0"` after sorting means every number is zero.

### Complexity

- Time: O(n * d * log n). Sorting with the rule "`a + b` before `b + a`" costs `n log n` comparisons of strings of up to `d` digits.
- Space: O(n * d). The strings.
