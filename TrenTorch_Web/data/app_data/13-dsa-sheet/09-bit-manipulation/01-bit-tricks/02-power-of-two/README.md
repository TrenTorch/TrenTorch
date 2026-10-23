---
name: sheet-power-of-two
title: 'Is It a Power of Two?'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
---

## Statement

Return `True` if `n` is a power of two (`1, 2, 4, 8, 16, ...`) and `False` otherwise. Do it without a loop.

### Examples

**Example 1**

Input:

```python
is_power_of_two(16)
```

Output:

```text
True
```

**Example 2**

Input:

```python
is_power_of_two(6)
```

Output:

```text
False
```

### Constraints

- `-2**62 <= n < 2**62`

## Theory

A power of two has **exactly one** bit set: `8` is `1000`. Using the trick `n & (n - 1)` (it clears the lowest set bit), a number with a single set bit becomes `0`. So `n > 0 and n & (n - 1) == 0` answers the question in one step.

The `n > 0` check matters: `0` also gives `0 & -1 == 0` and negative numbers have many set bits in two's complement form, so they must be excluded.

The loop version (`while n % 2 == 0: n //= 2`) works too, but takes up to 62 steps.

## Explanation

For a positive power of two, `n - 1` has all the lower bits set and the single `1` cleared, so `n & (n - 1)` is `0`. Any other positive number has a higher set bit that survives the `&`.
