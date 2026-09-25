---
name: seq-tokenization-encode-decode-roundtrip
title: Encode/decode round-trip
tags: [nlp, tokenization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

This track's four previous questions each built one PIECE of a real tokenizer in isolation: `[01-whitespace-char-tokenizer]` splits text into tokens, `[02-vocabulary-building]` maps tokens to ids (and handles unknowns), `[03-bpe-single-merge]` and `[04-bpe-full-training-loop]` build a smarter, learned vocabulary. This question is the payoff: wire the pieces together into the complete round trip a real tokenizer actually needs to support, `encode` (text -> a list of integer ids, ready to feed `[02-embeddings/01-token-embedding-lookup]`) and `decode` (ids -> text, needed to turn a language model's OUTPUT predictions, which are token ids, back into human-readable text).

A subtlety worth naming directly: `decode(encode(text))` is generally NOT guaranteed to reproduce `text` EXACTLY, character for character. `[02-vocabulary-building]`'s `<unk>` handling is lossy by design (an unknown word becomes `<unk>`, and there's no way to recover the original spelling from that alone), and `whitespace_tokenize` itself already collapses multiple spaces and strips leading/trailing whitespace, so even a perfectly round-tripped SEQUENCE OF TOKENS might not exactly match the original text's precise whitespace. What round-tripping IS guaranteed to preserve, for text made entirely of tokens the vocabulary actually knows, is the sequence of WORDS, in order, joined back together with single spaces.

### From theory to code

Implement `encode(text, vocab, unk_token)`, chaining `whitespace_tokenize` (already provided, reused from `[01-whitespace-char-tokenizer]`) into `encode_with_unk` (already provided, reused from `[02-vocabulary-building]`). Implement `build_inverse_vocab(vocab)`, constructing the REVERSE mapping (id -> token) from `vocab`'s forward mapping. Implement `decode(ids, vocab)`, converting each id back to its token via the inverse vocabulary and joining them with single spaces.

### Constraints

- `encode` must produce exactly what calling `whitespace_tokenize` then `encode_with_unk` in sequence would produce, reusing both rather than reimplementing their logic.
- `build_inverse_vocab` must correctly invert EVERY entry in `vocab`, including id `0` (`<unk>` or whatever the unknown token is named).
- `decode` must join tokens with a SINGLE space between each pair, matching what `whitespace_tokenize` would produce if it re-tokenized the decoded string.
- For text made entirely of tokens present in `vocab` (no `<unk>` needed), `decode(encode(text), vocab)` must exactly reproduce `text`'s WORD SEQUENCE, though not necessarily its exact original whitespace.

### Hints

<details>
<summary>Hint 1: encode</summary>

`tokens = whitespace_tokenize(text)`, then `return encode_with_unk(tokens, vocab, unk_token)`, a direct two-step chain, no additional logic needed.

</details>

<details>
<summary>Hint 2: build_inverse_vocab</summary>

A dict comprehension: `{token_id: token for token, token_id in vocab.items()}`, swapping each `(token, id)` pair's roles.

</details>

<details>
<summary>Hint 3: decode</summary>

Build the inverse vocab once (via `build_inverse_vocab`), then `tokens = [inverse_vocab[token_id] for token_id in ids]`, and `return " ".join(tokens)`.

</details>

## Theory

### The simple version

A librarian's card catalog again (as in `[03-dl-training/02-layers/05-module-base-class]`'s Theory): the catalog number LOOKS UP a book, and given a catalog number, you can find your way back to the book's actual title, that's the "decode" direction, the exact mirror image of "encode" (title -> catalog number). A well-built catalog supports looking things up in BOTH directions cleanly; a tokenizer's vocabulary is exactly this same two-way lookup structure, applied to words and integers instead of titles and shelf numbers.

### The formula

```
encode(text) = encode_with_unk(whitespace_tokenize(text), vocab)
decode(ids) = " ".join(inverse_vocab[id] for id in ids)
```

where `inverse_vocab = {id: token for token, id in vocab.items()}`.

### How PyTorch actually implements this

PyTorch itself has no tokenizer (as established throughout this track, this is a text-preprocessing library's job, most commonly Hugging Face `tokenizers`/`transformers`), but every real tokenizer library implements exactly this `encode`/`decode` pair as its primary public API, `tokenizer.encode(text)` and `tokenizer.decode(ids)` in Hugging Face's `PreTrainedTokenizer`, for instance. `decode` is specifically what a real text-generation pipeline calls at the very END of the process: `[03-dl-training/01-optimizers]`'s trained model produces a sequence of predicted token ids one at a time (covered in depth in this curriculum's later generation/decoding content), and `decode` is the final step that turns those raw integer predictions back into the human-readable text a user actually reads. Real tokenizers handle the "not a perfect character-for-character round trip" issue more gracefully than this simplified whitespace-based version: subword tokenizers like BPE (`[04-bpe-full-training-loop]`) typically DON'T insert a space between every token when decoding (since many subword tokens are meant to be glued directly onto the previous one, no space, `["un", "believ", "able"]` should decode to `"unbelievable"`, not `"un believ able"`), tracked via special marker characters (like the `Ġ` prefix GPT-2's byte-level BPE uses to denote "this token starts a new word") rather than assuming every token boundary is a word boundary.

## Explanation

`encode` calls `whitespace_tokenize(text)` to get a list of string tokens, then passes that list directly to `encode_with_unk(tokens, vocab, unk_token)`, which returns the final list of integer ids, chaining both previously-built functions with no additional logic.

`build_inverse_vocab` returns a dict comprehension swapping every `(token, id)` pair in `vocab` into `(id, token)`, producing the reverse lookup table `decode` needs.

`decode` calls `build_inverse_vocab(vocab)` once, uses it to map every id in `ids` back to its original token via a list comprehension, and joins the resulting token list with `" ".join(...)`, reconstructing a space-separated string.
