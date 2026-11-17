---
name: sheet-string-to-integer
title: 'String to Integer'
tags: [dsa-sheet, strings, harder-strings]
difficulty: Intermediate
theory: parsing-a-number-with-rules
---

## Statement

Convert the start of the string `s` to a whole number, following these rules in order:

1. Skip **leading spaces** (only the space character).
2. If the next character is `+` or `-`, read it as the sign (no sign means positive).
3. Read **digits** (`0` to `9`) until the first character that is not a digit or the end of the string. Ignore everything after that.
4. If no digit was read, the result is `0`.
5. Clamp the result to the range of a signed 32-bit integer: if it is below `-2**31` return `-2**31`, if above `2**31 - 1` return `2**31 - 1`.

### Examples

**Example 1**

Input:

```python
my_atoi('42')
```

Output:

```text
42
```

The digits `42`.

**Example 2**

Input:

```python
my_atoi('   -42abc')
```

Output:

```text
-42
```

Spaces skipped, sign `-`, digits `42`, then `abc` ignored.

**Example 3**

Input:

```python
my_atoi('words 987')
```

Output:

```text
0
```

The first character is a letter, so no digit is read: 0.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains letters, digits, spaces, `+` and `-`.

## Explanation

The index `i` moves through spaces, then the optional sign, then the digits. After each digit, `if value > 2**31: break` stops early because the result will be clamped anyway. Multiply by the sign and clamp with `max`/`min`.

### Complexity

- Time: O(n). One pass over the characters; the digit loop stops as soon as the value passes the 32-bit limit.
- Space: O(1). A few variables.
