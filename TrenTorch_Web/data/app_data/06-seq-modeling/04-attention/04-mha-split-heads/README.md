---
name: seq-attention-mha-split-heads
title: 'Multi-Head Attention: splitting into heads, per-head attention'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[01-scaled-dot-product-attention]`'s single attention computation produces exactly ONE set of attention weights per query, meaning it can only really capture ONE notion of "relevance" at a time. But natural language relationships are genuinely MULTI-FACETED: a word might need to attend to a nearby word for SYNTACTIC reasons (subject-verb agreement) and to a distant word for SEMANTIC reasons (what does "it" refer to) simultaneously, and a single shared attention pattern has to somehow blend both needs into one compromise. Multi-Head Attention's fix: instead of computing ONE attention pattern over the FULL `d_model`-dimensional vectors, split each of `query`/`key`/`value` into several smaller, INDEPENDENT "heads," each with its own SLICE of the full dimensionality, and let each head learn to specialize in capturing a DIFFERENT kind of relationship, entirely in parallel.

This question implements exactly the SPLITTING and PER-HEAD ATTENTION half of Multi-Head Attention; `Multi-Head Attention: concatenating heads plus output projection`, immediately following this question, implements the second half, recombining every head's separate output back into one unified representation.

### From theory to code

Implement `split_heads(x, num_heads)`, reshaping `x` (shape `(batch_size, seq_len, d_model)`) into `(batch_size, num_heads, seq_len, d_k)`, where `d_k = d_model // num_heads`. Implement `multi_head_attention_per_head(query, key, value, num_heads, mask)`, splitting all three inputs via `split_heads`, then calling `[01-scaled-dot-product-attention]`'s `scaled_dot_product_attention` ONCE on the split, head-batched inputs, letting it process every head in parallel since it's already shape-agnostic to leading batch dimensions.

### Constraints

- `split_heads` must reshape so that `d_model` splits into `num_heads` CONSECUTIVE, non-overlapping chunks of size `d_k` each (the first `d_k` dimensions become head 0, the next `d_k` become head 1, and so on), then move the head dimension to position `1` (right after batch).
- `d_model` must be evenly divisible by `num_heads` (assume this holds; no remainder-handling needed).
- `multi_head_attention_per_head` must call `scaled_dot_product_attention` a SINGLE time on the already-split, `(batch_size, num_heads, seq_len, d_k)`-shaped inputs, not loop over heads manually calling it once per head.
- The result's shape must be `(batch_size, num_heads, seq_len, d_k)`, the head dimension still separate (not yet recombined, that's `[05-mha-concat-output-projection]`'s job).

### Hints

<details>
<summary>Hint 1: split_heads's two-step reshape</summary>

First, `x.reshape(batch_size, seq_len, num_heads, d_k)` splits the LAST dimension (`d_model`) into two: `num_heads` and `d_k`, without changing the total number of elements or the order of any existing dimension. Then, `.transpose(0, 2, 1, 3)` swaps the `seq_len` and `num_heads` axes, moving the head dimension to sit right after batch: `(batch_size, num_heads, seq_len, d_k)`.

</details>

<details>
<summary>Hint 2: Why this specific reshape, not a different one</summary>

Reshaping `(batch, seq_len, d_model)` directly to `(batch, seq_len, num_heads, d_k)` (rather than some other splitting order) preserves the natural CONSECUTIVE-chunk interpretation: dimensions `0` through `d_k-1` of the original `d_model` axis become head 0's slice, dimensions `d_k` through `2*d_k-1` become head 1's slice, and so on, matching how the learned projection weights that PRODUCE `query`/`key`/`value` in a real Transformer are structured.

</details>

<details>
<summary>Hint 3: multi_head_attention_per_head</summary>

`query_heads = split_heads(query, num_heads)` (and the same for `key`/`value`), then `return scaled_dot_product_attention(query_heads, key_heads, value_heads, mask=mask)` directly, letting that function's existing shape-agnostic implementation handle the `(batch_size, num_heads, ...)` leading dimensions in one call.

</details>

## Theory

### The simple version

A panel of several independent expert reviewers examining the SAME document, each reviewer given access only to ONE narrower aspect of it (one reviewer checks grammar, another checks factual accuracy, another checks tone), rather than one single generalist reviewer trying to judge everything about the document at once with a single, necessarily-compromised set of criteria. Each "head" in Multi-Head Attention is one of these narrower-focus reviewers, examining the SAME sequence but through its OWN learned lens (its own slice of the `query`/`key`/`value` dimensionality), free to develop its own specialized notion of what "relevant" means.

### The formula

```
d_k = d_model // num_heads
split_heads(x) = reshape x from (batch, seq_len, d_model)
              to (batch, seq_len, num_heads, d_k)
              then transpose to (batch, num_heads, seq_len, d_k)

Q_heads, K_heads, V_heads = split_heads(query), split_heads(key), split_heads(value)
output, weights = scaled_dot_product_attention(Q_heads, K_heads, V_heads, mask)
```

Because `scaled_dot_product_attention` operates identically regardless of how many LEADING dimensions its inputs have, treating `(batch_size, num_heads)` together as one combined effective batch dimension computes every head's attention in a single, efficiently batched call, rather than requiring a slow Python loop over heads.

### How PyTorch actually implements this

`torch.nn.MultiheadAttention` implements exactly this split-into-heads pattern internally (its own reshape/transpose logic is functionally equivalent to `split_heads` here, though PyTorch's internal packing details differ slightly for efficiency), and modern efficient attention kernels (like FlashAttention, `Note: FlashAttention` later in this curriculum) are specifically designed to process the resulting `(batch, num_heads, seq_len, d_k)` shape efficiently on GPU hardware, computing all heads for a whole batch in one fused kernel launch. A real Transformer's `query`, `key`, and `value` themselves are typically produced by their OWN learned linear projections (`[03-dl-training/02-layers/01-linear-forward]`-style, `Wq`, `Wk`, `Wv`) applied to the SAME input embedding BEFORE this splitting step, so different heads genuinely see different LEARNED projections of the input, not just an arbitrary slice of the raw embedding, though the slicing mechanics `split_heads` implements are identical either way. Empirically, different heads in a trained Transformer often DO specialize in genuinely interpretable ways, some heads consistently attend to syntactically related words, others track long-range coreference, a real, observed phenomenon that gives some intuitive support to the "several independent experts" framing above.

## Explanation

`split_heads` reshapes `x` from `(batch_size, seq_len, d_model)` to `(batch_size, seq_len, num_heads, d_k)` (splitting the last axis into two, without disturbing element order), then transposes axes `1` and `2` to move `num_heads` to position `1`, giving the final `(batch_size, num_heads, seq_len, d_k)` shape, where each head's `d_k`-wide slice occupies a CONSECUTIVE chunk of the original `d_model` dimension.

`multi_head_attention_per_head` calls `split_heads` on `query`, `key`, and `value` independently, then passes all three split results directly into `[01-scaled-dot-product-attention]`'s `scaled_dot_product_attention` in a SINGLE call, relying on that function's shape-agnostic handling of leading dimensions to compute every head's own attention output and weights simultaneously, in one batched operation, rather than looping over heads one at a time.
