---
name: sheet-replace-words
title: 'Replace Words With Their Roots'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
theory: the-shortest-stored-prefix
---

## Statement

`roots` is a list of root words. In the `sentence` (words separated by single spaces), replace every word that **starts with a root** by the **shortest root** it starts with. Words without a root stay as they are. Return the new sentence.

For `roots = ["cat", "bat", "rat"]` and `sentence = "the cattle was rattled by the battery"` the answer is `"the cat was rat by the bat"`.

The starter code tries every root for every word. It is correct but too slow with many roots and words.

### Examples

**Example 1**

Input:

```python
replace_words(['cat', 'bat', 'rat'], 'the cattle was rattled by the battery')
```

Output:

```text
'the cat was rat by the bat'
```

**Example 2**

Input:

```python
replace_words(['a', 'b', 'c'], 'aadsfasf absbs bbab cadsfafs')
```

Output:

```text
'a a b c'
```

### Constraints

- `0 <= len(roots) <= 5000`
- `0 <= number of words in the sentence <= 20000`
- Lower-case letters; words and roots are 1 to 20 long.

## Explanation

The loop stops at the first node with the end marker, which is the shortest matching root because shorter prefixes are met first.

### Complexity

- Time: O(R + S). The roots are put in a trie once (`R` = total length of roots); each word of the sentence walks down it at most to its first root (`S` = length of the sentence).
- Space: O(R + S). The trie and the output words.
