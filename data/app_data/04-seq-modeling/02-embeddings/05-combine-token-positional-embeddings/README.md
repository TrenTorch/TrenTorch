---
name: seq-embeddings-combine-token-positional
title: Combine token and positional embeddings
tags: [nlp, transformers, embeddings]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every previous question in this track built one HALF of what a Transformer's input actually needs: `[01-token-embedding-lookup]` produces a vector encoding WHAT each token is, and `[03-sinusoidal-positional-encoding]`/`[04-learned-positional-embedding]` produce a vector encoding WHERE each token sits in the sequence. Neither alone is enough: a model that only sees "what" has no sense of word order at all (the "the dog bit the man" problem `[03-sinusoidal-positional-encoding]`'s Statement raised directly); a model that only saw "where" would have no idea WHICH word is actually at each position. This question is the simplest possible way to combine both signals into a single representation: just ADD them together, element-wise.

Addition (rather than, say, concatenation) might look like it should destroy information, mixing "what" and "where" into the same numbers rather than keeping them in separate dimensions, but it works remarkably well in practice, and is what the original Transformer paper actually does. Part of why: `embed_dim` is typically large (512, 768, or more), so there's enormous room for the token-identity signal and the positional signal to occupy substantially different, only lightly-overlapping DIRECTIONS within that high-dimensional space, without erasing each other, a phenomenon closely related to why high-dimensional random vectors tend to be nearly orthogonal to each other purely by chance.

### From theory to code

Implement `combine_embeddings(token_embeddings, positional_embeddings)`. `token_embeddings` has shape `(batch_size, seq_len, embed_dim)`; `positional_embeddings` has shape `(seq_len, embed_dim)` (the SAME positional encoding is reused for every sequence in the batch, since position 0 means the same thing regardless of which sequence it's part of). Add them together, letting NumPy's broadcasting handle applying the same `(seq_len, embed_dim)` positional table across every item in the batch.

### Constraints

- The output shape must match `token_embeddings`'s shape exactly, `(batch_size, seq_len, embed_dim)`.
- `positional_embeddings` (no batch dimension) must be broadcast identically across every sequence in the batch, not resized or tiled manually.
- Must be a pure element-wise addition, no scaling, normalization, or other transformation applied.

### Hints

<details>
<summary>Hint 1</summary>

`token_embeddings + positional_embeddings` is the entire implementation: NumPy's broadcasting rules automatically align `positional_embeddings`'s `(seq_len, embed_dim)` shape against `token_embeddings`'s trailing two dimensions, applying it identically across the leading `batch_size` dimension.

</details>

<details>
<summary>Hint 2</summary>

No reshaping, tiling, or explicit loop over the batch dimension is needed, or even correct, broadcasting handles the batch dimension automatically as long as the two arrays' TRAILING dimensions (`seq_len, embed_dim`) already match.

</details>

## Theory

### The simple version

Layering two transparent overlays on top of a map: one overlay shows terrain (what's actually AT each location, the "what"), the other shows a coordinate grid (WHICH location you're looking at, the "where"). Looking at both overlays stacked together, you get a single combined view that tells you both what's there AND exactly where it is, without either overlay needing to be redrawn or resized to accommodate the other, they were designed to sit directly on top of each other from the start.

### The formula

```
combined[b, pos, :] = token_embeddings[b, pos, :] + positional_embeddings[pos, :]
```

for every batch item `b` and position `pos`. NumPy's broadcasting computes exactly this for the whole batch at once: `positional_embeddings`'s `(seq_len, embed_dim)` shape is treated as if it had an implicit leading `batch_size` dimension of size 1, which broadcasting then automatically repeats across the REAL `batch_size` dimension.

### How PyTorch actually implements this

A real Transformer's input-embedding stage computes exactly this sum, `token_embed(input_ids) + positional_embed(positions)`, directly in PyTorch using ordinary tensor `+`, which follows the identical broadcasting rules as NumPy (PyTorch's broadcasting semantics were deliberately designed to match NumPy's). `[04-transformer-block]`'s residual/skip connections, covered later in this curriculum, use this exact same "just add two tensors together, let broadcasting and high dimensionality do the work" pattern repeatedly throughout a Transformer's architecture, this simple addition here is the FIRST of many such additions the network performs on its way from raw input to final output. A subtlety worth flagging: after this token+position sum, most real Transformer implementations immediately apply a `LayerNorm` (`Layer Normalization, forward`, in `[05-transformer-block]`, later in this curriculum) to the combined result, stabilizing the combined embedding's scale before it enters the first attention layer, this question deliberately stops at the raw addition, the exact point where the "what" and "where" signals first genuinely merge into one representation.

## Explanation

`combine_embeddings` returns `token_embeddings + positional_embeddings` directly: NumPy's broadcasting rules align the two arrays' trailing dimensions (`seq_len` and `embed_dim`, which match exactly between the two inputs), and automatically apply `positional_embeddings` identically across every item in `token_embeddings`'s leading `batch_size` dimension, producing a combined array of `token_embeddings`'s full `(batch_size, seq_len, embed_dim)` shape with no explicit looping, tiling, or reshaping required.
