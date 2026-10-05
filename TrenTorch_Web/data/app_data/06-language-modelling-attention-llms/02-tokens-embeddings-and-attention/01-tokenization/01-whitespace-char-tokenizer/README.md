---
name: seq-tokenization-whitespace-char
title: Whitespace/character tokenizer
tags: [nlp, tokenization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every question in this Part, and everything a language model does, starts from the same unavoidable first step: raw text (a sequence of Unicode characters) has to be chopped up into discrete units, TOKENS, before any of the math this curriculum has built so far (`[03-dl-training/02-layers/01-linear-forward]`'s matrix multiplications, `[02-deep-learning-core]`'s autograd engine) can be applied to it at all. A neural network has no native way to consume "the letter c followed by the letter a followed by the letter t"; it needs a fixed, finite VOCABULARY of tokens, each one identified by an integer id, so text can become a sequence of numbers a network can actually process.

The two simplest possible strategies for choosing what counts as "one token" sit at opposite extremes. Whitespace tokenization treats each SPACE-SEPARATED word as one token: fast, and each token usually carries a lot of meaning, but the vocabulary needed to cover a language is enormous (every inflected form of every word, "run," "runs," "running," "ran," all become entirely separate, unrelated tokens), and any word never seen during training becomes an unrecognizable "unknown" token, no matter how similar it is to a known one. Character tokenization treats each INDIVIDUAL character as one token: the vocabulary is tiny (just the alphabet, digits, and punctuation), and literally no input text can ever be truly "unknown," but sequences become much LONGER (a 5-letter word becomes 5 tokens instead of 1), which makes it far harder for a model to learn long-range structure. `BPE: single merge step`, later in this track, is the practical middle ground essentially every modern LLM actually uses, built by starting from character tokenization and progressively merging frequently-adjacent pairs.

### From theory to code

Implement `whitespace_tokenize(text)`, splitting `text` into a list of tokens on whitespace, and `char_tokenize(text)`, splitting `text` into a list of its individual characters.

### Constraints

- `whitespace_tokenize` must collapse any run of consecutive whitespace (multiple spaces, tabs, newlines) into a single split point, and must drop leading/trailing whitespace entirely (no empty-string tokens from it).
- `char_tokenize` must return one token per character, INCLUDING whitespace and punctuation characters (unlike `whitespace_tokenize`, nothing gets dropped or collapsed).
- Both functions must work correctly on an empty string input (`whitespace_tokenize("")` returns `[]`; `char_tokenize("")` also returns `[]`).

### Hints

<details>
<summary>Hint 1</summary>

Python's built-in `str.split()`, called with NO arguments, already does exactly the whitespace-collapsing, leading/trailing-stripping behavior this question needs: `"  hello   world  ".split()` gives `['hello', 'world']`.

</details>

<details>
<summary>Hint 2</summary>

`list(text)` converts any string directly into a list of its individual characters, `list("cat")` gives `['c', 'a', 't']`, this already handles whitespace and punctuation as their own tokens with no special-casing needed.

</details>

## Theory

### The simple version

Deciding how to divide a sentence into "chunks" when teaching someone a new language: teaching whole WORDS is fast to get started with, but every new word they haven't seen yet is a dead end; teaching individual LETTERS means they can technically sound out anything, but reading even a short sentence letter-by-letter is painfully slow and easy to lose the thread of. Whitespace and character tokenization are the two ends of exactly this same tradeoff, applied to how a neural network "reads."

### The formula

There's no numeric formula here, these are direct string-processing operations:

```
whitespace_tokenize(text) = text.split()          # splits on any whitespace run, strips ends
char_tokenize(text) = list(text)                   # one token per character
```

### How PyTorch actually implements this

PyTorch itself has no tokenizer of its own (tokenization is a text-preprocessing concern, upstream of any tensor math); the Hugging Face `tokenizers`/`transformers` libraries are the standard tools used in practice, and they implement exactly this same spectrum of granularity: `BasicTokenizer` (whitespace-based, an early preprocessing step inside BERT's tokenizer), byte-level and character-level tokenizers, and, most commonly in production, subword tokenizers (BPE, WordPiece, SentencePiece's Unigram algorithm) that sit deliberately between these two extremes, exactly the middle ground `BPE: single merge step` builds toward next in this track. Whichever granularity a real model uses, the OUTPUT of this tokenization step feeds directly into `[02-token-embedding-lookup]`, later in this same track: each token id becomes an index into a lookup table of learned vectors, the actual numeric representation the rest of the network operates on.

## Explanation

`whitespace_tokenize` calls `text.split()` with no arguments, Python's built-in whitespace-splitting behavior: it splits on any run of one or more whitespace characters and automatically discards leading/trailing whitespace, producing exactly the word-level tokens this question asks for.

`char_tokenize` calls `list(text)`, which iterates a Python string character by character (Python strings are already iterable at the character level), producing a list with one entry per character, whitespace and punctuation included.
