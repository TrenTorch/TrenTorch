---
name: seq-embeddings-learned-positional-embedding
title: Learned positional embedding
tags: [nlp, transformers, embeddings]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[03-sinusoidal-positional-encoding]` solved the "tell the model where each token sits" problem with a fixed, hand-derived FORMULA, sine and cosine waves at carefully chosen frequencies, never updated during training. There's a simpler, more direct alternative: just let position 0, position 1, position 2, ... each have their OWN dedicated, freely learnable vector, exactly the same idea as `[01-token-embedding-lookup]`'s token embedding table, except the thing being looked up is a POSITION instead of a token identity. Gradient descent then figures out, entirely from the training data, whatever positional pattern turns out to actually be useful, rather than the model being locked into the specific sinusoidal pattern chosen in advance.

The tradeoff this simplicity introduces is real and worth naming directly: a learned positional embedding table has a FIXED maximum length (`position_table`'s number of rows), baked in at model-construction time, and it has genuinely never seen, let alone learned anything useful about, any position beyond that maximum. A model trained this way, given a sequence LONGER than any it saw during training, has no learned embedding to look up for those extra positions at all. `[03-sinusoidal-positional-encoding]`'s fixed formula, by contrast, can simply be COMPUTED for any position, including ones far beyond anything seen during training, which is part of why some architectures still prefer the sinusoidal (or RoPE, the most modern approach, covered later in this track) formulation specifically for its ability to generalize to longer sequences.

### From theory to code

Implement `learned_positional_embedding(seq_len, position_table)`. `position_table` has shape `(max_seq_len, embed_dim)`, a genuinely trainable parameter (unlike `[03-sinusoidal-positional-encoding]`'s fixed table). Return its first `seq_len` rows, one per position, in order.

### Constraints

- Row `0` of the result must be `position_table`'s row `0` (position 0's embedding), row `1` must be `position_table`'s row `1`, and so on, in order, with no reordering.
- The result's shape must be exactly `(seq_len, embed_dim)`.
- Must not modify `position_table` itself.

### Hints

<details>
<summary>Hint 1</summary>

Since positions are always used IN ORDER, starting from 0, no arbitrary id-based lookup (like `[01-token-embedding-lookup]`'s fancy indexing) is needed here at all, just a plain slice: `position_table[:seq_len]`.

</details>

<details>
<summary>Hint 2</summary>

A NumPy slice (as opposed to fancy indexing with an array of indices) returns a VIEW into the original array by default, not a copy, this is fine here since the function is only ever meant to READ from `position_table`, never write to the returned result in a way that should affect the original table.

</details>

## Theory

### The simple version

Reserved parking spots, numbered 1 through 50, each permanently assigned to a specific employee. Unlike a general-purpose visitor spot that can flexibly fit ANY visitor's car (the way `[01-token-embedding-lookup]`'s embedding table can look up ANY token id, in any order, as many times as needed), spot number 5 always belongs to employee 5, and there simply IS no spot 51 if a 51st employee shows up, the lot's fixed maximum capacity is a hard, unavoidable limit. A learned positional embedding table has exactly this same fixed-capacity structure: `max_seq_len` reserved "spots," one per position, each independently learned, and nothing beyond that capacity.

### The formula

```
learned_positional_embedding(seq_len, position_table) = position_table[0 : seq_len]
```

Trivial as a formula (a plain slice), but the CONCEPTUAL structure is the substantive part: `position_table` is trained exactly like any other layer's weights (via `[03-dl-training/02-layers/05-module-base-class]`'s `register_parameter`, picked up by `.parameters()`, updated by whichever optimizer from `[03-dl-training/01-optimizers]` the model uses), the only thing distinguishing it from `[01-token-embedding-lookup]`'s token embedding table is WHAT it's indexed by (position vs. token identity) and HOW it's indexed (a fixed, in-order slice vs. an arbitrary, id-driven gather).

### How PyTorch actually implements this

This is typically implemented as just another plain `nn.Embedding` layer (identical mechanically to `[01-token-embedding-lookup]`'s `torch.nn.Embedding`), but called with a fixed, always-increasing index sequence (`torch.arange(seq_len)`) rather than actual token ids, GPT-2's original implementation uses exactly this approach: a learned `wpe` (word position embedding) table alongside its learned `wte` (word token embedding) table. This is precisely why GPT-2-family models have a hard, architecturally-fixed maximum context length (GPT-2's original models topped out at 1024 tokens): `wpe` simply has no row to return for position 1025. Modern large language models have largely moved away from plain learned positional embeddings specifically to escape this limitation, favoring `RoPE (Rotary Position Embeddings)`, later in this track, or other relative-position schemes that generalize more gracefully to sequence lengths beyond what was seen during training.

## Explanation

`learned_positional_embedding` returns `position_table[:seq_len]` directly: a plain NumPy slice selecting the first `seq_len` rows of `position_table`, in their original order, giving exactly one embedding vector per position from `0` to `seq_len - 1`.
