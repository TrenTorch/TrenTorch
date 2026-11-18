---
name: sheet-missing-number
title: 'Find the Missing Number'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: using-a-formula-for-the-total
---

## Statement

`nums` holds `n` **different** numbers taken from `0, 1, ..., n`. Exactly one number from that range is missing. Return it.

### Examples

**Example 1**

Input:

```python
missing_number([3, 0, 1])
```

Output:

```text
2
```

The numbers are from 0 to 3 and `2` is missing.

**Example 2**

Input:

```python
missing_number([0])
```

Output:

```text
1
```

The numbers are from 0 to 1 and `1` is missing.

### Constraints

- `1 <= len(nums) <= 3 * 10**5`
- All values are different and lie between `0` and `len(nums)`.

## Explanation

`len(nums)` is `n`. The full range sums to `n * (n + 1) // 2`. Subtract the actual `sum(nums)` and the difference is the missing number. Python integers do not overflow, so the sum is safe for any size.

### Complexity

- Time: O(n). One `sum` pass; the expected sum comes from a formula.
- Space: O(1). A single integer.
