---
name: sheet-longest-common-prefix
title: 'Longest Common Prefix'
tags: [dsa-sheet, strings, string-basics]
difficulty: Beginner
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

**Explanation:** All three words begin with "fl", but the third character differs ("o" vs "i"), so the longest common prefix is "fl".

**Example 2**

Input:

```python
longest_common_prefix(['dog', 'car'])
```

Output:

```text
''
```

**Explanation:** The first words "dog" and "car" have no matching initial character, so no common prefix exists.

### Constraints

- `0 <= len(words) <= 10**4`
- `0 <= len(word) <= 100`
- Words contain lower-case letters.

## Theory

The common prefix cannot be longer than the **shortest word**, and it is decided by the first position where the words disagree.

Two good approaches. **Vertical scanning**: compare the words column by column (all first letters, then all second letters, ...) and stop at the first column where they differ or a word ends. **Sort trick**: after sorting, the common prefix of _all_ words is the common prefix of just the **first and last** word, because every word in between sorts between them and must share what they share. That reduces the work to comparing two strings.

`os.path.commonprefix(words)` does it in the standard library; the point of the exercise is to know why it works.

## Explanation

An empty list returns `""`. Otherwise `min(words)` and `max(words)` are the alphabetically first and last words. Walk them together and stop at the first character that differs; everything before it is shared by all the words in between, hence by every word.

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                        | Variables                           |
| -------------------------------------- | ----------------------------------- |
| `first, last = min(words), max(words)` | `first = 'flight', last = 'flower'` |
| `i = 0`                                | `i = 0`                             |
| `i += 1`                               | `i = 1`                             |
| `i += 1`                               | `i = 2`                             |
| `return`                               | `returned = 'fl'`                   |

### Complexity

- Time: O(n * m) with n words, m max length.
- Extra space: O(1) extra space.
- The brute force takes O(n * m) with n words, m max length.
