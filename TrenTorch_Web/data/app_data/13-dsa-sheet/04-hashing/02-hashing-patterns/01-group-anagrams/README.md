---
name: sheet-group-anagrams
title: 'Group Anagrams'
tags: [dsa-sheet, hashing, hashing-patterns]
difficulty: Intermediate
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

## Theory

Comparing every pair of words is `O(n²)` comparisons. Instead give every word a **signature** that is the same for all anagrams and different otherwise, and group by signature with a dictionary.

The usual signature is the word with its letters **sorted**: `"eat"`, `"tea"` and `"ate"` all become `"aet"`. Use it as the dictionary key (strings are hashable) and append each word to the list stored under its key. A `defaultdict(list)` creates the empty list the first time a key is seen.

A tuple of letter counts also works and is `O(length)` per word instead of `O(length log length)`; sorting is simpler and fast for short words.

## Explanation

`groups[''.join(sorted(word))].append(word)` puts every word under its signature. Sort each group's words and then sort the groups by their first word to get one exact order.
