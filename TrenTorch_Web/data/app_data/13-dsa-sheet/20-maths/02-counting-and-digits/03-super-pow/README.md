---
name: sheet-super-pow
title: 'Super Power'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
---

## Statement

Compute `a^b mod 1337`, where the exponent `b` is a **huge number given as a list of its decimal digits** (most significant digit first, for example `[1, 0]` means 10). The list is not empty.

For `a = 2` and `b = [1, 0]` the answer is `1024`; for `a = 2147483647` and `b = [2, 0, 0]` it is `1198`.

### Examples

**Example 1**

Input:

```python
super_pow(2, [1, 0])
```

Output:

```text
1024
```

**Example 2**

Input:

```python
super_pow(2147483647, [2, 0, 0])
```

Output:

```text
1198
```

### Constraints

- `1 <= a <= 2**31 - 1`
- `1 <= len(b) <= 2000`
- Each digit is `0` to `9`; `b` has no leading zero unless `b = [0]`.

## Theory

Many contest problems are about **numbers**, and the input is huge (up to `10^12` or more), so a loop up to `n` is far too slow. The tools: the **square root bound** (a number `n` has a divisor `<= sqrt(n)` unless it is prime), **modular arithmetic** (work with remainders so the numbers stay small), and **formulas** that replace a loop. Python's big integers make the arithmetic itself safe, but the number of steps is what you must control.

Turning `b` into a normal integer and computing `a ** b` is impossible (the result has billions of digits). Use the digits directly with the identity `a^(10·q + d) = (a^q)^10 × a^d`. Process the digits from the left: keep `result = a^(prefix of b) mod 1337`. For the next digit `d`: `result = pow(result, 10, 1337) × pow(a, d, 1337) % 1337`.

That is one small modular power per digit, `O(len(b))` in total.

## Explanation

Appending a digit `d` to the exponent multiplies the old exponent by 10 and adds `d`, which the two `pow` calls do.
