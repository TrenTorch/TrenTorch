---
name: sheet-count-square-loop
title: 'Square Root Loop'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
---

## Statement

This loop runs while `i * i` has not passed `n`:

```python
count = 0
i = 1
while i * i <= n:
    count += 1
    i += 1
```

Implement `count_square_loop(n)` so it returns the final value of `count`.

`n` can be as large as `10**18`, so you cannot run the loop.

### Examples

**Example 1**

Input:

```python
count_square_loop(10)
```

Output:

```text
3
```

`i = 1, 2, 3` run (3 * 3 = 9 <= 10); `i = 4` gives 16 > 10.

**Example 2**

Input:

```python
count_square_loop(16)
```

Output:

```text
4
```

`i = 1, 2, 3, 4` run.

### Constraints

- `0 <= n <= 10**18`

## Theory

A loop that stops at `i * i > n` runs about `√n` times, which is `O(√n)`. This shows up in primality testing and in finding divisors: you never need to look past the square root.

For the exact count you need the integer square root: the largest `r` with `r * r <= n`. Python has `math.isqrt`. Do not use `math.sqrt` or `n ** 0.5` here: floats only have about 15 digits, so for `n = 10**18 - 1` they round up to `1e9` and give the wrong answer.

## Explanation

The loop body runs for `i = 1, 2, ..., r` where `r = isqrt(n)`, so the answer is `isqrt(n)`. For `n = 0` no `i` qualifies and the answer is `0`, which `isqrt(0)` also gives.

`math.isqrt` works on exact integers, so it is right for every `n`.
