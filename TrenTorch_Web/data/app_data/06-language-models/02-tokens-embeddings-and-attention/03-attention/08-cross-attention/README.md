---
name: lm-cross-attention
title: Cross-Attention & Encoder Masking
tags: [attention, encoder-decoder, masking]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Self-attention lets a sequence look at itself. **Cross-attention** lets one sequence look at a _different_ one: queries come from the decoder, while keys and values come from the encoder's output. This is how a translation model consults the source sentence, how a captioning model consults image features and how a diffusion model consults a text prompt. The decoder and encoder usually have different lengths, and the encoder side is padded in a batch, so padded encoder positions must be masked out before the softmax or the decoder would attend to nothing.

### From theory to code

Implement `cross_attention`.

### Constraints

- `x_dec` is `(Tq, d)` and `enc` is `(Tk, d)`. `W_q`, `W_k` and `W_v` are `(d, d_h)` projections: queries come from `x_dec @ W_q` and keys and values from `enc @ W_k` and `enc @ W_v`.
- Scores are `Q @ K.T / sqrt(d_h)`, shape `(Tq, Tk)`. `enc_mask` is a length-`Tk` array of 1 (real) and 0 (padding): scores at padding positions are set to `-inf` before the softmax.
- Return `(output, weights)` with `output` of shape `(Tq, d_h)` and `weights` of shape `(Tq, Tk)`.
- At least one encoder position is real.

### Hints

<details>
<summary>Hint 1</summary>

`np.where(enc_mask[None, :] == 1, scores, -np.inf)` masks the columns.

</details>

<details>
<summary>Hint 2</summary>

The stable softmax subtracts the row maximum, which is finite because at least one position is real.

</details>

## Theory

### The simple version

A student writing an essay (the decoder) keeps glancing at a source article (the encoder). The questions come from the essay, the answers come from the article, and blank lines at the end of the article's page (padding) are never worth looking at.

### The formula

$$
\text{CrossAttn}(X, E) = \text{softmax}\!\Big(\frac{(XW_q)(EW_k)^\top}{\sqrt{d_h}} + M\Big)(EW_v), \qquad M_{ij} = \begin{cases}0 & \text{real}\\ -\infty & \text{padding}\end{cases}
$$

Output length equals the decoder length $T_q$, regardless of the encoder length $T_k$.

### How this is done in practice

It is the second attention block of every encoder-decoder transformer layer (T5, BART, Whisper) and the conditioning mechanism of text-to-image U-Nets. In PyTorch it is `nn.MultiheadAttention(query=x, key=enc, value=enc, key_padding_mask=...)`.

## Explanation

The only difference from self-attention is where the inputs come from, and the only extra work is the padding mask on the key axis. Weights for padded columns are exactly zero, which the tests check directly.
