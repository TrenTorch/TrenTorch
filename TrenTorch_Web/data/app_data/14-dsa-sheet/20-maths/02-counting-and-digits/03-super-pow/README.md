---
name: sheet-super-pow
title: 'Super Power'
tags: [dsa-sheet, maths, counting-and-digits]
difficulty: Advanced
theory: powers-with-a-huge-exponent-given-as-digits
---

## Statement

Compute `a^b mod 1337`, where the exponent `b` is a **huge number given as a list of its decimal digits** (most significant digit first, for example `[1, 0]` means 10). The list is not empty.

For `a = 2` and `b = [1, 0]` the answer is `1024`; for `a = 2147483647` and `b = [2, 0, 0]` it is `1198`.

### Examples

**Example 1**

Input:

```python
super_pow(2, [1, 0])
```

Output:

```text
1024
```

**Example 2**

Input:

```python
super_pow(2147483647, [2, 0, 0])
```

Output:

```text
1198
```

### Constraints

- `1 <= a <= 2**31 - 1`
- `1 <= len(b) <= 2000`
- Each digit is `0` to `9`; `b` has no leading zero unless `b = [0]`.

## Explanation

Appending a digit `d` to the exponent multiplies the old exponent by 10 and adds `d`, which the two `pow` calls do.

### Complexity

- Time: O(len(b)). One step per digit of the exponent, each a pair of modular powers with a tiny exponent.
- Space: O(1). A few integers.
