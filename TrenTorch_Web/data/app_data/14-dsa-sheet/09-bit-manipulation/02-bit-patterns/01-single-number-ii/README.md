---
name: sheet-single-number-ii
title: 'Single Number, Others Three Times'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
theory: everything-else-appears-three-times
---

## Statement

Every value in `nums` appears **exactly three times**, except one value that appears **once**. Return that value. Use `O(1)` extra memory if you can (counting with a dictionary is allowed, but the challenge is to do it without one).

### Examples

**Example 1**

Input:

```python
single_number_ii([2, 2, 3, 2])
```

Output:

```text
3
```

**Example 2**

Input:

```python
single_number_ii([0, 1, 0, 1, 0, 1, 99])
```

Output:

```text
99
```

### Constraints

- `1 <= len(nums) <= 300000`
- `len(nums) % 3 == 1`
- `-2**31 <= nums[i] < 2**31`

## Explanation

For each bit, the number of times it is seen is a multiple of 3 for the tripled values, so only the single number's bits are left in `ones` after every value is processed.

### Complexity

- Time: O(n). One pass; two bit-masks count every bit position modulo 3.
- Space: O(1). Two integers.
