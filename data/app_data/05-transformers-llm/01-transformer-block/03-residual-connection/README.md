---
name: txf-block-residual-connection
title: 'Residual/skip connection'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[03-dl-training]`'s vanishing-gradient investigations, and `[04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding]` most vividly, showed exactly why deep networks are hard to train: a gradient flowing backward through many stacked layers gets multiplied, over and over, by each layer's local Jacobian. Multiply by something a bit less than `1` fifty times in a row and the gradient vanishes to essentially nothing; multiply by something a bit more than `1` fifty times and it explodes. Either way, the earliest layers in a deep stack end up learning far more slowly, or far more unstably, than the later ones, purely as a side effect of DEPTH itself.

He et al. (2015, ResNet) introduced a strikingly simple fix: alongside each sublayer's transformation, keep an unmodified copy of the input flowing forward too, and ADD the two together, `output = x + sublayer(x)`, rather than replacing `x` outright with `sublayer(x)`. This "residual" or "skip" connection gives the gradient an alternate path back through the network that involves NO multiplication at all, only addition, and addition's local gradient is always exactly `1`, regardless of depth. Every modern deep architecture, Transformers very much included, is built almost entirely out of blocks wrapped in residual connections, precisely because this is what makes stacking dozens or hundreds of layers actually trainable in practice.

### From theory to code

Implement `residual_connection(x, sublayer_output)`, a direct elementwise addition, and `residual_connection_backward(grad_output)`, the backward pass through that addition, which the "Assemble one full block" question, later in this track, will wire directly into a Transformer block's attention and feed-forward sublayers.

### Constraints

- `residual_connection` is a plain elementwise sum: `x + sublayer_output`, nothing more.
- `residual_connection_backward` returns `(grad_x, grad_sublayer_output)`: BOTH gradients equal `grad_output` itself, unchanged (the local gradient of addition with respect to either input is always `1`).
- Shapes of `x` and `sublayer_output` always match (the sublayer is designed to preserve `x`'s shape exactly, so no broadcasting is needed here).

### Hints

<details>
<summary>Hint 1: Forward</summary>

`return x + sublayer_output`. There is genuinely nothing more to this function; its entire value comes from HOW it's used, not from any computational complexity.

</details>

<details>
<summary>Hint 2: Backward</summary>

For `z = a + b`, `dz/da = 1` and `dz/db = 1` everywhere, so by the chain rule, `grad_a = grad_output * 1 = grad_output` and `grad_b = grad_output * 1 = grad_output`: both gradients are just `grad_output`, unchanged, handed back to both of the addition's inputs.

</details>

## Theory

### The simple version

A relay race where, alongside the runner actually carrying the baton forward (the sublayer's transformation), there's also a direct radio link from the start line straight to the finish line (the skip connection), carrying the original signal untouched. If something goes wrong partway through the relay (a layer that, mid-training, isn't contributing anything useful yet), the signal can still reach the end via the direct link, rather than being entirely lost or garbled by however many runners stand between start and finish.

### The formula

```
forward:  output = x + sublayer(x)
backward: grad_x           = grad_output   (via the skip path)
          grad_sublayer(x) = grad_output   (via the sublayer path)
```

Critically, `grad_x` here is the gradient flowing back along the SKIP path specifically; `x` also independently receives whatever gradient flows back THROUGH `sublayer(x)` itself (computed by that sublayer's own backward pass), so a residual block's TOTAL gradient with respect to `x` is the sum of both contributions, the direct pass-through path plus whatever additional signal the sublayer itself computes.

### How PyTorch actually implements this

There is no dedicated `torch.nn.Residual` layer, because the operation is simply Python's `+` applied to two tensors inside a model's own `forward` method (e.g. `x = x + self.attention(x)`), and `autograd` handles the backward pass through that addition exactly as described here, automatically, with no special-casing required. `[06-assemble-full-block]`, later in this track, wraps BOTH the attention sublayer and the feed-forward sublayer this way, and `Pre-norm vs. post-norm`, in the next track, examines a real, consequential design choice about exactly where this addition sits relative to `[01-layer-normalization-forward]`'s normalization step.

## Explanation

`residual_connection` is `x + sublayer_output`, a direct elementwise sum with no other computation. `residual_connection_backward` reflects addition's simplest possible local gradient: since `d(a+b)/da = 1` and `d(a+b)/db = 1` everywhere, the incoming `grad_output` is handed back UNCHANGED to both `grad_x` and `grad_sublayer_output`, no scaling, no reshaping. This is precisely what gives residual connections their training-stability benefit: a gradient traveling back along the skip path is never multiplied by anything, so stacking many residual blocks (`[07-stack-blocks]`) never causes THIS path to vanish or explode with depth, unlike the repeated-multiplication gradient path `[04-seq-modeling/03-recurrent-neural-networks/03-bptt-vanishing-exploding]` demonstrated for recurrent networks.
