---
name: txf-block-stack-blocks
title: 'Stack multiple blocks'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[06-assemble-full-block]` built ONE complete Transformer block: a self-attention sublayer and a feed-forward sublayer, each wrapped in `[01-layer-normalization-forward]`'s normalization and `[03-residual-connection]`'s residual connection. A real Transformer, and every modern LLM, is overwhelmingly just MANY of these identical-in-STRUCTURE (but independently-PARAMETERIZED) blocks, stacked one after another, each block's output feeding directly into the next block's input. This is genuinely most of what "scaling up a model" means in practice: GPT-2 small has 12 blocks, GPT-3 has 96, and the largest modern LLMs stack well over a hundred, each one adding another opportunity for the representation at every position to be further refined against the rest of the sequence.

Each block in the stack has its OWN independently-learned parameters (its own attention weights, its own FFN weights, its own LayerNorm `gamma`/`beta`), never shared across blocks, so a 12-block model has 12x as many block-level parameters as a single block, even though every block runs the identical FORWARD computation `[06-assemble-full-block]` already implements.

### From theory to code

Implement `stack_transformer_blocks(x, num_heads, blocks_params, mask, eps)`. `blocks_params` is a list of dicts, one per block, each containing that block's own set of weights (`weight_o`, `bias_o`, `ffn_weight1`, `ffn_bias1`, `ffn_weight2`, `ffn_bias2`, `gamma1`, `beta1`, `gamma2`, `beta2`, the exact keyword arguments `[06-assemble-full-block]`'s `transformer_block_forward` expects). Run `x` through each block IN ORDER, each block's output becoming the NEXT block's input.

### Constraints

- Blocks run strictly IN ORDER: block `i`'s output is block `i+1`'s input, never the other way around, and never independently against the original `x`.
- `num_heads`, `mask`, and `eps` are shared across every block in the stack (a real Transformer typically uses the same head count and mask at every layer); only the WEIGHTS differ per block.
- An empty `blocks_params` list returns `x` completely unchanged (zero blocks means zero transformation).

### Hints

<details>
<summary>Hint 1: The loop</summary>

```python
for params in blocks_params:
    x = transformer_block_forward(x, num_heads, mask=mask, eps=eps, **params)
return x
```

Each iteration REASSIGNS `x` to that block's output, so the next iteration's `transformer_block_forward` call automatically receives the previous block's output as its input.

</details>

<details>
<summary>Hint 2: Unpacking each block's parameters</summary>

`**params` unpacks a block's dict directly into `transformer_block_forward`'s keyword arguments (`weight_o=params["weight_o"]`, `ffn_weight1=params["ffn_weight1"]`, and so on), so each dict in `blocks_params` needs exactly the keys `[06-assemble-full-block]`'s `transformer_block_forward` expects beyond `x`, `num_heads`, `mask`, and `eps`.

</details>

## Theory

### The simple version

`[06-assemble-full-block]`'s editorial pipeline had two editors working on one draft. Stacking blocks is handing that SAME draft through an entire chain of independent editorial teams, one after another, each team seeing only the PREVIOUS team's output (never the original raw draft), and each team applying its own distinct judgment (its own learned weights). By the time the draft reaches the last team, it has been refined through many successive, independently-parameterized passes, each building on everything every earlier team already contributed.

### The formula

```
x_0 = input
x_1 = TransformerBlock_1(x_0)
x_2 = TransformerBlock_2(x_1)
  ...
x_N = TransformerBlock_N(x_{N-1})
return x_N
```

Every `TransformerBlock_i` runs the exact same STRUCTURE (`[06-assemble-full-block]`'s attention-norm-residual-FFN-norm-residual pipeline), each with its OWN independently-learned weights.

### How PyTorch actually implements this

`torch.nn.TransformerEncoder(encoder_layer, num_layers)` implements exactly this pattern: it internally deep-copies `encoder_layer` `num_layers` times (each copy independently initialized and independently trained, never sharing weights) and chains them via a plain Python loop functionally identical to this question's, each layer's output feeding the next layer's input. `Weight tying`, later in this curriculum's `[05-transformers-llm/03-language-model-assembly]` track, examines one specific case where parameters ARE deliberately shared (between the input embedding and output projection), a deliberate exception to the "every block/layer has its own independent parameters" default this question demonstrates.

## Explanation

`stack_transformer_blocks` loops over `blocks_params`, and on each iteration reassigns `x` to `transformer_block_forward(x, num_heads, mask=mask, eps=eps, **params)`'s result, so the NEXT iteration's call automatically receives the CURRENT block's output as its input, exactly the sequential chaining a real multi-layer Transformer performs. `num_heads`, `mask`, and `eps` are passed identically to every block (matching how a real model keeps its head count and masking strategy consistent across layers), while `**params` supplies each block's own, independently-parameterized weights. With an empty `blocks_params` list, the loop body never executes, so the function returns `x` completely unchanged, the correct "zero transformation" behavior for a stack of zero blocks.
