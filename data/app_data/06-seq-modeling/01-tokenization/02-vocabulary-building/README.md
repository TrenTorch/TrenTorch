---
name: seq-tokenization-vocabulary-building
title: Vocabulary building + unknown-token handling
tags: [nlp, tokenization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-whitespace-char-tokenizer]` turns raw text into a list of string tokens, but `[02-embeddings/01-token-embedding-lookup]`'s embedding lookup, and everything downstream of it, needs INTEGER ids, not strings, a lookup table is indexed by position, not by spelling. Building that string-to-integer mapping (the "vocabulary") from a training corpus is this question's first job. The second, equally important job: a vocabulary built from a FIXED training corpus will, by definition, never contain every string that might appear in future text the model encounters, someone will eventually type a typo, a brand-new word, or a name the vocabulary has never seen. Rather than crashing or silently corrupting the input, a real tokenizer reserves one special token, conventionally called `<unk>` ("unknown"), as the fallback id for anything outside the known vocabulary.

A secondary, practical concern this question also handles: including every single token that appears even ONCE in a large training corpus can bloat the vocabulary with rare misspellings, one-off names, and noise, each of which would get its own learned embedding vector that barely ever gets a useful training signal. Filtering by a minimum frequency threshold (`min_freq`) keeps the vocabulary focused on tokens common enough to be worth a dedicated embedding.

### From theory to code

Implement `build_vocabulary(token_lists, min_freq, unk_token)`, counting every token's frequency across the whole corpus (a list of token lists), reserving id `0` for `unk_token`, and assigning ids to every OTHER token with frequency `>= min_freq`, in order of descending frequency (ties broken alphabetically, for a deterministic, reproducible result). Implement `encode_with_unk(tokens, vocab, unk_token)`, mapping a list of tokens to their ids, substituting `unk_token`'s id for anything not present in `vocab`.

### Constraints

- `unk_token` must always be assigned id `0`, regardless of whether it happens to also appear literally in the corpus.
- Tokens with frequency below `min_freq` must be EXCLUDED from the vocabulary entirely (they'll map to `<unk>` at encoding time, via `encode_with_unk`).
- Remaining tokens must be assigned ids in order of DESCENDING frequency, with ties broken ALPHABETICALLY, so the same corpus always produces the exact same vocabulary.
- `encode_with_unk` must never raise a `KeyError`: any out-of-vocabulary token maps to `unk_token`'s id instead.

### Hints

<details>
<summary>Hint 1: Counting</summary>

`collections.Counter()` with `.update(tokens)` called once per sequence in `token_lists` accumulates a total frequency count across the whole corpus in a few lines.

</details>

<details>
<summary>Hint 2: Deterministic ordering</summary>

`sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))` sorts by frequency descending (`-kv[1]`, negating to reverse the usual ascending sort) with alphabetical order (`kv[0]`) as the tiebreak, a single sort key handles both requirements at once.

</details>

<details>
<summary>Hint 3: Assigning ids</summary>

Start `vocab = {unk_token: 0}`, then loop over the sorted `(token, count)` pairs, and for each one where `count >= min_freq`, assign `vocab[token] = len(vocab)` (the CURRENT size of `vocab` is exactly the next available id, since ids are assigned in order starting from `0`).

</details>

## Theory

### The simple version

A company's employee directory, where every employee gets a unique badge NUMBER instead of using their name to look things up (names can collide, be misspelled, or belong to someone who hasn't been hired yet). A visitor whose name isn't in the directory doesn't get let in under a made-up badge number, they get routed to a single, well-defined "visitor" badge, exactly what `<unk>` does for a token the vocabulary has never seen.

### The formula

There's no numeric formula here, this is data structure construction:

```
counts = frequency of every token across the whole corpus
vocab = {unk_token: 0}
for token, count in counts, sorted by (-count, token):
    if count >= min_freq:
        vocab[token] = len(vocab)

encode_with_unk(tokens) = [vocab.get(t, vocab[unk_token]) for t in tokens]
```

### How PyTorch actually implements this

PyTorch itself has no vocabulary-building utility (this is a preprocessing concern handled by libraries like `torchtext`'s `build_vocab_from_iterator` or, more commonly today, Hugging Face `tokenizers`), but the pattern implemented here, `<unk>` reserved as a fixed low id, frequency-based filtering, is exactly what those libraries do. Real vocabularies typically reserve SEVERAL special ids beyond just `<unk>`, commonly also `<pad>` (for padding shorter sequences up to a batch's max length, so `[03-dl-training/03-training-loop/01-dataset-dataloader]`'s `DataLoader` can stack variable-length sequences into one batch tensor), `<bos>`/`<eos>` (beginning/end of sequence markers, telling a generative model where a sequence starts and ends, directly relevant to autoregressive generation later in this curriculum), and `<mask>` (used by masked-language-model pretraining objectives like BERT's). `min_freq` filtering is a genuinely important practical lever in real tokenizer vocabularies too, though modern subword tokenizers (`BPE: single merge step`, next in this track) address the same "rare/unseen token" problem somewhat differently, by decomposing an unfamiliar word into smaller, more common subword pieces rather than mapping the whole word straight to `<unk>`.

## Explanation

`build_vocabulary` accumulates a `Counter` over every token list in the corpus, then sorts the resulting `(token, count)` pairs by `(-count, token)` (descending frequency, alphabetical tiebreak), and walks that sorted list assigning each token meeting the `min_freq` threshold the next available id (`len(vocab)`, since `vocab` starts at size `1` with just `unk_token`).

`encode_with_unk` looks up each token in `vocab` via `.get(token, unk_id)`, which returns the token's real id if present, or falls back to `unk_token`'s id (looked up once, outside the loop, for efficiency) if the token is out of vocabulary.
