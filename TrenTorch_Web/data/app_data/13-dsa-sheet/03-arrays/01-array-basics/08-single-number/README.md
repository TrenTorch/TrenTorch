---
name: sheet-single-number
title: 'The Number That Appears Once'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
---

## Statement

Every value in `nums` appears **exactly twice**, except for one value that appears **once**. Return that value.

### Examples

**Example 1**

Input:

```python
single_number([4, 1, 2, 1, 2])
```

Output:

```text
4
```

**Example 2**

Input:

```python
single_number([7])
```

Output:

```text
7
```

### Constraints

- `1 <= len(nums) <= 2 * 10**5 + 1`, and the length is odd
- `0 <= nums[i] <= 10**5`

## Theory

Counting with a dictionary works in `O(n)` but uses `O(n)` memory. There is a neat trick with **XOR** (`^`), which compares bits and gives `1` where they differ.

Two facts: `x ^ x = 0` (a value cancels itself) and `x ^ 0 = x`. XOR is also order-independent. So XOR every value together: each pair cancels to `0`, and only the single value is left.

The result needs one integer of memory and one pass: `O(n)` time, `O(1)` space. It is the first example of using **bit manipulation** to solve a counting problem.

## Explanation

`functools.reduce(operator.xor, nums)` folds `^` over the list. Pairs cancel because `x ^ x = 0`, and the leftover value is unchanged by the zeros.
