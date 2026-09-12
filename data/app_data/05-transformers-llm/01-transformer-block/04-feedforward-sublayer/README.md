---
name: txf-block-feedforward-sublayer
title: 'Feed-forward sublayer (reuses Part 1 Linear + activation)'
tags: [transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`[04-seq-modeling/04-attention]`'s attention mechanism lets every position gather information FROM every other position, but it does so entirely through weighted AVERAGING: the output at each position is a linear combination of OTHER positions' value vectors. Averaging alone is a fairly limited kind of computation: it can blend information together, but it cannot, on its own, apply an arbitrary nonlinear transformation to what a position has just gathered. A Transformer block therefore follows its attention sublayer with a SECOND sublayer that does the opposite job: a position-wise feed-forward network, applied IDENTICALLY and INDEPENDENTLY to every position (no mixing across positions at all, unlike attention), giving the model a place to apply genuine nonlinear computation to each position's own representation.

The specific shape used almost universally: expand the `d_model`-dimensional representation UP to a much larger hidden size (`d_ff`, conventionally `4 * d_model` in the original Transformer paper), apply a nonlinearity, then project back DOWN to `d_model`. The "expand, then contract" shape gives the network many more effective parameters and much more room to represent complex per-position functions, without changing the width the rest of the block operates at.

### From theory to code

Implement `feedforward_sublayer(x, weight1, bias1, weight2, bias2)` by directly reusing two pieces already built earlier in this curriculum: `[03-dl-training/02-layers/01-linear-forward]`'s `linear_forward` for both the expansion and the projection, and `[02-deep-learning-core/02-activations/05-gelu]`'s `gelu_forward` as the nonlinearity in between (GELU, not ReLU, is the activation the original Transformer paper and most modern variants actually use here).

### Constraints

- `weight1`/`bias1` expand `x` from `d_model` up to `d_ff` (`weight1` has shape `(d_ff, d_model)`, matching `linear_forward`'s `(out_features, in_features)` convention).
- `weight2`/`bias2` project back down from `d_ff` to `d_model` (`weight2` has shape `(d_model, d_ff)`).
- GELU is applied BETWEEN the two linear layers, never before the first or after the second.
- The same two weight matrices are applied identically at EVERY position: no position-dependent behavior, and no mixing of information ACROSS positions (that is attention's job, not this sublayer's).

### Hints

<details>
<summary>Hint 1: The full pipeline</summary>

`hidden = gelu_forward(linear_forward(x, weight1, bias1))`, then `return linear_forward(hidden, weight2, bias2)`. Two lines, both directly reusing already-built functions.

</details>

<details>
<summary>Hint 2: Why this order</summary>

Two linear layers with NO nonlinearity between them collapse mathematically into a single linear layer (`W2 @ (W1 @ x) = (W2 @ W1) @ x`), which would defeat the entire purpose of adding a second sublayer. GELU sitting between them is what makes this genuinely more expressive than a single linear projection.

</details>

## Theory

### The simple version

Attention was a meeting where everyone in the room shares notes and each person leaves with a BLEND of everyone else's input (a weighted average, nothing more creative than that). The feed-forward sublayer is what each person does ALONE at their own desk immediately afterward: taking their own notes from the meeting, expanding them into a much longer, more detailed draft (the `d_ff`-sized hidden layer), applying their own judgment and interpretation (the nonlinearity) to that draft, then condensing it back down into a final, polished summary (projecting back to `d_model`), entirely independently of what anyone else at the meeting is doing with their own notes at the same time.

### The formula

```
hidden = GELU(x @ W1^T + b1)      # d_model -> d_ff (expand)
output = hidden @ W2^T + b2        # d_ff -> d_model (project back down)
```

Applied identically, and entirely independently, at every position along the sequence, `d_ff` conventionally set to `4 * d_model` (e.g. `d_model=512, d_ff=2048` in the original Transformer paper).

### How PyTorch actually implements this

`torch.nn.TransformerEncoderLayer` builds exactly this sublayer internally from two `torch.nn.Linear` layers with an activation function (`gelu` or `relu`, selectable) in between, and a hand-rolled model reproduces it identically with `torch.nn.Sequential(nn.Linear(d_model, d_ff), nn.GELU(), nn.Linear(d_ff, d_model))`. `[05-swiglu-ffn]`, immediately following this question, implements a more modern variant (used in LLaMA, PaLM, and most current LLMs) that replaces this simple "expand, activate, project" shape with a GATED variant, empirically a meaningful quality improvement for roughly the same compute budget. `[06-assemble-full-block]` wires this sublayer, wrapped in `[03-residual-connection]`'s residual connection, into a complete Transformer block alongside the attention sublayer.

## Explanation

`feedforward_sublayer` calls `linear_forward(x, weight1, bias1)` to project `x` up from `d_model` to the larger `d_ff`, applies `gelu_forward` to that expanded representation (the sublayer's only nonlinearity, and the only reason composing two linear layers here is more expressive than a single one), then calls `linear_forward` again with `weight2`/`bias2` to project back down to `d_model`. Both linear layers, and the GELU between them, are applied identically and independently to every position: there is no cross-position mixing anywhere in this sublayer, in direct contrast to the attention sublayer it follows, which mixes information ACROSS positions but performs no genuine nonlinear computation of its own.
