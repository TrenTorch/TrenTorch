---
name: sheet-missing-number
title: 'Find the Missing Number'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
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

## Theory

Searching for each candidate (`v in nums`) is `O(n²)`. There are two classic `O(n)` tricks, both with no extra memory.

**Sum.** The numbers `0..n` add up to `n(n+1)/2`. The list adds up to that minus the missing value, so `n(n+1)/2 - sum(nums)` is the answer.

**XOR.** `x ^ x = 0` and `x ^ 0 = x`. XOR together every index `0..n` and every value in `nums`. Every present number appears twice and cancels, leaving the missing one. XOR cannot overflow in languages with fixed-size integers, which is why it is popular in C and Java.

## Explanation

`len(nums)` is `n`. The full range sums to `n * (n + 1) // 2`. Subtract the actual `sum(nums)` and the difference is the missing number. Python integers do not overflow, so the sum is safe for any size.
