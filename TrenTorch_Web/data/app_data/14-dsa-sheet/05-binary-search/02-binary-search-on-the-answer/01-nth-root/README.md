---
name: sheet-nth-root
title: 'Integer Root'
tags: [dsa-sheet, binary-search, binary-search-on-the-answer]
difficulty: Intermediate
theory: integer-roots
---

## Statement

Return the whole number `x` such that `x ** m == n`, or `-1` if there is no such whole number.

For example the cube root of `27` is `3`, and `2` has no whole square root, so the answer is `-1`.

### Examples

**Example 1**

Input:

```python
nth_root(27, 3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
nth_root(2, 2)
```

Output:

```text
-1
```

### Constraints

- `1 <= n <= 10**18`
- `1 <= m <= 40`
- Trying every `x` one by one is too slow for the large tests.

## Explanation

Binary search for the integer `x` with `x**m == n`. If `x**m` is below `n`, search higher; if above, search lower; if equal, return `x`; if the range runs out, there is no exact root, so return `-1`.

The range does not need to start at `n`: `n` has `b = n.bit_length()` bits, so its `m`-th root is below `2^(b // m + 1)`. That makes the search about `b / m` steps instead of `b`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                              | Variables        |
| -------------------------------------------- | ---------------- |
| `lo, hi = 1, 1 << (n.bit_length() // m + 1)` | `lo = 1, hi = 4` |
| `mid = (lo + hi) // 2`                       | `mid = 2`        |
| `power = mid**m`                             | `power = 8`      |
| `lo = mid + 1`                               | `lo = 3`         |
| `mid = (lo + hi) // 2`                       | `mid = 3`        |
| `power = mid**m`                             | `power = 27`     |
| `return`                                     | `returned = 3`   |

### Complexity

- Time: O((log n / m + 1) * log m) big-number multiplications. The root is below `2^(bits(n) / m + 1)`, so the search needs about `log2(n) / m` halvings, and each probe raises a number to the power `m` with `O(log m)` multiplications.
- Space: O(log n) bits. The powers have at most about `log2(n)` bits.
