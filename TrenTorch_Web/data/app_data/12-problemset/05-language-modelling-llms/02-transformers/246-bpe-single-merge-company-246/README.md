---
name: bpe-single-merge-company-246
title: 'bpe-single-merge — Netflix case'
tags: [problemset, transformer-llm, tokenization-for-llms, netflix]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|Transformers'
topic: 'Transformers'
caseCompany: 'Netflix'
hint: 'scan with an index; on a match append merged and advance by 2'
---

## Statement

Netflix-inspired text-ranking pipeline is building a compact subword vocabulary from frequent token pairs. You need to perform one BPE merge correctly so the vocabulary-building process can continue.

Perform one BPE merge: scan `tokens` from left to right and replace every occurrence of the adjacent pair `(a, b)` by the single token `merged`. Matches do not overlap; the leftmost one is merged first.

Implement `solve(tokens,a,b,merged)`.

**Returns.** Return a new list of tokens. If the pair does not occur the tokens are returned unchanged (as a new list).

Perform one BPE merge: scan `tokens` from left to right and replace every occurrence of the adjacent pair `(a, b)` by the single token `merged`. Matches do not overlap; the leftmost one is merged first.

Implement `solve(tokens,a,b,merged)`.

**Returns.** Return a new list of tokens. If the pair does not occur the tokens are returned unchanged (as a new list).

### Examples

**Example 1**

Input:

```python
solve(['l', 'o', 'w', 'l', 'o', 'w'], 'l', 'o', 'lo')
```

Output:

```text
['lo', 'w', 'lo', 'w']
```

**Example 2**

Input:

```python
solve(['a', 'a', 'a'], 'a', 'a', 'aa')
```

Output:

```text
['aa', 'a']
```

## Theory

### The simple version

Byte-Pair Encoding learns a subword vocabulary by repeatedly fusing the most frequent adjacent pair into a new symbol. Each learned merge is then replayed in order when tokenising new text, so common words become single tokens and rare words fall apart into familiar pieces.

### One merge

Scan left to right; when `tokens[i], tokens[i+1] == (a, b)`, emit `merged` and skip both tokens, otherwise emit `tokens[i]`.

### Why it matters

- BPE builds a subword vocabulary by repeatedly merging the most frequent adjacent pair.
- Each learned merge is replayed in order to tokenise new text.

### How it works

1. Scan the tokens from left to right.
2. If the current and next token equal the pair, emit the merged token and skip both.
3. Otherwise emit the current token.

### Worked example

For $(l,o,w,l,o,w)$ and the pair $(l,o)$: the first two merge into `lo`, then `w` is kept, then the second $(l,o)$ merges and `w` is kept, giving ['lo', 'w', 'lo', 'w'].

## Explanation

Skipping both tokens after a match guarantees non-overlapping merges: in `['a','a','a']` with the pair `('a','a')` only the first two merge. The merged symbol is supplied by the caller, so it need not be the concatenation of the parts.
