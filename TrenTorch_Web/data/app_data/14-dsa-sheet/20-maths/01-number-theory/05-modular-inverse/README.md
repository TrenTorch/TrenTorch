---
name: sheet-modular-inverse
title: 'Modular Inverse'
tags: [dsa-sheet, maths, number-theory]
difficulty: Advanced
theory: dividing-in-a-world-of-remainders
---

## Statement

Return the number `x` with `0 <= x < m` such that `(a * x) % m == 1`, the **modular inverse** of `a` modulo `m`. If there is no such `x`, return `-1`. For `m = 1` the answer is `0`.

For `a = 3` and `m = 11` the answer is `4` (`3 × 4 = 12 = 1 mod 11`); for `a = 2` and `m = 4` it is `-1`.

### Examples

**Example 1**

Input:

```python
mod_inverse(3, 11)
```

Output:

```text
4
```

**Example 2**

Input:

```python
mod_inverse(2, 4)
```

Output:

```text
-1
```

### Constraints

- `1 <= m <= 10**9 + 7`
- `0 <= a <= 10**18`

## Explanation

The invariant is `old_r ≡ old_x × a (mod m)`. When the loop ends, `old_r` is the gcd; a gcd other than 1 means no inverse.

### Complexity

- Time: O(log m). The extended Euclidean algorithm takes about `log m` steps.
- Space: O(1). A few integers.
