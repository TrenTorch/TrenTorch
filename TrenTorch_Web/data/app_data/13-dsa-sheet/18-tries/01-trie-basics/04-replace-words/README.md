---
name: sheet-replace-words
title: 'Replace Words With Their Roots'
tags: [dsa-sheet, tries, trie-basics]
difficulty: Intermediate
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

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

Insert all roots into a trie with end markers. For each word, walk the trie letter by letter: the **first end marker** you meet marks the shortest root, so stop there and use the prefix of the word read so far. If the walk falls off the trie or the word ends first, keep the word.

Each word costs `O(len(word))` regardless of the number of roots.

## Explanation

The loop stops at the first node with the end marker, which is the shortest matching root because shorter prefixes are met first.
