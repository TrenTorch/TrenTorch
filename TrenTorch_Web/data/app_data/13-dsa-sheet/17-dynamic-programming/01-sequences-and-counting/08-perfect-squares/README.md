---
name: sheet-perfect-squares
title: 'Perfect Squares'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
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

**Explanation:** 12 can be expressed as 4+4+4, using three perfect squares, and no representation with fewer squares exists.

**Example 2**

Input:

```python
num_squares(13)
```

Output:

```text
2
```

**Explanation:** 13 equals 4+9, which uses two perfect squares, and it cannot be formed with a single square.

### Constraints

- `0 <= n <= 12000`

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

This is **coin change** where the coins are all the perfect squares up to `n`. **State:** `fewest(i)`, the fewest squares that sum to `i`. **Transition:** `fewest(i) = 1 + min(fewest(i - k*k))` over all `k` with `k*k <= i`. **Base case:** `fewest(0) = 0`. `O(n √n)`.

(Lagrange's four-square theorem says the answer is never more than 4, which gives an even faster number-theory solution, but the DP shows the general method.)

## Explanation

`best[i]` starts at `i` (all ones) and improves with each square that fits.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                 | Variables                                                         |
| ------------------------------- | ----------------------------------------------------------------- |
| `best = list(range(n + 1))`     | `best = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]`               |
| `k = 1`                         | `i = 4, k = 1`                                                    |
| `for i in range(2, n + 1):`     | `best = [0, 1, 2, 3, 1, 2, 6, 7, 8, 9, 10, 11, 12], i = 6, k = 3` |
| `k += 1`                        | `best = [0, 1, 2, 3, 1, 2, 3, 4, 8, 9, 10, 11, 12], i = 7, k = 2` |
| `k = 1`                         | `best = [0, 1, 2, 3, 1, 2, 3, 4, 2, 9, 10, 11, 12], i = 9, k = 1` |
| `best[i] = best[i - k * k] + 1` | `best = [0, 1, 2, 3, 1, 2, 3, 4, 2, 1, 2, 11, 12], i = 10`        |
| `k += 1`                        | `best = [0, 1, 2, 3, 1, 2, 3, 4, 2, 1, 2, 3, 12], i = 11, k = 4`  |
| `return`                        | `returned = 3`                                                    |

### Complexity

- Time: O(n * sqrt(n)), n is the input value.
- Extra space: O(n), n is the input value.
- The brute force takes O(n * sqrt(n)), n is the input value.
