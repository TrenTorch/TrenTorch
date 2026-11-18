---
name: sheet-single-number
title: 'The Number That Appears Once'
tags: [dsa-sheet, arrays, array-basics]
difficulty: Beginner
theory: xor-the-cancelling-operator
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

## Explanation

`functools.reduce(operator.xor, nums)` folds `^` over the list. Pairs cancel because `x ^ x = 0`, and the leftover value is unchanged by the zeros.

### Complexity

- Time: O(n). One XOR pass; equal values cancel out.
- Space: O(1). One running XOR.
