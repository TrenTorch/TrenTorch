---
name: sheet-chinese-remainder-theorem
title: 'Chinese Remainder Theorem'
tags: [dsa-sheet, maths, number-theory]
difficulty: Mastery
theory: merging-two-conditions-at-a-time
---

## Statement

You are given conditions `x ≡ remainders[i] (mod moduli[i])`, that is, `x % moduli[i] == remainders[i] % moduli[i]`. The moduli do **not** have to be coprime. Return the **smallest non-negative `x`** that satisfies all of them, or `-1` if there is none. With no conditions the answer is `0`.

For `remainders = [2, 3, 2]` and `moduli = [3, 5, 7]` the answer is `23`.

The starter code tries the numbers one by one up to the least common multiple. It is correct but too slow when the moduli are large.

### Examples

**Example 1**

Input:

```python
solve_congruences([2, 3, 2], [3, 5, 7])
```

Output:

```text
23
```

**Example 2**

Input:

```python
solve_congruences([1, 2], [4, 6])
```

Output:

```text
-1
```

### Constraints

- `0 <= len(moduli) == len(remainders) <= 20`
- `1 <= moduli[i] <= 10000`, `0 <= remainders[i] <= 10**9`
- The least common multiple of the moduli is at most `10**12`.

## Explanation

`x` and `modulus` always describe the solutions found so far as `x mod modulus`. Each step either detects a contradiction or merges one more condition.

### Complexity

- Time: O(k log M). One extended-gcd step (`pow(x, -1, m)`) per congruence (`k` of them, `M` = the lcm).
- Space: O(1). A few integers.
