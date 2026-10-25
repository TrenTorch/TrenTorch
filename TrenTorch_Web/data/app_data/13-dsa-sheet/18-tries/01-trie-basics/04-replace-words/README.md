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

### Worked example

The solution run on example 1, one step at a time. The values are recorded from the real code.

| After this line                  | Variables                                                                                                              |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `trie = {}`                      | `trie = {}`                                                                                                            |
| `node = trie`                    | `trie = {'c': {'a': {'t': {'$': True}}}}, root = 'bat', node = {'c': {'a': {'t': {'$': True}}}}, ch = 't'`             |
| `node = node.setdefault(ch, {})` | `trie = {'c': {'a': {'t': {'$': True}}}, 'b': {'a': {'t': {'$': T..., root = 'rat', node = {}, ch = 'r'`               |
| `node = trie`                    | `node = {'c': {'a': {'t': {'$': True}}}, 'b': {'a': {'t': {'$': T..., ch = 't', out = ['the'], word = 'cattle', i = 0` |
| `for i, ch in enumerate(word):`  | `ch = 'w', out = ['the', 'cat'], word = 'was'`                                                                         |
| `out.append(word[: i + 1])`      | `node = {'$': True}, ch = 't', out = ['the', 'cat', 'was', 'rat'], word = 'rattled', i = 2`                            |
| `node = node.get(ch)`            | `node = None, out = ['the', 'cat', 'was', 'rat', 'by'], word = 'the', i = 0`                                           |
| `return`                         | `returned = 'the cat was rat by the bat'`                                                                              |

### Complexity

- Time: O(n + q): The Trie construction takes O(n) time, where n is the total number of characters in the roots. The search and replacement process for the sentence takes O(q) time, where q is the total number of characters in the input sentence, since each character is processed once while traversing the Trie. Thus, the total time is O(n + q).
- Extra space: O(n): The space used by the Trie to store the root words is proportional to the total number of characters in the roots, which is n. There is no significant additional space used for the search itself, as it is performed directly on the existing data structure.
- The brute force takes O(n * q).
