---
name: potd-raw-embedding-lookup
title: 'THE RAW EMBEDDING LOOKUP'
tags: [transformers]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Transformers

---

### Story

An Azure Cognitive Services text pipeline needs the single most basic operation in any transformer:
turning token ids into vectors via table lookup, before any positional encoding or attention
touches them.

---

### The Math

Given embedding matrix `E` of shape `(V, d)` and a sequence of token ids, return `E[ids]`.

### Input Format

```
V d
E (V x d, row-major)
n
id_1 ... id_n
```

### Output Format

`n x d` matrix, one row per token, 6 decimals.

### Constraints

- `1 <= V <= 10^5`, `1 <= d <= 512`, `1 <= n <= 10^4`, ids in `[0, V-1]`
- Time limit: 1.0 second.

---

### Example

**Input**

```
4 2
0.1 0.2
0.3 0.4
0.5 0.6
0.7 0.8
3
2 0 3
```

**Output**

```
0.500000 0.600000
0.100000 0.200000
0.700000 0.800000
```

## Theory

### The simple version

An embedding table is just a lookup: row i is the vector for token i. Looking a token up is nothing more than reading the matching row out of the table.

### It's an index, not a transpose

`E` is given shaped `(V, d)`: row `i` is the embedding for token `i`. The only real failure mode
here is accidentally treating `E` as `(d, V)`, which produces a shape that looks plausible whenever
`V != d` happens to coincide, but is simply wrong. Testing with `V != d` catches a transpose bug
that a square `V == d` case would hide.

### Repeats and over-length sequences are both fine

A token id can repeat any number of times in the same sequence; each occurrence looks it up
independently and returns the same row. Because ids can repeat, a sequence length `n` larger than
the vocabulary size `V` is completely valid, not a contradiction.

### Direct indexing, not a scan

At `V = 10^5` and `d = 512`, looking up each id by scanning the vocabulary for a match instead of
indexing directly into `E` would be far slower than needed; a table lookup is, definitionally,
direct indexing.

## Explanation

`embedding_lookup` returns `E[ids]`, NumPy's own fancy indexing: given an array of integer indices,
`E[ids]` builds a new array by pulling row `ids[k]` of `E` into row `k` of the output, for every `k`
at once. This is a direct index operation, not a search, so it stays fast regardless of how large
`V` is, and repeated ids in `ids` naturally produce repeated rows in the output with no special
handling.
