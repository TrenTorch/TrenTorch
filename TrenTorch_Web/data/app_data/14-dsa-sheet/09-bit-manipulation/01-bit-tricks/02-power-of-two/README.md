---
name: sheet-power-of-two
title: 'Is It a Power of Two?'
tags: [dsa-sheet, bit-manipulation, bit-tricks]
difficulty: Beginner
theory: is-it-a-power-of-two
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

## Explanation

For a positive power of two, `n - 1` has all the lower bits set and the single `1` cleared, so `n & (n - 1)` is `0`. Any other positive number has a higher set bit that survives the `&`.

### Complexity

- Time: O(1). A power of two has exactly one set bit, which `n & (n - 1) == 0` tests.
- Space: O(1). Nothing is stored.
