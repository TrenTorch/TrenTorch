---
name: vision-vit-encoder-block
title: 'Feed Through the Transformer Block, Unmodified'
tags: [computer-vision, transformers, vision-transformer]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Every step so far — patchify, patch embedding, CLS token + position embedding — existed purely to reshape an image into something that looks EXACTLY like a language transformer's input: a sequence of `d_model`-dimensional vectors. This question is the payoff for that work: the transformer block itself needs no vision-specific code whatsoever. Self-attention computes relationships between sequence positions using nothing but dot products and softmax — it has no built-in concept of "image" or "sentence," so a block already built and tested for language modeling works on patch sequences without a single line changed.

### From theory to code

Theory says: this curriculum already has a fully assembled, tested transformer block (`05-transformers-llm/01-transformer-block/06-assemble-full-block`). It expects a batch dimension (`(batch, seq_len, d_model)`); a single image's sequence has none. Add a batch dimension of size 1, run the existing block completely unmodified, then remove the batch dimension from the result.

Implement `vit_encoder_block(sequence, num_heads, ...)` against that reasoning.

### Constraints

- `sequence`: shape `(seq_len, d_model)` — the output of `03-cls-token-position-embedding`, no batch dimension.
- All other parameters are passed straight through to `transformer_block_forward`, unchanged.
- Returns shape `(seq_len, d_model)` — same shape as `sequence`.
- `sequence` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`sequence[None, :, :]` inserts a new axis at the front, turning `(seq_len, d_model)` into `(1, seq_len, d_model)` — a "batch" of exactly one image.

</details>

<details>
<summary>Hint 2</summary>

`transformer_block_forward(batched_sequence, num_heads, ...)` returns shape `(1, seq_len, d_model)` — index `[0]` on the result strips the batch dimension back off.

</details>

## Theory

### The simple version

Think of the transformer block as a translator who only ever reads sentences, never learns anything about grammar being English versus French versus any other language — it just processes whatever sequence of tokens it's handed, purely by looking at relationships between tokens. Handing it a sequence of image patches instead of words doesn't confuse it in the slightest, because from its perspective, a sequence is a sequence: it was never looking at "words" to begin with, only at vectors and the relationships attention computes between them.

### The formula

```text
batched  = sequence[None, :, :]                          # (seq_len, d_model) -> (1, seq_len, d_model)
output   = transformer_block_forward(batched, num_heads, ...)
return output[0]                                          # (1, seq_len, d_model) -> (seq_len, d_model)
```

### How PyTorch actually implements this

This is precisely why `torchvision.models.vit_b_16` (and every other real ViT implementation) reuses the exact same `nn.TransformerEncoderLayer` class that language models use — no ViT-specific transformer block exists anywhere in PyTorch, because none is needed. The famous finding behind the original "An Image is Worth 16x16 Words" ViT paper is essentially this fact turned into a research result: once an image is reshaped into a sequence the right way, a completely off-the-shelf, unmodified transformer architecture is competitive with (and at large enough scale, better than) purpose-built convolutional architectures.

## Explanation

`sequence[None, :, :]` uses NumPy's `None` indexing to insert a new length-1 axis at position 0, turning the `(seq_len, d_model)` array into `(1, seq_len, d_model)` — exactly the batch-of-one shape `transformer_block_forward` expects, since it's written generically for any batch size. Passing every other parameter straight through unchanged is the entire point: nothing about attention, layer normalization, residual connections, or the feedforward sublayer needs to know or care that its input happens to represent image patches rather than word embeddings. `output[0]` then indexes into the batch dimension to pull out the single image's result, restoring the original `(seq_len, d_model)` shape — the wrapping and unwrapping is pure bookkeeping around a transformer block that does, quite literally, nothing different for vision than it does for language.
