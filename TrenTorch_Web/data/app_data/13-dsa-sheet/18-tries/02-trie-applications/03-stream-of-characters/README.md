---
name: sheet-stream-of-characters
title: 'Stream of Characters'
tags: [dsa-sheet, tries, trie-applications]
difficulty: Advanced
---

## Statement

Letters of `stream` arrive one by one. After **each** letter, report whether **some suffix of the letters received so far is one of the `words`**.

For `words = ["cd", "f", "kl"]` and `stream = "abcdefghijkl"` the answer is `[False, False, False, True, False, True, False, False, False, False, False, True]`.

The starter code tries every word after every letter. It is correct but too slow for many words and long streams.

### Examples

**Example 1**

Input:

```python
stream_checker(['cd', 'f', 'kl'], 'abcdefghijkl')
```

Output:

```text
[False, False, False, True, False, True, False, False, False, False, False, True]
```

**Example 2**

Input:

```python
stream_checker(['a'], 'ba')
```

Output:

```text
[False, True]
```

### Constraints

- `0 <= len(words) <= 2000`
- `1 <= len(word) <= 10`
- `0 <= len(stream) <= 100000`
- Lower-case letters.

## Theory

A **trie** (prefix tree) stores a set of words letter by letter: every node is one letter, a word is a path from the root, and words that share a prefix share the start of their path. Each node has up to 26 children (a dictionary `letter -> node` in Python) and a flag that says "a word ends here". Inserting or searching a word of length `L` takes `O(L)` no matter how many words are stored, and a trie answers **prefix** questions ("does any word start with `ab`?") that a plain set of words cannot answer quickly. A node can be a small dictionary: `node = {}`; mark the end of a word with a special key such as `"$"`.

You are asked about the **end** of the stream, while a trie matches **starts** of words. Reverse the words: insert each word **reversed** into a trie. Then, after each new letter, walk the trie along the stream **backwards** (the newest letter first). If the walk reaches a node marked as a word end, some suffix of the stream is a word.

Words are at most `maxlen` long, so look back at most `maxlen` letters: `O(maxlen)` per letter instead of `O(words)`.

## Explanation

The inner loop goes from the newest letter back, at most `maxlen` steps, following the reversed-word trie.
