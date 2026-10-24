---
name: sheet-count-triple-loop
title: 'Three Nested Loops'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Intermediate
---

## Statement

This code has three loops that each start where the previous one is:

```python
count = 0
for i in range(n):
    for j in range(i, n):
        for k in range(j, n):
            count += 1
```

Implement `count_triple_loop(n)` so it returns the final value of `count`.

### Examples

**Example 1**

Input:

```python
count_triple_loop(3)
```

Output:

```text
10
```

The triples are (0,0,0) (0,0,1) (0,0,2) (0,1,1) (0,1,2) (0,2,2) (1,1,1) (1,1,2) (1,2,2) (2,2,2).

**Example 2**

Input:

```python
count_triple_loop(5)
```

Output:

```text
35
```

### Constraints

- `0 <= n <= 10**6`

## Theory

Each extra nested loop adds a factor of `n`, so three loops give `O(n³)`. Counting exactly is the same game as before, one level deeper.

Fix `i` and `j`: the innermost loop runs `n - j` times. Summing over `j` from `i` to `n-1` gives a triangle number, and summing those over `i` gives a tetrahedral number. The closed form is `n(n+1)(n+2)/6`, the same as choosing 3 items from `n + 2` with repeats.

## Explanation

The count is the number of triples `i <= j <= k` taken from `0..n-1`. That is the number of multisets of size 3 from `n` items, which is `C(n+2, 3) = n(n+1)(n+2)/6`.

The product of three consecutive integers is divisible by 6, so `//` is exact.
