---
name: sheet-largest-odd-number
title: 'Largest Odd Number in a String'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: scanning-from-the-end
---

## Statement

`num` is a string of digits. Return the **largest odd number** that appears as a **substring** (a run of consecutive digits) of `num`, as a string. If there is no odd number in it, return `""`.

### Examples

**Example 1**

Input:

```python
largest_odd_number('52')
```

Output:

```text
'5'
```

`5` is the biggest odd substring.

**Example 2**

Input:

```python
largest_odd_number('4206')
```

Output:

```text
''
```

There is no odd digit.

### Constraints

- `0 <= len(num) <= 3 * 10**5`
- `num` contains digits and may start with `0`.

## Explanation

Scan from the right for the first digit that is odd (`1 3 5 7 9`). Return the prefix up to it. If no digit is odd, return `""`.

### Complexity

- Time: O(n). Scan from the right until an odd digit is found, then slice.
- Space: O(n). The returned slice.
