---
name: sheet-fast-power
title: 'Fast Power With a Remainder'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Intermediate
theory: fast-power-with-a-remainder
---

## Statement

Return `(base ** exp) % mod` where `exp` can be as large as `10**18`. The starter code multiplies `exp` times, which is far too slow for the big tests. Make it fast.

### Examples

**Example 1**

Input:

```python
power_mod(2, 10, 1000)
```

Output:

```text
24
```

`2**10 = 1024`, remainder 24.

**Example 2**

Input:

```python
power_mod(3, 0, 7)
```

Output:

```text
1
```

Anything to the power 0 is 1.

### Constraints

- `0 <= base < 10**9`
- `0 <= exp <= 10**18`
- `1 <= mod <= 10**9 + 7`
- Multiplying `exp` times is too slow for the large tests.

## Explanation

The loop version processes the bits of `exp`: when the lowest bit is `1`, multiply the result by the current power of `base`; then square the base and shift `exp` right. Each step is reduced modulo `mod`. `mod = 1` always gives `0`.

### Complexity

- Time: O(log exp). The exponent is halved at every step, with one or two modular multiplications each.
- Space: O(1). Three integers.
