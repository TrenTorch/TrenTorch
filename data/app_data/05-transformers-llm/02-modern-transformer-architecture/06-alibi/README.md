---
name: txf-modern-alibi
title: 'ALiBi: a positional bias baked into attention scores instead of the embeddings'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding]` and `[06-rope]` both inject positional information by modifying the QUERY/KEY VECTORS themselves, before attention ever runs. Press et al. (2021, "ALiBi," Attention with Linear Biases) proposed a different place entirely to encode position: leave the vectors untouched, and instead add a fixed, position-DEPENDENT PENALTY directly onto the raw attention SCORES, right where `[04-flash-attention]`'s and `[05-sliding-window-attention]`'s masks already get added, before softmax. The penalty is simple: for query position `i` and key position `j`, subtract a value proportional to the DISTANCE `i - j`, so keys further in the past get an increasingly large negative bias, and therefore, after softmax, an increasingly SMALL attention weight, a direct, built-in recency preference, without touching the content-based `Q @ K^T` similarity at all.

Different attention HEADS use different bias STRENGTHS (a range of slopes, from very mild to very aggressive recency preference), letting some heads stay close to ordinary, distance-agnostic attention while others behave almost like `[05-sliding-window-attention]`'s hard cutoff, all without any explicit windowing logic. A major practical payoff: because the bias is a simple, closed-form FUNCTION of distance rather than a fixed, learned per-position vector, ALiBi generalizes cleanly to sequence lengths LONGER than anything the model was trained on, a genuine weakness of `[04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding]`'s learned or fixed-table approaches.

### From theory to code

Implement `compute_alibi_slopes(num_heads)` (a geometric sequence of per-head slopes), `compute_alibi_bias(seq_len, num_heads)` (`-slope * (i - j)` for every head and every query/key position pair), and `alibi_causal_mask(seq_len, num_heads)`, combining that bias with `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask into one additive mask ready to hand directly to `[01-scaled-dot-product-attention]`.

### Constraints

- Slopes form a GEOMETRIC sequence: `slopes[h] = ratio^(h+1)` for `h = 0, ..., num_heads-1`, where `ratio = 2^(-8/num_heads)` (both the starting value AND the common ratio).
- `bias[h, i, j] = -slopes[h] * (i - j)`: zero on the diagonal (`i == j`), increasingly NEGATIVE as `j` moves further into the past relative to `i` (larger `i - j`).
- `alibi_causal_mask` still enforces causality: `j > i` must remain `-inf`, exactly like `[02-causal-mask]`, with the ALiBi bias added only where the causal mask itself doesn't already forbid attending.
- Output shape is `(num_heads, seq_len, seq_len)`: unlike `[02-causal-mask]`'s single shared `(seq_len, seq_len)` mask, ALiBi's mask genuinely differs PER HEAD.

### Hints

<details>
<summary>Hint 1: The slopes</summary>

`ratio = 2.0 ** (-8.0 / num_heads)`, then `slopes = ratio ** np.arange(1, num_heads + 1)`: head `0` gets slope `ratio^1`, head `1` gets `ratio^2`, and so on, each roughly HALF (or less) of the previous head's slope by the time `num_heads` is reasonably large.

</details>

<details>
<summary>Hint 2: The bias tensor</summary>

`distance = positions[:, None] - positions[None, :]` (shape `(seq_len, seq_len)`, exactly `[05-sliding-window-attention]`'s distance computation), then `bias = -slopes[:, None, None] * distance[None, :, :]`, broadcasting the per-head slopes against the shared `(seq_len, seq_len)` distance matrix to get shape `(num_heads, seq_len, seq_len)`.

</details>

<details>
<summary>Hint 3: Combining with the causal mask</summary>

`return compute_alibi_bias(seq_len, num_heads) + build_causal_mask(seq_len)[None, :, :]`: the causal mask's `(seq_len, seq_len)` shape broadcasts against every head via the extra leading axis, and adding `-inf` to any finite bias still gives `-inf`, so causally-forbidden positions stay forbidden regardless of what the bias itself computed there.

</details>

## Theory

### The simple version

`[04-seq-modeling/02-embeddings]`'s positional encodings were like stamping a timestamp directly onto every letter BEFORE it's read, permanently changing the letter's own content. ALiBi instead leaves every letter untouched, and applies a "how recent is this" DISCOUNT only at the moment of DECIDING how much attention to pay to it, exactly like a person naturally trusting a recent memory more than an old one, not because the old memory itself changed, but because of a built-in, distance-based skepticism applied at RECALL time.

### The formula

```
ratio = 2^(-8/num_heads)
slopes[h] = ratio^(h+1)                        for h = 0, ..., num_heads-1

bias[h, i, j] = -slopes[h] * (i - j)
alibi_causal_mask[h, i, j] = bias[h, i, j] + causal_mask[i, j]
```

Added directly onto `[01-scaled-dot-product-attention]`'s scaled scores, exactly where `[02-causal-mask]`'s mask and `[05-sliding-window-attention]`'s mask are also added, before softmax.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements ALiBi directly (like RoPE and GQA before it, it lives in model-specific code, e.g. the BLOOM and MPT model families' Hugging Face `transformers` implementations), but every real implementation performs exactly this "distance times a per-head slope, added to the scores before softmax" computation. `[04-seq-modeling/02-embeddings/06-rope]`'s RoPE is the more widely-adopted alternative in the CURRENT generation of LLMs (LLaMA, Mistral, and most others), but ALiBi remains an instructive contrast: both approaches encode RELATIVE position (only the DIFFERENCE `i - j` matters, never an absolute position index), but RoPE modifies the vectors THEMSELVES via rotation, while ALiBi modifies only the SCORES, a fundamentally simpler mechanism that requires no per-dimension pairing or rotation math at all.

## Explanation

`compute_alibi_slopes` builds a geometric sequence via `ratio ** np.arange(1, num_heads + 1)`, giving each head a distinct, monotonically-DECREASING bias strength. `compute_alibi_bias` computes the `(seq_len, seq_len)` distance matrix once (broadcasting row positions against column positions, exactly `[05-sliding-window-attention]`'s pattern) and multiplies it by each head's own (negated) slope via a broadcast against a new leading axis, producing a full `(num_heads, seq_len, seq_len)` bias tensor: zero on the diagonal, increasingly negative for keys further in the past. `alibi_causal_mask` adds that bias directly to `[02-causal-mask]`'s ordinary causal mask (broadcast across the head axis), so future positions stay strictly forbidden (`-inf` dominates any finite bias added to it) while every remaining, causally-VALID position gets its attention score nudged down in proportion to its distance from the query, a soft, content-independent recency preference baked directly into the score computation itself.
