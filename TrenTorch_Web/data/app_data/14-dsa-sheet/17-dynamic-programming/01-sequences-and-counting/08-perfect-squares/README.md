---
name: sheet-perfect-squares
title: 'Perfect Squares'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
theory: perfect-squares-and-word-break
---

## Statement

Return the **fewest perfect squares** (`1, 4, 9, 16, ...`) that add up to `n`.

For `n = 12` the answer is `3` (`4 + 4 + 4`); for `n = 13` it is `2` (`4 + 9`).

The starter code is a plain recursion. It is correct but too slow for large `n`.

### Examples

**Example 1**

Input:

```python
num_squares(12)
```

Output:

```text
3
```

**Example 2**

Input:

```python
num_squares(13)
```

Output:

```text
2
```

### Constraints

- `0 <= n <= 12000`

## Explanation

Two classic theorems finish this without a table. Lagrange: every positive integer is a sum of at most four squares, so the answer is 1, 2, 3 or 4. Legendre: it needs four exactly when, after removing all factors of 4, the number leaves remainder 7 when divided by 8.

So check in order: a perfect square gives 1; the 4-test gives 4; a loop over `i` from 1 up to `sqrt(n)` looking for `n - i^2` being a perfect square gives 2; everything else is 3.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line    | Variables          |
| ------------------ | ------------------ |
| `m = n`            | `m = 12`           |
| `m //= 4`          | `m = 3`            |
| `rest = n - i * i` | `i = 1, rest = 11` |
| `i += 1`           | `i = 2`            |
| `rest = n - i * i` | `rest = 8`         |
| `i += 1`           | `i = 3`            |
| `i += 1`           | `i = 4, rest = 3`  |
| `return`           | `returned = 3`     |

### Complexity

- Time: O(sqrt(n)). Lagrange's four-square theorem says the answer is at most 4; Legendre's three-square theorem gives exactly when it is 4 (`n = 4^a * (8b + 7)`); 1 and 2 are found by testing every square up to `sqrt(n)`.
- Space: O(1). A few integers.
