---
name: lm-parameter-and-flop-counting
title: Parameter & FLOP Counting
tags: [scaling-laws, compute, transformers]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Before training a model you need two numbers: how many parameters it has and how much compute a run will cost. A decoder-only transformer's parameters are dominated by two kinds of weights. Each layer has four `d x d` attention matrices (query, key, value, output) and a two-matrix MLP of width `d_ff`. The embedding table has `vocab x d` weights and is counted once if the output head shares it. Training compute then follows a famous rule of thumb: each parameter takes part in about 6 floating-point operations per training token (2 for the forward pass, 4 for the backward pass), so total FLOPs are about `6 * N * D` for `N` parameters and `D` tokens.

### From theory to code

Implement `transformer_params`, `training_flops` and `chinchilla_tokens`.

### Constraints

- `transformer_params(n_layers, d_model, vocab, d_ff=None, tied=True)` counts: per layer `4 * d_model**2 + 2 * d_model * d_ff`, plus the embedding `vocab * d_model` once if `tied` else twice. `d_ff` defaults to `4 * d_model`. Ignore biases and normalization weights.
- `training_flops(n_params, n_tokens)` is `6 * n_params * n_tokens`.
- `chinchilla_tokens(n_params)` is the compute-optimal token count `20 * n_params`.
- Return Python ints for the first function and floats or ints from the arithmetic for the others.

### Hints

<details>
<summary>Hint 1</summary>

Count per-layer weights once, multiply by the number of layers, then add the embedding term.

</details>

<details>
<summary>Hint 2</summary>

Python integers do not overflow, so no special handling is needed for large counts.

</details>

## Theory

### The simple version

Estimating a road trip: distance (parameters) and fuel per kilometre (FLOPs per token) multiply to total fuel. The factor 6 is the fuel economy of one parameter on one token: two operations going forward, four going back.

### The formula

$$
N = L\,(4d^2 + 2\,d\,d_{ff}) + V d, \qquad C \approx 6\,N\,D, \qquad D_{\text{opt}} \approx 20\,N
$$

With $d_{ff} = 4d$ the per-layer count is $12 d^2$, which gives the useful shortcut $N \approx 12\,L\,d^2$ for the non-embedding parameters.

### How this is done in practice

The estimate reproduces published sizes closely: 12 layers, `d = 768` and the GPT-2 vocabulary of 50,257 give about 124 million parameters. Scaling-law papers use exactly these formulas (with or without the embedding term) to place runs on a compute axis, and hardware planners divide `6ND` by realistic sustained FLOPs to estimate days.

## Explanation

All three functions are one-line arithmetic once the structure of a transformer layer is clear. The test with the GPT-2-small configuration anchors the formula against a number you can look up.
