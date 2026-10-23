---
name: sheet-two-single-numbers
title: 'Two Single Numbers'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
---

## Statement

Every value in `nums` appears **twice**, except **two different values** that appear once each. Return those two values in increasing order. Use `O(1)` extra memory if you can.

### Examples

**Example 1**

Input:

```python
two_single_numbers([1, 2, 1, 3, 2, 5])
```

Output:

```text
[3, 5]
```

**Example 2**

Input:

```python
two_single_numbers([-1, 0])
```

Output:

```text
[-1, 0]
```

### Constraints

- `2 <= len(nums) <= 300000`
- `-2**31 <= nums[i] < 2**31`

## Theory

XOR of the whole list cancels the pairs and leaves `a ^ b`, the xor of the two singles. It is not zero, because `a != b`, so it has at least one set bit, and that bit is a position where `a` and `b` **differ**.

Use it to **split the numbers into two groups**: those with that bit set and those without. The pairs stay together (equal numbers have equal bits), and `a` and `b` land in different groups. XOR each group separately: each ends up as one single number.

To get the bit, isolate the lowest set bit of `a ^ b` with `x & -x`. The method takes two passes, `O(n)` time and `O(1)` memory.

## Explanation

`xor_all = a ^ b`. `low = xor_all & -xor_all` is one bit where they differ. Numbers with `low` set xor to one single number and the rest to the other.
