---
name: txf-modern-encoder-decoder-arrangements
title: 'Encoder vs. decoder vs. encoder-decoder: three ways to arrange the same block'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[01-transformer-block/06-assemble-full-block]` built ONE reusable Transformer block. Nothing about that block's internal STRUCTURE changes across "BERT," "GPT," and "the original 2017 Transformer" (translation-style encoder-decoder models), the three big architectural families real systems fall into. What changes is entirely WHICH POSITIONS self-attention is allowed to see, and, for the encoder-decoder family, whether a SECOND kind of attention gets added at all.

An **encoder** (BERT-style) lets every position attend to every other position, in both directions: useful for building a representation of a COMPLETE, already-fully-visible input (classification, understanding tasks), where there's no reason to hide any part of the input from any other part. A **decoder** (GPT-style) restricts self-attention with `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask: essential for autoregressive generation, where a model must never "cheat" by looking at tokens it hasn't generated yet. An **encoder-decoder** (translation-style) uses BOTH: an encoder processes the full source sequence bidirectionally, and a decoder generates the target sequence causally, while ALSO attending to the encoder's output via a second, distinct attention call, "cross-attention," where the query comes from the decoder but the key/value come from the encoder.

### From theory to code

Implement `encoder_block_forward` (a thin wrapper around `[06-assemble-full-block]`'s block, no mask), `decoder_block_forward` (the same block, with `[02-causal-mask]`'s mask), and `encoder_decoder_cross_attention` (a direct call to `[05-mha-concat-output-projection]`'s `multi_head_attention`, with `query` from the decoder and `key`/`value` both from the encoder's output).

### Constraints

- `encoder_block_forward` passes `mask=None` to the underlying Transformer block: full bidirectional attention.
- `decoder_block_forward` builds a causal mask sized to `x`'s own sequence length and passes it through.
- `encoder_decoder_cross_attention`'s `query` is `decoder_hidden`; its `key` AND `value` are both `encoder_output`. These may have DIFFERENT sequence lengths (the source and target sentences in translation are rarely the same length).
- Cross-attention uses NO mask (the decoder is always allowed to attend to the entire, already-fully-computed encoder output).

### Hints

<details>
<summary>Hint 1: Encoder and decoder blocks</summary>

`encoder_block_forward` is exactly `transformer_block_forward(x, num_heads, mask=None, **block_params)`. `decoder_block_forward` is the same call with `mask=build_causal_mask(x.shape[-2])` instead.

</details>

<details>
<summary>Hint 2: Cross-attention</summary>

`output, _ = multi_head_attention(decoder_hidden, encoder_output, encoder_output, num_heads, weight_o, bias_o)`. Notice `query` and `key`/`value` come from genuinely DIFFERENT tensors here, unlike every self-attention call used so far in this curriculum, where all three were the same tensor.

</details>

## Theory

### The simple version

A translator working on a document. Reading and fully understanding the SOURCE document first (the encoder): they're allowed to read the whole thing back and forth, cross-referencing later sentences against earlier ones freely, since the entire source is already sitting in front of them. Writing the TRANSLATION (the decoder): they can only see what they've already written so far (causal, generation is sequential), but at every point while writing, they're free to glance back at their (complete) understanding of the source document (cross-attention) to decide what to write next.

### The formula

```
encoder_block(x)        = TransformerBlock(x, mask=None)                       # bidirectional
decoder_block(x)        = TransformerBlock(x, mask=causal_mask(len(x)))        # causal
cross_attention(dec, enc) = MultiHeadAttention(query=dec, key=enc, value=enc)   # decoder attends to encoder
```

An encoder-only model (BERT) stacks only the first. A decoder-only model (GPT, and essentially every modern LLM) stacks only the second. An encoder-decoder model (the original Transformer, T5) stacks BOTH families, with the third operation added into every decoder block, immediately after decoder self-attention.

### How PyTorch actually implements this

`torch.nn.TransformerEncoderLayer` implements the encoder case; `torch.nn.TransformerDecoderLayer` implements the decoder-with-cross-attention case directly, taking a `memory` argument (the encoder's output) that becomes cross-attention's key/value, alongside its own causally-masked self-attention. Modern LLMs (GPT, LLaMA, essentially every widely-used chat model as of this curriculum) are overwhelmingly DECODER-ONLY: cross-attention and a separate encoder stack turned out to be unnecessary for most tasks once decoder-only models were simply scaled up and trained on enough data, one of the most consequential architectural simplifications in the field's recent history. `[05-transformers-llm/03-language-model-assembly]`, later in this curriculum, builds out a decoder-only language model specifically, reflecting this modern default.

## Explanation

`encoder_block_forward` and `decoder_block_forward` both delegate directly to `[06-assemble-full-block]`'s `transformer_block_forward`, differing only in the `mask` argument: `None` for the encoder (every position visible to every other position), a freshly built causal mask (sized to the input's own sequence length) for the decoder (each position sees only itself and earlier positions). `encoder_decoder_cross_attention` calls `[05-mha-concat-output-projection]`'s `multi_head_attention` directly, with `decoder_hidden` as the query and `encoder_output` as BOTH the key and the value, letting the decoder look up relevant information from the encoder's (already fully computed, bidirectionally-attended) representation of the source sequence, with no restriction on which encoder positions it may attend to and no requirement that the two sequences share a length.
