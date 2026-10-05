---
name: lm-bigram-counts
title: Bigram Counts
tags: [language-modeling, counting]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A language model is a machine that, given what has been written so far, says how likely each possible next symbol is. The simplest honest version looks back exactly one symbol. To learn it from a list of words you count how often each symbol follows each other symbol, then read the counts as evidence. The only wrinkle is the edges of a word: a word starts and ends, and the model should learn how words start and how they stop. Adding one special boundary symbol `.` at both ends of every word turns "how words begin" and "how words end" into ordinary follow-counts.

### From theory to code

Implement `bigram_counts(words)`. It returns the count matrix and the list of symbols that labels its rows and columns. The skeleton is already in the editor.

### Constraints

- `words` is a list of non-empty strings. The symbol `.` never appears inside a word.
- The symbol list `itos` is `['.']` followed by the sorted distinct characters of all words. Row and column `i` of the matrix belong to `itos[i]`.
- Wrap each word as `.` + word + `.` and count every adjacent pair. `counts[i, j]` is the number of times `itos[j]` directly followed `itos[i]`.
- Return `(counts, itos)` with `counts` an integer array of shape `(V, V)`.

### Hints

<details>
<summary>Hint 1</summary>

Build `itos` first, then a dictionary from symbol to index so counting is one lookup.

</details>

<details>
<summary>Hint 2</summary>

`zip(seq, seq[1:])` walks adjacent pairs of the wrapped word.

</details>

<details>
<summary>Hint 3</summary>

The matrix total equals the sum over words of `len(word) + 1`, which is a handy self-check.

</details>

## Theory

### The simple version

Imagine a spreadsheet whose rows are "the letter I just saw" and whose columns are "the letter that came next". Reading a word letter by letter you put a tally mark in the cell for each step. After many words, a cell with a big tally is a common follow-up and an empty cell is a follow-up you have never seen.

### The formula

For a word $w = c_1 c_2 \dots c_n$ wrapped as $c_0 = c_{n+1} = \texttt{.}$,

$$
N_{ij} = \sum_{\text{words}} \sum_{t=0}^{n} \mathbf{1}[c_t = i,\; c_{t+1} = j]
$$

The total $\sum_{ij} N_{ij}$ equals $\sum_{w}(|w| + 1)$ because a word of length $n$ has $n + 1$ adjacent pairs once wrapped.

### How this is done in practice

This table is the whole model in a classic n-gram system, and it is the object that neural language models later learn to approximate. Production code stores it sparsely (a dictionary of dictionaries or a `Counter` of pairs) because most cells of a real vocabulary are empty. With a vocabulary of characters a dense array is fine, and NumPy's `np.add.at` can fill it in one call from index arrays.

## Explanation

The function wraps every word with the boundary symbol, maps symbols to indices through `stoi`, and increments one cell per adjacent pair. Because the boundary symbol sits at index 0, row 0 holds the start-of-word statistics and column 0 holds the end-of-word statistics, so the same table answers "how do words begin", "what follows an `a`" and "when does a word stop".
