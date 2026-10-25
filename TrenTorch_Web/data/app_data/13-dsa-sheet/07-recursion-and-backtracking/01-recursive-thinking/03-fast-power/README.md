---
name: sheet-fast-power
title: 'Fast Power With a Remainder'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Intermediate
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

**Explanation:** 2 raised to the 10th power modulo 1000 equals 24 because repeated squaring reduces the product modulo step by step.

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

**Explanation:** Any number to the zero power equals one, so 3 to the 0th power modulo 7 equals 1.

Anything to the power 0 is 1.

### Constraints

- `0 <= base < 10**9`
- `0 <= exp <= 10**18`
- `1 <= mod <= 10**9 + 7`
- Multiplying `exp` times is too slow for the large tests.

## Theory

**Exponentiation by squaring.** Instead of `exp` multiplications, halve the exponent: `x^(2k) = (x^k)^2` and `x^(2k+1) = x * (x^k)^2`. The recursion `power(x, e)` computes `half = power(x, e // 2)`, squares it, and multiplies by `x` once more when `e` is odd. The depth is `log₂ e`, about 60 for `10^18`.

Take the remainder **after every multiplication** so the numbers never grow beyond `mod²`. That is why this is used in cryptography and in problems that ask for "the answer modulo 1,000,000,007".

Python's built-in `pow(base, exp, mod)` does exactly this; write it yourself once so you understand where the speed comes from.

## Explanation

The loop version processes the bits of `exp`: when the lowest bit is `1`, multiply the result by the current power of `base`; then square the base and shift `exp` right. Each step is reduced modulo `mod`. `mod = 1` always gives `0`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                | Variables              |
| ------------------------------ | ---------------------- |
| `result = 1 % mod`             | `result = 1`           |
| `exp >>= 1`                    | `base = 4, exp = 5`    |
| `result = result * base % mod` | `result = 4`           |
| `exp >>= 1`                    | `base = 16, exp = 2`   |
| `base = base * base % mod`     | `base = 256`           |
| `result = result * base % mod` | `exp = 1, result = 24` |
| `base = base * base % mod`     | `base = 536`           |
| `return`                       | `returned = 24`        |

### Complexity

- Time: O(log exp) where exp is exponent.
- Extra space: O(1) extra memory.
- The brute force takes O(exp) where exp is exponent.
