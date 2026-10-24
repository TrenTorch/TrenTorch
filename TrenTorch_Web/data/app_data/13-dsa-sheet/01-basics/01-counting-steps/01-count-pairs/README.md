---
name: sheet-count-pairs
title: 'Count the Pairs'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
---

## Statement

This code counts pairs of positions:

```python
count = 0
for i in range(n):
    for j in range(i + 1, n):
        count += 1
```

Implement `count_pairs(n)` so it returns the final value of `count`.

`n` can be huge, so you cannot run the loops. Work the number out from the shape of the loops.

### Examples

**Example 1**

Input:

```python
count_pairs(4)
```

Output:

```text
6
```

The pairs are (0,1) (0,2) (0,3) (1,2) (1,3) (2,3).

**Example 2**

Input:

```python
count_pairs(1)
```

Output:

```text
0
```

No pair fits.

### Constraints

- `0 <= n <= 10**12`
- Your function must answer instantly, even for the largest `n`.

## Theory

The time a program takes is, to a first approximation, how many times its innermost line runs. Counting that is the basic skill behind every complexity bound.

Here the inner loop runs `n-1` times when `i = 0`, `n-2` times when `i = 1`, and so on down to `0`. The total is `(n-1) + (n-2) + ... + 1 + 0 = n(n-1)/2`.

That grows like `n²`, so the code is `O(n²)`: doubling `n` makes it about four times slower. The formula answers in one step, which is `O(1)`.

## Explanation

The inner loop runs `n-1-i` times for each `i`, so the total is the sum of `0..n-1`, which is `n(n-1)/2`.

`n * (n - 1)` is always even (one of two neighbours is even), so `//` gives the exact answer. Python integers do not overflow, so `10**12` squared is fine.
