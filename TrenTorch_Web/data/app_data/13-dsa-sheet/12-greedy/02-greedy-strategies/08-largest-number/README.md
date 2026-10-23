---
name: sheet-largest-number
title: 'Largest Number'
tags: [dsa-sheet, greedy, greedy-strategies]
difficulty: Advanced
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

## Theory

A **greedy** algorithm builds the answer step by step and, at each step, takes the choice that looks best **right now**, without ever going back. It is fast and simple, but it is only correct when the problem has a structure that makes local choices safe. The hard part is the **proof**: show that the greedy choice can always be part of some best answer.

Sorting the numbers by value fails (`30` vs `3`: `330` is bigger than `303`). What matters is which of the two **joined strings** is bigger: put `a` before `b` if `a + b > b + a` (as text). Example: `"3" + "30" = "330"` beats `"30" + "3" = "303"`, so `3` comes first.

This comparison is consistent (it is a proper ordering), so a normal sort with a custom comparison works. In Python use `functools.cmp_to_key`. Join the sorted strings; if the first one is `"0"`, all are zeros: return `"0"`.

The proof that the pairwise rule gives the global best is an exchange argument: if two neighbours are in the wrong order, swapping them makes the number larger.

## Explanation

`key=cmp_to_key(compare)` sorts with `a + b` versus `b + a`. A leading `"0"` after sorting means every number is zero.
