---
name: sheet-reverse-words
title: 'Reverse the Words'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

## Theory

`s.split()` with **no argument** splits on any run of whitespace and drops the empty pieces, which removes the extra spaces for free. `" ".join(words)` glues pieces back with single spaces. Reversing a list is `words[::-1]` or `reversed(words)`.

Strings in Python are **immutable**: you cannot change a string in place, every "change" builds a new one. That is why building a long string with `+=` in a loop can be slow, while `join` builds it once. The whole job here is `O(n)`.

## Explanation

`s.split()` gives the words with no empty pieces, `[::-1]` reverses them, and `" ".join(...)` puts them back with one space between. An all-space or empty string has no words and gives `""`.
