---
name: sheet-gray-code
title: 'Gray Code'
tags: [dsa-sheet, recursion, recursive-thinking]
difficulty: Intermediate
---

## Statement

A **Gray code** is a sequence of all `2^n` numbers from `0` to `2^n - 1` where **each number differs from the next in exactly one bit**, and the last differs from the first in one bit too. Return the standard (reflected) Gray code that starts at `0`.

For `n = 2`: `[0, 1, 3, 2]` (binary `00, 01, 11, 10`).

### Examples

**Example 1**

Input:

```python
gray_code(2)
```

Output:

```text
[0, 1, 3, 2]
```

**Example 2**

Input:

```python
gray_code(0)
```

Output:

```text
[0]
```

### Constraints

- `0 <= n <= 16`

## Theory

The **reflected** construction is recursive. The Gray code for `n` bits is the Gray code for `n - 1` bits, followed by the same list **in reverse order with the top bit set**. Reversing makes the last number of the first half equal to the first number of the second half apart from the new top bit, so they still differ in one bit.

There is also a closed formula with no recursion: the `i`-th number is `i ^ (i >> 1)`: the number XOR-ed with itself shifted right by one bit. Both give the same sequence. Gray codes are used in encoders and in Karnaugh maps because only one bit changes at a time.

## Explanation

`[i ^ (i >> 1) for i in range(2**n)]` builds the reflected Gray code directly. The recursive construction doubles the list at each step: `codes + [c | (1 << (k - 1)) for c in reversed(codes)]`.
