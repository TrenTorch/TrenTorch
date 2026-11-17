---
name: sheet-trailing-zeros-of-factorial
title: 'Trailing Zeros of a Factorial'
tags: [dsa-sheet, maths, number-theory]
difficulty: Intermediate
theory: zeros-at-the-end-of-a-factorial
---

## Statement

Return the number of **zeros at the end of `n!`** (`n! = 1 × 2 × ... × n`).

For `n = 25` the answer is `6` (`25! = 15511210043330985984000000`).

The starter code visits every number up to `n`. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
trailing_zeros(25)
```

Output:

```text
6
```

**Example 2**

Input:

```python
trailing_zeros(5)
```

Output:

```text
1
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Explanation

`n //= 5` in each round gives `n // 5`, then `n // 25`, and so on, and the terms are added up.

### Complexity

- Time: O(log n). The loop divides by 5 until zero, adding the multiples of 5, 25, 125, ...
- Space: O(1). A counter.
