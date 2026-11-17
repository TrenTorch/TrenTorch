---
name: sheet-valid-palindrome
title: 'Valid Palindrome'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: skipping-characters-we-do-not-care-about
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

## Explanation

Two pointers, one at each end. Skip any character that is not a letter or digit. When both point at letters or digits, compare them in lower case: a difference means it is not a palindrome. Move both inward; reaching the middle means it is one. An empty string, or one with only punctuation, is a palindrome.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line        | Variables         |
| ---------------------- | ----------------- |
| `i, j = 0, len(s) - 1` | `i = 0, j = 29`   |
| `i += 1`               | `i = 3, j = 28`   |
| `j -= 1`               | `i = 5, j = 25`   |
| `j -= 1`               | `i = 8, j = 24`   |
| `j -= 1`               | `i = 10, j = 22`  |
| `i += 1`               | `i = 12, j = 20`  |
| `i += 1`               | `i = 15, j = 18`  |
| `return`               | `returned = True` |

### Complexity

- Time: O(n). Two pointers move toward each other, skipping non-alphanumeric characters.
- Space: O(1). Two indices.
