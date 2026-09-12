---
name: txf-llmeng-sequence-packing
title: 'Sequence packing: concatenating short examples to fill a fixed context window'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A model trains on fixed-length windows of `context_length` tokens, but real training examples come in wildly varying lengths, many of them far SHORTER than `context_length`. Padding every short example up to the full context length individually (a common, simple approach) wastes an enormous amount of compute: `[03-attention-quadratic-complexity]` already showed attention's cost scales with sequence length, so running a mostly-padding sequence through the model spends real compute on positions that carry no actual information at all. Sequence packing fixes this directly: concatenate MANY short examples end-to-end into one long stream, then chop that stream into fixed-length `context_length` chunks, so nearly every position in every training batch is genuine content, only the very LAST chunk of the whole stream needs any padding at all.

This creates a genuinely new problem, though: after packing, two UNRELATED examples can end up sitting right next to each other within the same `context_length` window, and an ordinary `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask alone would happily let a later example's tokens attend BACKWARD into an entirely unrelated earlier example, just because they happen to share a packed window, corrupting what each example's attention actually "sees." The fix: track which original example every packed position came from, and additionally mask out any attention that would cross a document boundary, even when ordinary causality alone would permit it.

### From theory to code

Implement `pack_sequences(examples, context_length, pad_token)`, concatenating and chunking, tracking each packed position's original example via a parallel `doc_ids` array, and `build_intra_document_mask(doc_ids)`, an additive mask combining ordinary causality with a "same document only" restriction.

### Constraints

- Examples are concatenated in order, then chopped into `context_length`-sized chunks; only the FINAL chunk of the whole concatenated stream may need padding (with `pad_token`).
- `doc_ids` tracks the ORIGINAL example index for every packed position, `-1` for padding positions.
- `build_intra_document_mask`'s attention rule: position `i` may attend to position `j` only if `j <= i` (ordinary causality) AND `doc_ids[j] == doc_ids[i]` (same original example) AND `doc_ids[i] != -1` (not itself padding).
- A packed sequence's chunk BOUNDARIES may (and typically will) fall in the MIDDLE of an original example, when that example is longer than what's left in the current chunk; the example simply continues into the next chunk, still tagged with its own `doc_ids`.

### Hints

<details>
<summary>Hint 1: Packing</summary>

```python
all_tokens, all_doc_ids = [], []
for doc_id, example in enumerate(examples):
    all_tokens.extend(example)
    all_doc_ids.extend([doc_id] * len(example))

for start in range(0, len(all_tokens), context_length):
    chunk = all_tokens[start:start + context_length]
    # pad the LAST chunk only, if it's short
```

</details>

<details>
<summary>Hint 2: The intra-document mask</summary>

```python
doc_ids_arr = np.array(doc_ids)
causal = np.arange(len(doc_ids))[None, :] <= np.arange(len(doc_ids))[:, None]
same_doc = doc_ids_arr[None, :] == doc_ids_arr[:, None]
not_padding = doc_ids_arr[:, None] != -1
allowed = causal & same_doc & not_padding
return np.where(allowed, 0.0, -np.inf)
```

</details>

## Theory

### The simple version

`[02-causal-mask]`'s ordinary reader flips through a bound book, only ever looking backward at pages already read. Packed training data is like several SHORT, UNRELATED pamphlets bound together into one physical volume purely to save shelf space (fill the context window efficiently), with no blank pages between them. A reader who only respects "don't look at pages not yet reached" would accidentally treat the END of one pamphlet as connected to the START of a completely different, unrelated one just because they're bound side by side. The intra-document mask is the reader additionally checking "is this page actually part of the SAME pamphlet I'm currently reading," refusing to reference anything from a different pamphlet even if it's technically an earlier page in the bound volume.

### The formula

```
concatenated = example_1 + example_2 + ... + example_N
chunks = split(concatenated, context_length)     # pad only the LAST chunk

allowed(i, j) = (j <= i) AND (doc_ids[j] == doc_ids[i]) AND (doc_ids[i] != -1)
mask(i, j) = 0 if allowed(i, j) else -inf
```

### How PyTorch actually implements this

Nothing in core `torch.nn` implements packing directly (a data-pipeline and masking concern, not a model architecture change), but real large-scale LLM training pipelines (documented in most major open LLM technical reports) use exactly this pattern, often called "packing with document masking" or "intra-document attention masking," and some efficient attention implementations (variants of `[04-flash-attention]`'s kernel) support this mask pattern natively via a compact "cumulative sequence lengths" representation rather than materializing the full `(seq_len, seq_len)` mask this question builds explicitly, for the same memory-efficiency reasons `[04-flash-attention]` itself was motivated by. Getting the masking wrong (packing examples together WITHOUT the intra-document restriction) is a real, documented failure mode: the model ends up training on spurious cross-example "context" that will never exist at actual inference time, when examples aren't artificially concatenated together.

## Explanation

`pack_sequences` first concatenates every example into one long token stream, building a parallel `doc_ids` stream tagging every token with which original example it came from, then chops both streams into `context_length`-sized chunks, padding only the very last chunk (with `pad_token` for tokens, `-1` for its `doc_ids`) if the total concatenated length doesn't divide evenly. `build_intra_document_mask` combines three conditions via a boolean AND: ordinary causality (`j <= i`), same-document membership (`doc_ids[j] == doc_ids[i]`), and non-padding (`doc_ids[i] != -1`), converting the combined boolean grid to an additive mask exactly like `[02-causal-mask]`'s own `0`/`-inf` convention. The result: attention still flows normally WITHIN each packed example (ordinary causal behavior, unaffected by packing), but is completely severed at every packed boundary, so a model trained on packed data never learns to rely on cross-example "context" that was never actually meaningful, only ever an artifact of how the training batch happened to be assembled.
