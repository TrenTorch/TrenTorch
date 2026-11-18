---
name: lm-logit-lens
title: Logit Lens
tags: [interpretability, transformers, residual-stream]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A transformer's layers write into a shared **residual stream**, and only the final layer's stream is turned into next-token probabilities by the unembedding matrix. But nothing stops us from applying the same unembedding to the stream after _every_ layer. The result, the **logit lens**, shows what the model would predict if it stopped early. Watching the prediction sharpen layer by layer reveals where information about the answer first appears. The final normalization must be applied before unembedding because the real model always applies it, so a lens that skips it reads garbage on streams whose scale differs from the last layer's.

### From theory to code

Implement `logit_lens` and `target_rank_by_layer`.

### Constraints

- `resid` has shape `(L, d)`: the residual stream at one position after each of `L` layers. `W_U` has shape `(d, V)`. `norm_weight` is a length-`d` RMSNorm gain.
- `logit_lens(resid, W_U, norm_weight, eps=1e-6)` applies RMSNorm to each row, `x / sqrt(mean(x ** 2) + eps) * norm_weight`, then multiplies by `W_U`. It returns logits of shape `(L, V)`.
- `target_rank_by_layer(logits, target)` returns an integer array of length `L` giving the rank of token `target` in each row, where rank `0` means it is the top prediction (the number of tokens with a strictly larger logit).
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

RMSNorm is row-wise: `np.mean(resid ** 2, axis=1, keepdims=True)`.

</details>

<details>
<summary>Hint 2</summary>

Rank is `(logits > logits[:, [target]]).sum(axis=1)`.

</details>

## Theory

### The simple version

It is like opening a book to a middle page and asking "if the story ended here, how would you predict the last word?". Early pages give a vague guess and later pages a sharp one, and the page where the right word first becomes likely marks where the model worked it out.

### The formula

$$
\text{lens}_\ell = \text{RMSNorm}(h_\ell)\, W_U, \qquad
\text{RMSNorm}(x) = \frac{x}{\sqrt{\tfrac{1}{d}\sum_j x_j^2 + \epsilon}}\odot g
$$

$h_\ell$ is the residual stream after layer $\ell$. The rank of the true token across layers is a scale-free summary of how early the model "knows" the answer.

### How this is done in practice

The idea was introduced as the logit lens and refined by the _tuned lens_, which learns a small affine map per layer because raw intermediate streams are not perfectly aligned with the final unembedding. Libraries such as TransformerLens expose `model.run_with_cache` plus `ln_final` and `unembed` so the lens is a few lines.

## Explanation

The lens is normalization followed by a matrix multiplication, applied to all layers at once. The rank function turns the logits into something comparable across layers and models: rank is invariant to the scale of the logits, which grows with depth.
