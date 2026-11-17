---
name: sheet-group-anagrams
title: 'Group Anagrams'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
theory: keys-that-ignore-the-order
---

## Statement

Group the words that are **anagrams** of each other (they use exactly the same letters). Inside a group sort the words alphabetically (repeated words stay), and sort the groups by their first word. Return the list of groups.

### Examples

**Example 1**

Input:

```python
group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
```

Output:

```text
[['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
```

**Example 2**

Input:

```python
group_anagrams(['a'])
```

Output:

```text
[['a']]
```

### Constraints

- `0 <= len(words) <= 10**5`
- Each word has at most 12 lower-case letters.

## Explanation

`groups[''.join(sorted(word))].append(word)` puts every word under its signature. Sort each group's words and then sort the groups by their first word to get one exact order.

### Complexity

- Time: O(n * k log k + n * k log n). Sorting each word is `k log k`; ordering the `n` words at the end needs `n log n` comparisons of strings of length `k`.
- Space: O(n * k). The dictionary of groups holds every word once.
