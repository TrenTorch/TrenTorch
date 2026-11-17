---
name: sheet-fibonacci-modulo
title: 'Huge Fibonacci Number'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
theory: huge-fibonacci-numbers
---

## Statement

The Fibonacci numbers are `F(0) = 0`, `F(1) = 1`, `F(k) = F(k - 1) + F(k - 2)`. Return `F(n)` modulo `10**9 + 7`.

For `n = 10` the answer is `55`.

The starter code adds up one number at a time. It is correct but far too slow when `n` is huge.

### Examples

**Example 1**

Input:

```python
fib_mod(10)
```

Output:

```text
55
```

**Example 2**

Input:

```python
fib_mod(0)
```

Output:

```text
0
```

### Constraints

- `0 <= n <= 9 * 10**15`

## Explanation

`pair(k)` returns `(F(k), F(k + 1))`. For odd `k` the pair is shifted by one step after doubling.

### Complexity

- Time: O(log n). Fast doubling halves `n` every step.
- Space: O(log n). The recursion is `log2(n)` deep.
