---
name: txf-block-assemble-full-block
title: 'Assemble one full block (attention, norm, residual, FFN, norm, residual)'
tags: [transformers]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Every piece needed to build a real Transformer block already exists somewhere in this curriculum: `[04-seq-modeling/04-attention/05-mha-concat-output-projection]`'s Multi-Head Attention lets every position gather information from every other position; `[01-layer-normalization-forward]`'s LayerNorm keeps activations at a stable scale as they flow through many stacked layers; `[03-residual-connection]`'s skip connections keep gradients flowing cleanly through depth; `[04-feedforward-sublayer]`'s FFN gives each position room for genuine per-position nonlinear computation. A Transformer block is nothing more than these four pieces, wired together in a SPECIFIC order, applied twice (once around attention, once around the FFN).

The specific ordering matters. This question implements the "Pre-Norm" arrangement (used by GPT-2 and most modern LLMs): LayerNorm is applied to the block's input BEFORE each sublayer runs, and the residual connection always adds the sublayer's output back onto the RAW (un-normalized) input, never the normalized version. `[05-transformers-llm/02-modern-transformer-architecture]`'s "Pre-norm vs. post-norm" question, immediately following this track, examines the alternative ("Post-Norm," the original 2017 Transformer paper's choice) and WHY the ordering has a real, measurable effect on how easy the resulting network is to train.

### From theory to code

Implement `transformer_block_forward`, composing the block from already-built functions:

```
normed1  = LayerNorm(x, gamma1, beta1)
attn_out = MultiHeadAttention(normed1, normed1, normed1, num_heads, weight_o, bias_o, mask)
x1       = x + attn_out                                    # residual onto the RAW x, not normed1

normed2  = LayerNorm(x1, gamma2, beta2)
ffn_out  = FeedForward(normed2, ffn_weight1, ffn_bias1, ffn_weight2, ffn_bias2)
x2       = x1 + ffn_out                                     # residual onto x1, not normed2

return x2
```

Self-attention means the SAME normalized tensor is passed as `query`, `key`, AND `value`.

### Constraints

- Two INDEPENDENT LayerNorms, each with its own `gamma`/`beta`: one before attention, one before the FFN. They are never shared.
- Each residual connection adds a sublayer's output back onto the tensor that FED INTO that sublayer's LayerNorm (its own "raw" input), never onto the normalized version.
- Self-attention: `query = key = value` = the first LayerNorm's output.
- `mask` (when given) passes straight through to `MultiHeadAttention`, unchanged.

### Hints

<details>
<summary>Hint 1: The attention half</summary>

`normed1 = layer_norm_forward(x, gamma1, beta1, eps)`, then `attn_out, _ = multi_head_attention(normed1, normed1, normed1, num_heads, weight_o, bias_o, mask=mask)`, then `x = residual_connection(x, attn_out)` (note: `x`, the ORIGINAL input to this whole function, not `normed1`).

</details>

<details>
<summary>Hint 2: The FFN half</summary>

Same pattern, one step later: `normed2 = layer_norm_forward(x, gamma2, beta2, eps)` (`x` here is the UPDATED value from Hint 1's residual add), `ffn_out = feedforward_sublayer(normed2, ffn_weight1, ffn_bias1, ffn_weight2, ffn_bias2)`, `x = residual_connection(x, ffn_out)`.

</details>

<details>
<summary>Hint 3: Verifying your own wiring</summary>

A useful self-check: if `weight_o`/`bias_o` AND `ffn_weight2`/`ffn_bias2` are all zeroed out, both sublayers contribute exactly `0` to their residual connections, so the block's output must equal its ORIGINAL input `x` exactly, regardless of what the LayerNorms computed. If your implementation doesn't satisfy this, a residual connection is very likely wired to the wrong tensor.

</details>

## Theory

### The simple version

An editorial pipeline with two independent review stages. Stage one: a piece of writing goes through a formatting pass (`[01-layer-normalization-forward]`, getting every section onto a consistent, comparable scale) before an editor cross-references it against every other section for consistency (`[04-seq-modeling/04-attention]`'s attention), and whatever the editor changes gets ADDED to the ORIGINAL draft, not to the reformatted version (`[03-residual-connection]`'s residual, preserving the original author's voice even as edits accumulate). Stage two repeats the same pattern for a second editor doing detailed per-paragraph rewriting (`[04-feedforward-sublayer]`'s FFN), again adding their changes back onto the draft that fed INTO their own formatting pass, not onto anyone else's intermediate reformatting.

### The formula

```
x1 = x  + MultiHeadAttention(LayerNorm(x,  gamma1, beta1))
x2 = x1 + FeedForward(LayerNorm(x1, gamma2, beta2))
return x2
```

Two sublayers, each following the identical "normalize, transform, add back onto what fed into the normalization" pattern, LayerNorm never appearing inside a residual path itself, only feeding INTO a sublayer that the residual then wraps around.

### How PyTorch actually implements this

`torch.nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward, norm_first=True)` implements exactly this Pre-Norm arrangement (`norm_first=False`, its default, implements the alternative Post-Norm ordering instead, examined in `[05-transformers-llm/02-modern-transformer-architecture]`'s "Pre-norm vs. post-norm" question). Real production LLMs (GPT-2 onward, LLaMA, essentially every modern large language model) use `norm_first=True`-style Pre-Norm specifically because it empirically trains more stably at large depth, without needing the careful learning-rate warmup Post-Norm models typically require to avoid early-training divergence. `[07-stack-blocks]`, immediately following this question, stacks many of these blocks in sequence, which is genuinely most of what a full Transformer/LLM architecture IS.

## Explanation

`transformer_block_forward` wires together four already-verified pieces in the Pre-Norm order: `layer_norm_forward` runs on the block's raw input `x` first, producing `normed1`, which becomes `query`, `key`, AND `value` for a single self-attention call via `multi_head_attention`. That attention output is added back onto the ORIGINAL, un-normalized `x` (via `residual_connection`), producing `x1`, the first sublayer's final output. The exact same pattern repeats for the FFN half: `layer_norm_forward` runs on `x1`, `feedforward_sublayer` transforms the normalized result, and `residual_connection` adds that transformed result back onto `x1` (not onto the normalized version), producing the block's final output. Every one of these steps was independently built and independently tested earlier in the curriculum; this question's entire job is composing them in the correct order, with residual connections consistently pointing at the RAW tensor that fed each LayerNorm, never the normalized one.
