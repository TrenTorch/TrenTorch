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

**Explanation:** Numbers 1 and 2 appear twice; 3 and 5 appear once, so the two singles are 3 and 5 sorted ascending.

**Example 2**

Input:

```python
two_single_numbers([-1, 0])
```

Output:

```text
[-1, 0]
```

**Explanation:** Both -1 and 0 appear once, so they are the two singles returned in increasing order.

### Constraints

- `2 <= len(nums) <= 300000`
- `-2**31 <= nums[i] < 2**31`

## Theory

XOR of the whole list cancels the pairs and leaves `a ^ b`, the xor of the two singles. It is not zero, because `a != b`, so it has at least one set bit, and that bit is a position where `a` and `b` **differ**.

Use it to **split the numbers into two groups**: those with that bit set and those without. The pairs stay together (equal numbers have equal bits), and `a` and `b` land in different groups. XOR each group separately: each ends up as one single number.

To get the bit, isolate the lowest set bit of `a ^ b` with `x & -x`. The method takes two passes, `O(n)` time and `O(1)` memory.

## Explanation

`xor_all = a ^ b`. `low = xor_all & -xor_all` is one bit where they differ. Numbers with `low` set xor to one single number and the rest to the other.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line  | Variables                      |
| ---------------- | ------------------------------ |
| `xor_all = 0`    | `xor_all = 0`                  |
| `xor_all ^= x`   | `xor_all = 3, x = 2`           |
| `xor_all ^= x`   | `xor_all = 1, x = 3`           |
| `xor_all ^= x`   | `xor_all = 6, x = 5`           |
| `for x in nums:` | `x = 1, low = 2, a = 0, b = 0` |
| `for x in nums:` | `a = 2, b = 1`                 |
| `for x in nums:` | `x = 2, a = 1, b = 0`          |
| `return`         | `returned = [3, 5]`            |

### Complexity

- Time: O(n) where n is length of nums.
- Extra space: O(1) extra memory.
- The brute force takes O(n) where n is length of nums.
