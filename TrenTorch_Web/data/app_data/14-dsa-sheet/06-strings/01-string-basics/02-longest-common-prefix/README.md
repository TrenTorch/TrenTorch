---
name: sheet-longest-common-prefix
title: 'Longest Common Prefix'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
theory: comparing-column-by-column
---

## Statement

Return the **longest prefix** (the beginning of a string) that **all** the words in `words` start with. If they share none, or the list is empty, return `""`.

### Examples

**Example 1**

Input:

```python
longest_common_prefix(['flower', 'flow', 'flight'])
```

Output:

```text
'fl'
```

**Example 2**

Input:

```python
longest_common_prefix(['dog', 'car'])
```

Output:

```text
''
```

### Constraints

- `0 <= len(words) <= 10**4`
- `0 <= len(word) <= 100`
- Words contain lower-case letters.

## Explanation

An empty list returns `""`. Otherwise `min(words)` and `max(words)` are the alphabetically first and last words. Walk them together and stop at the first character that differs; everything before it is shared by all the words in between, hence by every word.

### Complexity

- Time: O(S). The smallest and largest word (in dictionary order) are found with `n` comparisons that stop at the first difference; `S` is the total number of characters.
- Space: O(m). The returned prefix, `m` = length of the shortest word.
