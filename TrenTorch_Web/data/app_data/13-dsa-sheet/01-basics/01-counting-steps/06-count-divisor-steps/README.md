---
name: sheet-count-divisor-steps
title: 'Divisor Loop'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Advanced
---

## Statement

The inner loop jumps by `i` each time:

```python
count = 0
for i in range(1, n + 1):
    for j in range(i, n + 1, i):
        count += 1
```

Implement `count_divisor_steps(n)` so it returns the final value of `count`.

Looping `i` from `1` to `n` is too slow for the largest inputs.

### Examples

**Example 1**

Input:

```python
count_divisor_steps(5)
```

Output:

```text
10
```

`5//1 + 5//2 + 5//3 + 5//4 + 5//5 = 5 + 2 + 1 + 1 + 1`.

**Example 2**

Input:

```python
count_divisor_steps(10)
```

Output:

```text
27
```

### Constraints

- `1 <= n <= 10**10`
- An answer that loops `n` times will time out on the large tests.

## Theory

For one `i`, the inner loop visits `i, 2i, 3i, ...` up to `n`, which is `n // i` steps. So the total is `n//1 + n//2 + ... + n//n`. Summed over all `i` this is about `n ln n`: the harmonic series. This pattern is why the sieve of Eratosthenes runs in `O(n log log n)`.

The sum itself can be computed faster. The value `n // i` takes at most about `2√n` different values, and long runs of consecutive `i` share the same one. Add each run at once as `value * run_length`.

## Explanation

Start at `i = 1`. Let `q = n // i`. The largest `j` with `n // j == q` is `n // q`. All `i..j` contribute `q` each, so add `q * (j - i + 1)` and continue from `j + 1`.

There are at most `2√n` runs, so the loop does about `2 * 10**5` steps for `n = 10**10`.
