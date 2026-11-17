---
name: sheet-count-halving-steps
title: 'Halving Steps'
tags: [dsa-sheet, basics, counting-steps]
difficulty: Beginner
theory: halving-gives-a-logarithm
---

## Statement

This loop keeps halving `n`, rounding down:

```python
count = 0
while n > 1:
    n //= 2
    count += 1
```

Implement `count_halving_steps(n)` so it returns the final value of `count`.

### Examples

**Example 1**

Input:

```python
count_halving_steps(8)
```

Output:

```text
3
```

8 → 4 → 2 → 1 is 3 steps.

**Example 2**

Input:

```python
count_halving_steps(1000)
```

Output:

```text
9
```

1000 → 500 → 250 → 125 → 62 → 31 → 15 → 7 → 3 → 1 is 9 steps.

### Constraints

- `1 <= n <= 10**18`

## Explanation

`n // 2` drops the last binary digit, so the loop runs until one digit is left: `n.bit_length() - 1` times.

The simulation also works here, because it only takes about 60 steps for `10**18`. The point of this question is to see that the answer is `log₂ n`, not `n`.

### Complexity

- Time: O(1). `bit_length()` reads the size of the integer instead of looping.
- Space: O(1). A single integer is produced.
