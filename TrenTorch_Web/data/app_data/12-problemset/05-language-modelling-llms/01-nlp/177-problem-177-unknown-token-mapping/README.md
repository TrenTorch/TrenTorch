---
name: problem-177-unknown-token-mapping
title: 'Unknown Token Mapping'
tags: [problemset, sequence-models-attention, tokenization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: '[vocab.get(t, unk_id) for t in tokens]'
tools: [NumPy]
---

## Statement

Map tokens to integer ids with a vocabulary dict, using `unk_id` for every token that is not in the vocabulary.

Implement `solve(tokens, vocab, unk_id)`.

**Returns.** Return a list of ids with the same length as `tokens`.

### Examples

**Example 1**

Input:

```python
solve(['the', 'cat', 'zzz'], {'the': 1, 'cat': 2}, 0)
```

Output:

```text
[1, 2, 0]
```

**Example 2**

Input:

```python
solve([], {'a': 1}, 0)
```

Output:

```text
[]
```

## Theory

### The simple version

A model has a fixed vocabulary, but text contains words it has never seen. Instead of failing, unseen words are replaced by a special _unknown_ id, so the model can still process the sentence, just without knowing that word.

### The rule

$$\text{id}(w)=\begin{cases}\text{vocab}[w]&w\in\text{vocab}\\\text{unk\_id}&\text{otherwise}\end{cases}$$

## Explanation

`dict.get` with a default does the lookup and the fallback in one step. Subword tokenisers (BPE, WordPiece) make unknown tokens rare by splitting an unseen word into known pieces instead.
