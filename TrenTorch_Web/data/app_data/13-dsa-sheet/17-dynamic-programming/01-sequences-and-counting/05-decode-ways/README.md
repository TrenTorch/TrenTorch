---
name: sheet-decode-ways
title: 'Decode Ways'
tags: [dsa-sheet, dynamic-programming, sequences-and-counting]
difficulty: Intermediate
---

## Statement

A message uses the code `A = 1, B = 2, ..., Z = 26`. Given a string `s` of digits, return the **number of ways to decode it** into letters (a digit group like `"06"` or `"0"` alone is not a valid code). The answer is returned modulo `10**9 + 7`.

For `"12"` the answer is `2` (`AB` or `L`); for `"226"` it is `3`; for `"06"` it is `0`.

### Examples

**Example 1**

Input:

```python
num_decodings('12')
```

Output:

```text
2
```

**Explanation:** 12 can be read as 1 and 2 (AB) or as 12 (L), so there are 2 ways.

**Example 2**

Input:

```python
num_decodings('226')
```

Output:

```text
3
```

**Explanation:** 226 can be split as 2 2 6, 22 6 or 2 26. The whole 226 is above 26, so it is not a code. That makes 3 ways.

**Example 3**

Input:

```python
num_decodings('06')
```

Output:

```text
0
```

**Explanation:** 06 starts with 0, which has no letter, and 06 is not a valid code, so there are 0 ways.

### Constraints

- `0 <= len(s) <= 200000`
- `s` contains only digits.

## Theory

**Dynamic programming (DP)** solves a problem by combining the answers to smaller versions of the same problem and **remembering** them, so each smaller version is solved only once. It works when the plain recursion keeps asking the same questions (**overlapping subproblems**) and the best answer is built from best answers of smaller parts (**optimal substructure**). The recipe: pick the **state** (what identifies one subproblem), write the **transition** (how a state's answer comes from smaller states), set the **base cases**, and choose the **order**: top-down recursion with a cache, or a bottom-up table. A table often needs only its last row or last few values, which saves memory.

**State:** `ways(i)`, the number of ways to decode the first `i` digits. **Transition:** the last letter uses either one digit or two:

- one digit `s[i - 1]` is valid when it is not `"0"`: add `ways(i - 1)`;
- two digits `s[i - 2:i]` are valid when they form a number from 10 to 26: add `ways(i - 2)`.

**Base cases:** `ways(0) = 1` (the empty string has one way). The table can be shrunk to two variables. `O(n)`.

## Explanation

`a` is `ways(i - 2)` and `b` is `ways(i - 1)`. A zero digit contributes nothing alone but may still pair with the digit before it.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line       | Variables          |
| --------------------- | ------------------ |
| `mod = 10**9 + 7`     | `mod = 1000000007` |
| `a, b = 1, 1`         | `a = 1, b = 1`     |
| `now = 0`             | `i = 1, now = 0`   |
| `now += b`            | `now = 1`          |
| `now = 0`             | `i = 2, now = 0`   |
| `now += b`            | `now = 1`          |
| `a, b = b, now % mod` | `b = 2, now = 2`   |
| `return`              | `returned = 2`     |

### Complexity

- Time: O(n).
- Extra space: O(1).
- The brute force takes O(2^n).
