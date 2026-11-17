---
name: problem-184-bpe-pair-counting
title: 'BPE Pair Counting'
tags: [problemset, transformer-llm, tokenization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-language-modelling-attention-llms|NLP'
topic: 'tokenization'
hint: 'Counter over zip(seq, seq[1:]) for every sequence; most_common(1)'
tools: [NumPy]
---

## Statement

Count adjacent symbol pairs across a corpus and return the most frequent one, as in the first step of every Byte-Pair-Encoding merge. `corpus` is a list of sequences (lists or strings of symbols). Ties go to the pair that appeared first.

Implement `solve(corpus)`.

**Returns.** Return a tuple `((left, right), count)`. The corpus must contain at least one adjacent pair.

### Examples

**Example 1**

Input:

```python
solve([['l', 'o', 'w'], ['l', 'o', 'w', 'e', 'r']])
```

Output:

```text
(('l', 'o'), 2)
```

**Example 2**

Input:

```python
solve([['a', 'b', 'a', 'b']])
```

Output:

```text
(('a', 'b'), 2)
```

## Theory

### The simple version

BPE builds a vocabulary bottom-up. It starts with single characters, then repeatedly finds the most frequent pair of neighbouring symbols and fuses it into a new symbol. Frequent words end up as single tokens, and rare words are split into reusable pieces.

### One step

$$(a,b)^*=\arg\max_{(a,b)}\;\#\{\text{adjacent occurrences of }a\,b\}$$

### Why it matters

- BPE builds a subword vocabulary from the most frequent adjacent pair.
- Frequent words become single tokens; rare ones split into pieces.

### How it works

1. Count pairs within each sequence.
2. Return the most frequent (first seen on ties).

### Worked example

`low` gives $(l,o),(o,w)$ and `lower` gives $(l,o),(o,w),(w,e),(e,r)$. $(l,o)$ and $(o,w)$ both occur twice; $(l,o)$ appeared first: (('l', 'o'), 2).

## Explanation

Pairs are counted within each sequence only, never across the boundary between two sequences. In the first example `('l', 'o')` and `('o', 'w')` each occur twice; `('l','o')` was seen first, so it wins the tie. The count decides which merge to learn next.
