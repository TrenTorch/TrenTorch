---
name: sheet-reverse-vowels
title: 'Reverse the Vowels'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: swapping-from-both-ends
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

**Example 2**

Input:

```python
reverse_vowels('leetcode')
```

Output:

```text
'leotcede'
```

### Constraints

- `0 <= len(s) <= 3 * 10**5`
- `s` contains letters.

## Explanation

`vowels` is the list of vowels in order; `reversed_vowels = iter(reversed(vowels))` hands them out from the end. Scanning `s`, each vowel is replaced by the next reversed vowel and all other characters are copied unchanged.

### Complexity

- Time: O(n). One pass collects the vowels and one pass rebuilds the string.
- Space: O(n). The vowel list and the result.
