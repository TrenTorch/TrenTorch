---
name: seq-tokenization-bpe-single-merge
title: 'BPE: single merge step'
tags: [nlp, tokenization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-whitespace-char-tokenizer]` and `[02-vocabulary-building]` demonstrated the two extremes: whitespace tokens (compact sequences, unbounded vocabulary, every unseen word becomes `<unk>`) versus character tokens (tiny fixed vocabulary, but every word becomes a long sequence of individual letters). Byte-Pair Encoding (BPE) is the practical middle ground essentially every modern LLM (GPT, Llama, and many others) actually uses in production: start from character-level tokens, then repeatedly find the MOST FREQUENTLY adjacent pair of tokens anywhere in the training corpus and merge it into one new token, building progressively larger, more meaningful subword units out of the raw characters. Run enough merge steps, and common whole words end up as single tokens (since their constituent character pairs get merged together long before rarer pairs do), while genuinely rare or novel words gracefully decompose into a handful of smaller, still-meaningful subword pieces, "unbelievable" might become `["un", "believ", "able"]` rather than one opaque `<unk>`, retaining SOME of the word's structure instead of losing it entirely.

This question implements exactly ONE step of that repeated process: find the single most common adjacent pair across the whole corpus, and merge every occurrence of it. `Stretch: BPE, full training loop`, immediately after this question, wraps this single step in a loop, repeating it however many times are needed to reach a target vocabulary size.

### From theory to code

Implement `get_pair_frequencies(corpus)` (count every adjacent token pair's frequency across a corpus of token-lists), `merge_pair(corpus, pair)` (replace every occurrence of `pair` with one merged token, everywhere it appears), and `bpe_single_merge_step(corpus)` (find the single most frequent pair and merge it, returning both the updated corpus and which pair was merged).

### Constraints

- `get_pair_frequencies` counts pairs WITHIN each sequence only, never across the boundary between two different sequences in the corpus.
- `merge_pair` must merge occurrences NON-OVERLAPPING and left-to-right: after merging positions `i` and `i+1` into one token, the NEXT possible merge starts checking from position `i+2`, not `i+1`.
- `bpe_single_merge_step` must pick the pair with the HIGHEST count; ties should be broken by picking the pair that sorts alphabetically GREATER (as a tuple), for a fully deterministic result.
- The merged token is the literal string CONCATENATION of the pair's two tokens (`pair[0] + pair[1]`), not joined by any separator.

### Hints

<details>
<summary>Hint 1: get_pair_frequencies</summary>

For each `sequence` in `corpus`, loop `for i in range(len(sequence) - 1)` and increment `pair_counts[(sequence[i], sequence[i+1])]` by one. A `collections.Counter` handles the "increment, starting from zero" bookkeeping automatically.

</details>

<details>
<summary>Hint 2: merge_pair's left-to-right scan</summary>

Walk each sequence with an explicit index `i` (not a `for` loop over the sequence directly, since the step size varies): if `sequence[i], sequence[i+1]` matches `pair`, append the merged token and advance `i` by `2`; otherwise append `sequence[i]` unchanged and advance `i` by `1`.

</details>

<details>
<summary>Hint 3: bpe_single_merge_step</summary>

`max(pair_counts.items(), key=lambda kv: (kv[1], kv[0]))[0]` finds the pair with the highest count, using the pair itself as a tiebreak (Python tuples compare lexicographically, matching the alphabetically-greater tiebreak rule). Then call `merge_pair(corpus, that_pair)` and return both.

</details>

## Theory

### The simple version

Learning a new spoken language by noticing which sounds keep showing up glued together: if you hear "th" appear together constantly, you start treating "th" as one unit rather than two separate sounds, then later notice "th" plus "e" showing up together constantly too, and start treating "the" as one unit. BPE does exactly this, mechanically and repeatedly, over a training corpus's character pairs: whatever pair of tokens co-occurs most often gets promoted into a single new token, and the process repeats on the RESULT, so pairs of already-merged tokens can themselves get merged again in later steps, building up progressively larger, more meaningful chunks.

### The formula

One merge step:

```
pair_counts(pair) = number of times `pair` appears as two ADJACENT tokens, anywhere in the corpus
best_pair = argmax over all pairs of pair_counts(pair)
new_corpus = corpus with every occurrence of best_pair replaced by (best_pair[0] + best_pair[1])
```

Repeated `k` times (the full training loop `Stretch: BPE, full training loop` builds), this produces a vocabulary of the original character set plus `k` learned merges, exactly how a real BPE tokenizer's vocabulary is constructed.

### How PyTorch actually implements this

PyTorch has no BPE implementation of its own; the Hugging Face `tokenizers` library (written in Rust for speed, with Python bindings) is the standard real-world tool, and GPT-2's original BPE tokenizer (still used, with minor variations, by many modern LLMs) implements precisely this repeated merge-the-most-frequent-pair algorithm, just operating over UTF-8 BYTES rather than characters (a detail called "byte-level BPE," which sidesteps needing any special out-of-vocabulary handling at all, since every possible byte sequence, including entirely novel Unicode characters, can always be decomposed down to individual bytes as a fallback). A subtlety real BPE implementations handle that this simplified version doesn't: an explicit "end of word" marker (often written `</w>`) is usually appended to each word before running BPE, so a merged token like `"er"` at the END of a word ("teacher") can be learned as a DISTINCT token from `"er"` in the MIDDLE of a word ("term"), since these often carry different meaning (a suffix vs. a coincidental letter sequence).

## Explanation

`get_pair_frequencies` iterates every sequence and every adjacent index pair within it, incrementing a `Counter` keyed by `(sequence[i], sequence[i+1])`, giving a total frequency count for every distinct adjacent pair across the whole corpus.

`merge_pair` walks each sequence with an explicit index, checking at each position whether the CURRENT and NEXT token together match `pair`: if so, it appends the concatenated merged token and skips ahead by two positions (consuming both original tokens); otherwise it appends the current token unchanged and advances by one, ensuring merges never overlap.

`bpe_single_merge_step` calls `get_pair_frequencies` to get every pair's count, uses `max` with a `(count, pair)` sort key to find the single most frequent pair (with ties broken toward the alphabetically greater pair, since `max` naturally prefers the greater tuple on a tie), calls `merge_pair` with that winning pair, and returns both the updated corpus and the pair that was merged.
