---
name: txf-modern-pre-norm-vs-post-norm
title: 'Pre-norm vs. post-norm: where LayerNorm sits, and why it changes trainability'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-transformer-block/06-assemble-full-block]` placed `[01-layer-normalization-forward]`'s LayerNorm BEFORE each sublayer (attention, then FFN), the "Pre-Norm" arrangement, with `[03-residual-connection]`'s residual always adding a sublayer's output back onto the RAW, un-normalized input. The ORIGINAL 2017 Transformer paper did the opposite: it ran each sublayer FIRST, added the residual, and normalized AFTERWARD, "Post-Norm." Both are structurally valid: the same four ingredients, just reordered. But the reordering has a real, measurable, non-cosmetic consequence for how easy the resulting network is to actually TRAIN, which is why nearly every modern LLM has converged on Pre-Norm despite Post-Norm being the historical original.

The concrete difference: in Pre-Norm, the "residual stream," the running sum of every sublayer's output added back through the network, NEVER gets renormalized. It grows, unboundedly, with every added block (nothing in the architecture ever caps it). In Post-Norm, LayerNorm is the LAST operation at every single block, so the output's scale gets re-pinned at every layer, never growing with depth. Post-Norm's bounded activations sound like the safer choice, but Xiong et al. (2020) showed the opposite is true for TRAINING dynamics: Post-Norm's gradients, at the very deepest stacks, without careful learning-rate warmup, can grow unstably large near the INPUT layers specifically (the opposite failure mode from vanishing), while Pre-Norm's gradients stay comparatively well-behaved regardless of depth, which is the actual, practical reason modern architectures default to it.

### From theory to code

Implement `post_norm_transformer_block_forward` (mirroring `[06-assemble-full-block]`'s Pre-Norm block, with the LayerNorm/sublayer order reversed), and `stack_pre_norm_blocks`/`stack_post_norm_blocks` (running the SAME block, with the SAME weights, repeatedly, to isolate the effect of depth alone).

### Constraints

- Post-Norm order: `x = LayerNorm(x + Sublayer(x))`, sublayer THEN residual THEN norm, for both the attention and FFN halves.
- `stack_pre_norm_blocks`/`stack_post_norm_blocks` reuse the exact SAME `block_params` dict at every iteration (deliberately: this isolates depth's effect from the effect of having different, independently-learned weights per block).
- Both stacking functions chain blocks sequentially: block `i`'s output feeds block `i+1`'s input.

### Hints

<details>
<summary>Hint 1: Post-Norm's attention half</summary>

`attn_out, _ = multi_head_attention(x, x, x, num_heads, weight_o, bias_o, mask=mask)`, `x = residual_connection(x, attn_out)`, `x = layer_norm_forward(x, gamma1, beta1, eps)`. Compare directly against Pre-Norm's order (normalize, THEN attend, THEN residual): this is the same three operations, reordered.

</details>

<details>
<summary>Hint 2: Post-Norm's FFN half, and the stacking loops</summary>

Identical pattern: `ffn_out = feedforward_sublayer(x, ...)`, `x = residual_connection(x, ffn_out)`, `x = layer_norm_forward(x, gamma2, beta2, eps)`. Both stacking functions are a simple `for _ in range(num_blocks): x = <block_fn>(x, num_heads, **block_params)` loop, exactly `[01-transformer-block/07-stack-blocks]`'s pattern with every block sharing one params dict instead of each having its own.

</details>

## Theory

### The simple version

`[06-assemble-full-block]`'s editorial pipeline had each editor's changes added back onto the draft that fed INTO their own review (Pre-Norm: format, then review, then add changes to the UN-formatted original). Post-Norm instead has each editor review the raw draft directly, add their changes, and only THEN reformat the COMBINED result before it moves to the next editor. Post-Norm's draft always arrives at each stage in a clean, consistently-formatted state (bounded scale); Pre-Norm's draft accumulates every editor's raw, unformatted changes on top of each other indefinitely (growing, unbounded scale), only ever getting glimpsed through a temporary, disposable "formatted view" each editor uses for their OWN review, never actually stored back into the draft.

### The formula

```
Pre-Norm:  x = x + Sublayer(LayerNorm(x))     # normalize before, residual onto raw x
Post-Norm: x = LayerNorm(x + Sublayer(x))     # normalize after, residual onto raw x, then normalize the sum
```

Both apply the SAME sublayer and the SAME residual connection; only the position of LayerNorm relative to those two operations differs.

### How PyTorch actually implements this

`torch.nn.TransformerEncoderLayer(d_model, nhead, norm_first=True)` is Pre-Norm; `norm_first=False` (PyTorch's own default, matching the original 2017 paper) is Post-Norm. Despite Post-Norm being the DEFAULT in PyTorch's own API (a historical artifact of matching the original paper), essentially every modern LLM (GPT-2 onward, LLaMA, and effectively every widely-deployed chat model as of this curriculum) explicitly opts INTO Pre-Norm, specifically because it trains stably at large depth without the fragile, hand-tuned learning-rate warmup schedules Post-Norm models otherwise need to avoid early-training divergence. `[04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding]`'s gradient-instability theme reappears here in a genuinely different guise: not exploding/vanishing from REPEATED MULTIPLICATION through time, but from where, structurally, a NORMALIZING operation sits relative to a growing residual stream across DEPTH.

## Explanation

`post_norm_transformer_block_forward` runs attention on the raw `x`, adds the residual, and only then calls `layer_norm_forward`, repeating the identical pattern for the FFN half, the exact reverse ordering from `[06-assemble-full-block]`'s Pre-Norm block. `stack_pre_norm_blocks` and `stack_post_norm_blocks` both loop their respective block function `num_blocks` times, deliberately reusing the SAME weights at every step, isolating exactly one variable: how many times the block has been applied. The measurable consequence falls directly out of the ordering: Pre-Norm's residual stream is the running, ever-growing sum `x + sublayer_1(...) + sublayer_2(...) + ...`, with LayerNorm only ever consulted as a temporary, un-stored VIEW fed into each sublayer, never written back into `x` itself, so its norm keeps growing with depth. Post-Norm's LAST operation at every block is LayerNorm itself, so the output's scale gets forcibly re-pinned (to roughly `|gamma2|`) at every single block, regardless of how many blocks came before, bounded rather than growing.
