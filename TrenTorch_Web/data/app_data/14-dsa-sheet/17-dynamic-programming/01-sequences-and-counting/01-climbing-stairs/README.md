---
name: sheet-climbing-stairs
title: 'Climbing Stairs'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Beginner
theory: climbing-stairs
---

## Statement

You climb a staircase with `n` steps. Each move goes up **1 or 2** steps. Return the **number of different ways** to reach the top, modulo `10**9 + 7`.

For `n = 3` the answer is `3` (`1+1+1`, `1+2`, `2+1`).

The starter code is a plain recursion. It is correct but far too slow for large `n`.

### Examples

**Example 1**

Input:

```python
climb_stairs(3)
```

Output:

```text
3
```

**Example 2**

Input:

```python
climb_stairs(5)
```

Output:

```text
8
```

### Constraints

- `0 <= n <= 1000000`

## Explanation

The number of ways to climb `n` steps is the Fibonacci number `F(n + 1)`: the last move is a 1-step from `n - 1` or a 2-step from `n - 2`. Instead of adding `n` times, use fast doubling: from the pair `(F(k), F(k+1))` you get `F(2k) = F(k) * (2 * F(k+1) - F(k))` and `F(2k+1) = F(k)^2 + F(k+1)^2`, all modulo `10^9 + 7`. Recurse on `k >> 1` and step once more when `k` is odd. That is `log2(n)` levels.

### Complexity

- Time: O(log n). The number of ways is a Fibonacci number, and fast doubling gets `F(n)` in `log2(n)` steps.
- Space: O(log n). The recursion is `log2(n)` deep.
