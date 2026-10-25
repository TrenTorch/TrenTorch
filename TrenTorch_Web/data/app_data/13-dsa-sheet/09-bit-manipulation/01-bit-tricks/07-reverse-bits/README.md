---
name: sheet-reverse-bits
title: 'Reverse the Bits'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Intermediate
---

## Statement

Treat `n` as a **32-bit** unsigned number, reverse the order of its 32 bits and return the new number. For `n = 1` (31 zeros and then a `1`) the answer is `2147483648` (a `1` and then 31 zeros).

### Examples

**Example 1**

Input:

```python
reverse_bits(1)
```

Output:

```text
2147483648
```

**Explanation:** The 32-bit representation of 1 has a single 1 in the least significant position; reversing moves it to the most significant position, giving 2^31 = 2147483648.

`1` becomes `1` followed by 31 zeros.

**Example 2**

Input:

```python
reverse_bits(43261596)
```

Output:

```text
964176192
```

**Explanation:** The 32-bit binary of 43261596 is reversed bitwise to produce 964176192.

### Constraints

- `0 <= n < 2**32`

## Theory

Build the answer bit by bit: take the lowest bit of `n` (`n & 1`), push it into the **result from the right** (`result = (result << 1) | bit`), then shift `n` right. After 32 rounds the first bit read has moved all the way to the top.

Always do all 32 rounds, even when `n` runs out of bits: leading zeros of `n` become trailing zeros of the answer, and the shifts of `result` make room for them.

## Explanation

Each round moves one bit from the bottom of `n` to the bottom of `result` while shifting the earlier bits of `result` up by one. The first bit read ends in position 31.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                     | Variables                    |
| ----------------------------------- | ---------------------------- |
| `result = 0`                        | `result = 0`                 |
| `result = (result << 1) \| (n & 1)` | `n = 0, result = 8, _ = 3`   |
| `result = (result << 1) \| (n & 1)` | `result = 256, _ = 8`        |
| `for _ in range(32):`               | `result = 4096, _ = 13`      |
| `for _ in range(32):`               | `result = 131072, _ = 18`    |
| `result = (result << 1) \| (n & 1)` | `result = 4194304, _ = 22`   |
| `result = (result << 1) \| (n & 1)` | `result = 134217728, _ = 27` |
| `return`                            | `returned = 2147483648`      |

### Complexity

- Time: O(1) constant 32 iterations.
- Extra space: O(1) constant extra space.
- The brute force takes O(1) constant 32-bit string operations.
