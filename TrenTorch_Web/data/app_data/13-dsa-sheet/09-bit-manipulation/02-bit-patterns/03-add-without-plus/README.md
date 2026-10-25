---
name: sheet-add-without-plus
title: 'Add Without the Plus Sign'
tags: [dsa-sheet, bit-manipulation, bit-patterns]
difficulty: Advanced
---

## Statement

Return `a + b` **without using `+` or `-`**, only bit operations. The numbers are 32-bit signed integers; if the true sum does not fit in 32 bits, the answer **wraps around** like a 32-bit register: the result is the sum reduced to the range `-2**31 .. 2**31 - 1`.

### Examples

**Example 1**

Input:

```python
bit_add(1, 2)
```

Output:

```text
3
```

**Explanation:** 1 and 2 have no overlapping set bits, so XOR gives 3 and carry becomes 0 immediately.

**Example 2**

Input:

```python
bit_add(-2, 3)
```

Output:

```text
1
```

**Explanation:** -2 is 0xFFFFFFFE in 32-bit two's complement; adding 3 yields 1 after carry propagation and sign correction.

### Constraints

- `-2**31 <= a, b < 2**31`

## Theory

This is how a computer adds. Adding two bits gives a **sum bit** (`x ^ y`, no carry) and a **carry bit** (`x & y`, which belongs one position to the left, so `(x & y) << 1`).

So `a + b = (a ^ b) + ((a & b) << 1)`: the sum without carries, plus the carries. That is still an addition, so **repeat**: put `a ^ b` into `a` and the carries into `b`, until there are no carries (`b == 0`). The loop ends because carries shift left and eventually leave the 32 bits.

Python integers have no fixed width, so negative numbers would carry forever. Keep everything in 32 bits with a mask `0xFFFFFFFF`, and at the end convert back to signed: a result above `2**31 - 1` means a negative number, which is `result - 2**32`.

## Explanation

`a ^ b` adds without carry; `(a & b) << 1` is the carry. With the mask, values stay in 0..2**32-1, and the final test restores the sign.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                | Variables           |
| ---------------------------------------------- | ------------------- |
| `mask = 0xFFFFFFFF`                            | `mask = 4294967295` |
| `a, b = (a ^ b) & mask, ((a & b) << 1) & mask` | `a = 3, b = 0`      |
| `return`                                       | `returned = 3`      |

### Complexity

- Time: O(1) constant time for 32-bit integers.
- Extra space: O(1) constant extra space.
- The brute force takes O(1) constant time using modulo arithmetic.
