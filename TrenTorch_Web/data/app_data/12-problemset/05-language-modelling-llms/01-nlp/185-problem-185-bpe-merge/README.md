---
name: problem-185-bpe-merge
title: 'BPE Merge'
tags: [problemset, transformer-llm, tokenization]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'scan with an index; on a match append the concatenation and advance by 2'
tools: [NumPy]
---

## Statement

Apply one BPE merge to a token sequence: scan left to right and replace each occurrence of the adjacent pair `pair` by the concatenation of its two tokens. Merged occurrences do not overlap, so the earlier pair wins.

Implement `solve(seq, pair)`.

**Returns.** Return a new list of tokens.

### Examples

**Example 1**

Input:

```python
solve(['a', 'b', 'a', 'b', 'c'], ('a', 'b'))
```

Output:

```text
['ab', 'ab', 'c']
```

**Example 2**

Input:

```python
solve(['a', 'a', 'a'], ('a', 'a'))
```

Output:

```text
['aa', 'a']
```

## Theory

### The simple version

Once the most frequent pair has been chosen, every place it occurs in the data is rewritten as a single new token. Repeating "count pairs, merge the best" grows the vocabulary one token at a time.

### The rule

Scan from the left; if `seq[i], seq[i+1] == pair`, emit their concatenation and skip both; otherwise emit `seq[i]`.

## Explanation

Scanning left to right and skipping both tokens avoids overlaps: in `['a','a','a']` with the pair `('a','a')` only the first two merge, giving `['aa', 'a']` (second example).
