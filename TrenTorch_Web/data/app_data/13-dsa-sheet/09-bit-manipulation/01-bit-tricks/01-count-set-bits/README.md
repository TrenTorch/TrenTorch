---
name: sheet-count-set-bits
title: 'Count the Set Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
---

## Statement

Return how many bits of `n` are `1` when `n` is written in binary. For `n = 13` (binary `1101`) the answer is `3`.

### Examples

**Example 1**

Input:

```python
count_set_bits(13)
```

Output:

```text
3
```

**Explanation:** The binary representation of 13 is 1101, which contains three 1s.

**Example 2**

Input:

```python
count_set_bits(0)
```

Output:

```text
0
```

**Explanation:** The binary representation of 0 is 0, which contains zero 1s.

### Constraints

- `0 <= n < 2**62`

## Theory

Numbers are stored as bits (0s and 1s). Python lets you work on those bits directly: `&` (and), `|` (or), `^` (xor), `~` (not), `<<` and `>>` (shift).

The easy way is to test each bit: `n & 1` is the lowest bit, then shift `n >> 1` and repeat (62 steps at most). Python also has `bin(n).count("1")` and, in 3.10+, `n.bit_count()`.

A clever way is **Brian Kernighan's trick**: `n & (n - 1)` clears the **lowest set bit** of `n`. Subtracting 1 turns the lowest `1` into `0` and all the `0`s below it into `1`s, so the `&` wipes exactly that bit. Repeat until `n` is `0`; the number of repeats is the number of set bits. It loops once per `1`, not once per bit.

## Explanation

Each loop round removes one `1` bit with `n &= n - 1`, so the loop runs exactly as many times as there are set bits.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line | Variables      |
| --------------- | -------------- |
| `count = 0`     | `count = 0`    |
| `n &= n - 1`    | `n = 12`       |
| `count += 1`    | `count = 1`    |
| `n &= n - 1`    | `n = 8`        |
| `count += 1`    | `count = 2`    |
| `n &= n - 1`    | `n = 0`        |
| `count += 1`    | `count = 3`    |
| `return`        | `returned = 3` |

### Complexity

- Time: O(k), where k is the number of set bits in n.
- Extra space: O(1), using a constant amount of extra memory.
- The brute force takes O(log n), where n is the input integer.
