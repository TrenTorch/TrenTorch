---
name: sheet-count-square-loop
title: 'Square Root Loop'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
theory: loops-that-stop-at-the-square-root
---

## Statement

This loop runs while `i * i` has not passed `n`:

```python
count = 0
i = 1
while i * i <= n:
    count += 1
    i += 1
```

Implement `count_square_loop(n)` so it returns the final value of `count`.

`n` can be as large as `10**18`, so you cannot run the loop.

### Examples

**Example 1**

Input:

```python
count_square_loop(10)
```

Output:

```text
3
```

`i = 1, 2, 3` run (3 * 3 = 9 <= 10); `i = 4` gives 16 > 10.

**Example 2**

Input:

```python
count_square_loop(16)
```

Output:

```text
4
```

`i = 1, 2, 3, 4` run.

### Constraints

- `0 <= n <= 10**18`

## Explanation

The loop body runs for `i = 1, 2, ..., r` where `r = isqrt(n)`, so the answer is `isqrt(n)`. For `n = 0` no `i` qualifies and the answer is `0`, which `isqrt(0)` also gives.

`math.isqrt` works on exact integers, so it is right for every `n`.

### Complexity

- Time: O(1). `math.isqrt` on a number of at most 60 bits does a fixed number of steps.
- Space: O(1). A single integer is produced.
