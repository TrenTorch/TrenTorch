---
name: sheet-two-single-numbers
title: 'Two Single Numbers'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
theory: two-single-numbers
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

## Explanation

`xor_all = a ^ b`. `low = xor_all & -xor_all` is one bit where they differ. Numbers with `low` set xor to one single number and the rest to the other.

### Complexity

- Time: O(n). Two passes: XOR everything, then XOR the two groups split by one differing bit.
- Space: O(1). A few integers.
