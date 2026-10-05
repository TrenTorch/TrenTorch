---
name: lm-sparse-autoencoder
title: Sparse Autoencoders
tags: [interpretability, sparse-autoencoder, features]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Individual neurons in a language model are hard to read because the model packs many more concepts into its activations than it has dimensions (**superposition**), so each neuron responds to a mixture. A **sparse autoencoder** (SAE) tries to unpack them. It maps an activation vector up into a much wider layer of feature activations, keeps only a few of them active through a sparsity penalty, and reconstructs the original activation from those few features. If it works, each feature fires on one recognizable concept. The training objective is a trade-off: reconstruct well, but explain each activation with as few features as possible.

### From theory to code

Implement `sae_forward` and `sae_loss`.

### Constraints

- `x` has shape `(n, d)`. The encoder is `f = relu((x - b_dec) @ W_enc + b_enc)` with `W_enc` of shape `(d, m)`. The decoder is `x_hat = f @ W_dec + b_dec` with `W_dec` of shape `(m, d)`.
- `sae_forward(x, W_enc, b_enc, W_dec, b_dec)` returns `(x_hat, f)`.
- `sae_loss(x, x_hat, f, l1_coeff)` returns `mse + l1_coeff * l1` where `mse` is the mean over examples of the **sum** over dimensions of `(x - x_hat) ** 2`, and `l1` is the mean over examples of the sum of `|f|` over features. Return a Python float.
- `m > d` is expected (an overcomplete dictionary).

### Hints

<details>
<summary>Hint 1</summary>

Subtracting the decoder bias before encoding centres the input and is a common design choice that makes `b_dec` the model's estimate of the mean activation.

</details>

<details>
<summary>Hint 2</summary>

`f` is non-negative after the ReLU, so `|f|` is just `f`.

</details>

## Theory

### The simple version

Think of a paint shop that must reproduce any colour using a few tins from a large shelf of many tins. A good shelf lets every colour be matched using only two or three tins. The sparsity penalty is a small fee per tin opened, and the tins that end up useful are the features.

### The formula

$$
f = \text{ReLU}\big((x - b_d) W_e + b_e\big), \quad \hat x = f W_d + b_d, \quad
\mathcal{L} = \mathbb{E}\lVert x - \hat x\rVert_2^2 + \lambda\,\mathbb{E}\lVert f\rVert_1
$$

The L1 term is the convex relaxation of counting active features. Decoder columns are usually constrained to unit norm so the penalty cannot be dodged by shrinking $f$ and growing $W_d$.

### How this is done in practice

Anthropic, OpenAI and the open-source community (SAELens, `dictionary_learning`) train SAEs on residual-stream or MLP activations of large models, then label features by the text that activates them. TopK SAEs replace the L1 penalty with keeping only the `k` largest activations, and dead or dense features are tracked as training diagnostics.

## Explanation

The forward pass is two affine maps with a ReLU between them. The loss separates the two competing goals so their balance is a single coefficient, which is the main knob when training a real SAE: raise it for sparser, more interpretable features and lower it for better reconstruction.
