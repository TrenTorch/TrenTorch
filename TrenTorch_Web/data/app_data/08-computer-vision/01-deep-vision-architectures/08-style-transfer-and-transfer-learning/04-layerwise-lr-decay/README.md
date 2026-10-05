---
name: vision-layerwise-lr-decay
title: Layer-wise Learning Rate Decay
tags: [computer-vision, transfer-learning, fine-tuning, learning-rate]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A pretrained network's early layers learn general features (edges, textures, word pieces) that transfer to almost any task, while its last layers are specific to the original task. When fine-tuning on new data it is therefore wise to update the early layers **gently** and the later layers **boldly**. **Layer-wise learning-rate decay** formalizes this: the top layer gets the base learning rate, and each layer below it gets the rate of the layer above multiplied by a decay factor `d < 1`. The result is a different learning rate per parameter group, which optimizers support directly. Parameter names carry the layer index, so the group can be recovered from the name.

### From theory to code

Implement `layer_index` and `layerwise_lr`.

### Constraints

- Parameters are named `embed.<...>`, `layers.<i>.<...>` or `head.<...>`. With `n_layers` blocks, assign depth indices: `embed` is `0`, `layers.i` is `i + 1`, `head` is `n_layers + 1`. `layer_index(name, n_layers)` returns this index. Any other name raises `ValueError`.
- `layerwise_lr(name, n_layers, base_lr, decay)` returns `base_lr * decay ** (n_layers + 1 - layer_index(name, n_layers))`, so the head gets `base_lr` and every step down multiplies by `decay`.

### Hints

<details>
<summary>Hint 1</summary>

Split the name on `.`; the second component of `layers.<i>...` is the block number.

</details>

<details>
<summary>Hint 2</summary>

`decay = 1` gives the same rate everywhere, `decay = 0.5` halves it at each level.

</details>

## Theory

### The simple version

Retraining a skilled chef for a new cuisine: the knife skills (early layers) need only a light touch, the menu knowledge (the head) is rewritten.

### The formula

$$
\eta_\ell = \eta_{\text{base}}\; d^{\,L + 1 - \ell}, \qquad \ell \in \{0, 1, \dots, L + 1\}
$$

with $\ell = 0$ the embedding and $\ell = L + 1$ the classifier head.

### How this is done in practice

ULMFiT introduced discriminative fine-tuning, and the factor 0.65 to 0.95 is common in BERT and ViT fine-tuning recipes (for example `layer_decay=0.75` in `timm`). In PyTorch each rate becomes an entry in the optimizer's `param_groups`.

## Explanation

Name parsing plus an exponent. The tests check the endpoints, the geometric progression and the error case.
