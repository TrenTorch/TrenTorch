---
name: sheet-largest-odd-number
title: 'Largest Odd Number in a String'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

**Explanation:** The rightmost odd digit is 5 at index 0, so the prefix up to it is '5'.

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

**Explanation:** No odd digits exist, so no odd substring can be formed and the result is empty.

There is no odd digit.

### Constraints

- `0 <= len(num) <= 3 * 10**5`
- `num` contains digits and may start with `0`.

## Theory

A number is odd exactly when its **last digit** is odd. So the candidates are the substrings that end at an odd digit.

For a fixed end, the best substring starts as early as possible, so it is a prefix: a longer string of digits is a bigger number. And the **latest** odd digit gives the longest prefix, so it beats every earlier one.

So find the **last odd digit** and return everything up to and including it: `num[:i + 1]`. There is no need to compare numbers. If `num` starts with zeros the prefix keeps them: the answer is the longest substring that ends in an odd digit.

## Explanation

Scan from the right for the first digit that is odd (`1 3 5 7 9`). Return the prefix up to it. If no digit is odd, return `""`.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                         | Variables        |
| --------------------------------------- | ---------------- |
| `for i in range(len(num) - 1, -1, -1):` | `i = 1`          |
| `for i in range(len(num) - 1, -1, -1):` | `i = 0`          |
| `return`                                | `returned = '5'` |

### Complexity

- Time: O(n) where n is length of num.
- Extra space: O(1) extra space.
- The brute force takes O(n^3) where n is length of num.
