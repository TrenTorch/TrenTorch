---
name: sheet-valid-palindrome
title: 'Valid Palindrome'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
---

## Statement

Return `True` if `s` is a **palindrome** when you keep only **letters and digits** (`a-z`, `A-Z`, `0-9`) and ignore the case. An empty result is a palindrome.

### Examples

**Example 1**

Input:

```python
valid_palindrome('A man, a plan, a canal: Panama')
```

Output:

```text
True
```

**Example 2**

Input:

```python
valid_palindrome('race a car')
```

Output:

```text
False
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains printable ASCII characters.

## Theory

Clean the string first, then compare it with its reverse. `str.isalnum()` is `True` for letters and digits, `str.lower()` removes case differences, and `text[::-1]` reverses a string. The whole check is `O(n)`.

The **two-pointer** version avoids building the cleaned string: one pointer from each end, move inward, skip characters that are not letters or digits, and compare the lower-cased characters. It uses `O(1)` extra memory, and it is the version to give in an interview.

## Explanation

`cleaned` keeps only alphanumeric characters, lower-cased. The string is a palindrome when it equals its reverse. Two-pointer code would reach the same answer without the copy.
