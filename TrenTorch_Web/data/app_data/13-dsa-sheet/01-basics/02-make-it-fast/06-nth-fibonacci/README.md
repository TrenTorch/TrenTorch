---
name: sheet-nth-fibonacci
title: 'Nth Fibonacci Number'
tags: [dsa-sheet, basics, make-it-fast]
difficulty: Intermediate
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

## Theory

The starter calls itself twice per step, so it recomputes the same values again and again. The number of calls grows like `F(n)` itself, which is exponential: `O(2ⁿ)` for practical purposes.

Each `F(k)` only depends on the two before it, so compute them once, in order. Keep just the last two values and move forward: `O(n)` time and `O(1)` extra values. This is the simplest form of **dynamic programming**: remember sub-answers instead of recomputing them.

You could also cache the recursive version with `functools.lru_cache`. Python's recursion limit is 1000 by default, so a cached recursion on `n = 50000` fails unless you raise it with `sys.setrecursionlimit`. The loop avoids the problem.

## Explanation

`a, b = b, a + b` slides the pair `(F(k), F(k+1))` forward one step. After `n` steps `a` is `F(n)`.

The numbers get big, so each addition costs time proportional to the number of digits, but 50,000 additions still run well under a second.
