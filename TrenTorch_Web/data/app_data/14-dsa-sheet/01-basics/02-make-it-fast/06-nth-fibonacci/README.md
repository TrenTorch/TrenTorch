---
name: sheet-nth-fibonacci
title: 'Nth Fibonacci Number'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
theory: fibonacci-slowly-and-then-very-quickly
---

## Statement

The Fibonacci numbers start `F(0) = 0`, `F(1) = 1`, and every next number is the sum of the previous two. Return `F(n)`.

The starter code follows the definition directly. It is correct but takes far too long once `n` reaches 40 or so. Make it fast.

### Examples

**Example 1**

Input:

```python
nth_fibonacci(10)
```

Output:

```text
55
```

0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55.

**Example 2**

Input:

```python
nth_fibonacci(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 50000`
- The answer can have more than 10,000 digits. Python integers handle that without overflow.

## Explanation

Fast doubling. If you know the pair `(F(k), F(k+1))`, the pair for `2k` is `F(2k) = F(k) * (2 * F(k+1) - F(k))` and `F(2k+1) = F(k)^2 + F(k+1)^2`. Recurse on `k >> 1`, then step forward once more when `k` is odd. That is only `log2(n)` levels instead of `n` additions.

The numbers have thousands of digits, so what costs time is the big multiplications, and the last level dominates.

### Complexity

- Time: O(log n) big-number multiplications. Fast doubling halves `n` at every step; the numbers have about `0.69 * n` bits, so the last multiplications dominate and the total is about the cost of multiplying two `n`-bit numbers.
- Space: O(n) bits. The result `F(n)` itself has about `0.69 * n` bits; the recursion is only `log2(n)` deep.
