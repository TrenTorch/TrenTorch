---
name: sheet-word-pattern
title: 'Word Pattern'
tags: [dsa-sheet, hashing, counting-with-dictionaries]
difficulty: Intermediate
---

## Statement

`pattern` is a string of letters and `words` is a list of words. Return `True` if the words **follow the pattern**: each letter of the pattern stands for exactly one word, and each word is matched by exactly one letter. For example the pattern `"abba"` matches `["dog", "cat", "cat", "dog"]` but not `["dog", "cat", "cat", "fish"]` (`a` and `b` would both... `a` would need two words) and not `["dog", "dog", "dog", "dog"]` (`a` and `b` would share one word).

The pattern and the list must have the same length.

### Examples

**Example 1**

Input:

```python
word_pattern('abba', ['dog', 'cat', 'cat', 'dog'])
```

Output:

```text
True
```

**Example 2**

Input:

```python
word_pattern('abba', ['dog', 'dog', 'dog', 'dog'])
```

Output:

```text
False
```

### Constraints

- `0 <= len(pattern), len(words) <= 10**5`
- Pattern letters are lower-case; every word is a lower-case string.

## Theory

This is the isomorphism problem again, with letters on one side and **whole words** on the other. You need a two-way mapping: pattern letter to word, and word to pattern letter. A one-way check lets two letters share a word.

Dictionary keys can be any hashable value, including strings, so the code is the same as for characters. Walk both sequences together with `zip`; check that the lengths match first, because `zip` silently stops at the shorter one.

## Explanation

If the lengths differ the answer is `False`. Otherwise the loop keeps `letter_to_word` and `word_to_letter`. A mapping created earlier must match the current pair in both dictionaries.
