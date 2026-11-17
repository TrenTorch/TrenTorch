---
name: sheet-reverse-words
title: 'Reverse the Words'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: words-and-the-reverse-words-problem
---

## Statement

A **word** is a run of characters that are not spaces. Return a string with the words of `s` in **reverse order**, separated by exactly one space, with no space at the start or the end. `s` may have extra spaces anywhere.

### Examples

**Example 1**

Input:

```python
reverse_words('the sky is blue')
```

Output:

```text
'blue is sky the'
```

**Example 2**

Input:

```python
reverse_words('  hello   world  ')
```

Output:

```text
'world hello'
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains letters and spaces.

## Explanation

`s.split()` gives the words with no empty pieces, `[::-1]` reverses them, and `" ".join(...)` puts them back with one space between. An all-space or empty string has no words and gives `""`.

### Complexity

- Time: O(n). `split` and `join` each read the string once.
- Space: O(n). The list of words and the result.
