---
name: sheet-reverse-vowels
title: 'Reverse the Vowels'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
---

## Statement

Return `s` with its **vowels** (`a e i o u`, in lower or upper case) in **reverse order**, while every other character stays where it is. A reversed vowel keeps its own case.

### Examples

**Example 1**

Input:

```python
reverse_vowels('hello')
```

Output:

```text
'holle'
```

**Explanation:** Vowels e and o reverse positions in hello to form holle.

**Example 2**

Input:

```python
reverse_vowels('leetcode')
```

Output:

```text
'leotcede'
```

**Explanation:** Vowels e e o e reverse to e o e e, giving leotcede.

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains letters.

## Theory

Collect the vowels in order, reverse them, and write them back into the vowel positions. Python strings are immutable, so work on a **list of characters**, change the list, and `"".join` it at the end.

A neat way to do it with two pointers: `i` from the left and `j` from the right; move each until it points at a vowel, swap, and continue inward. The version with a reversed list of vowels and an iterator is shorter: replace each vowel by the next one popped from the end.

## Explanation

`vowels` is the list of vowels in order; `reversed_vowels = iter(reversed(vowels))` hands them out from the end. Scanning `s`, each vowel is replaced by the next reversed vowel and all other characters are copied unchanged.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                                   | Variables                                                           |
| ------------------------------------------------- | ------------------------------------------------------------------- |
| `vowels = [ch for ch in s if ch in "aeiouAEIOU"]` | `vowels = ['e', 'o']`                                               |
| `replacement = iter(reversed(vowels))`            | `replacement = <list_reverseiterator object at 0x000001F484C57640>` |
| `return`                                          | `returned = 'holle'`                                                |
