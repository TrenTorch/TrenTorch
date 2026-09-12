---
name: seq-attention-mha-concat-output-projection
title: 'Multi-Head Attention: concatenating heads plus output projection'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-mha-split-heads]` split a single `d_model`-wide representation into `num_heads` separate, smaller heads, computed each head's own independent attention pattern, and left the results as `num_heads` SEPARATE `d_k`-wide outputs, shape `(batch_size, num_heads, seq_len, d_k)`. Before this can be used by anything downstream (`[05-transformer-block]`'s residual connections, later in this curriculum, need a `d_model`-wide vector to add back to the original input), every head's output needs to be recombined back into ONE full-width representation. Simply gluing the heads' outputs side by side (concatenation) is the obvious first step, but the original Transformer paper's design adds one more crucial piece: a LEARNED linear projection applied to that concatenated result, before it's considered "done."

This output projection isn't a rounding-error detail, it's what gives the model a way to learn how to COMBINE different heads' contributions intelligently (some heads might deserve more weight than others for a given context, or their outputs might need to be blended in non-trivial, LEARNED ways), rather than forcing a fixed, naive side-by-side stacking to be the final answer regardless of what the training data actually calls for.

### From theory to code

Implement `concat_heads(x)`, the exact inverse of `[04-mha-split-heads]`'s `split_heads`: reshape `(batch_size, num_heads, seq_len, d_k)` back into `(batch_size, seq_len, d_model)`. Implement `multi_head_attention(query, key, value, num_heads, weight_o, bias_o, mask)`, calling `[04-mha-split-heads]`'s `multi_head_attention_per_head` (already provided) to get the per-head outputs, concatenating them via `concat_heads`, then applying a `[03-dl-training/02-layers/01-linear-forward]`-style output projection (`weight_o`, `bias_o`) to the concatenated result.

### Constraints

- `concat_heads` must be the exact mathematical inverse of `split_heads`: `concat_heads(split_heads(x, num_heads)) == x` for any valid `x`.
- The head dimension must move BACK to sit next to `d_k` before flattening (mirroring `[04-mha-split-heads]`'s move in the opposite direction), so each head's output lands in the correct CONSECUTIVE chunk of the final `d_model`-wide vector.
- `multi_head_attention` must apply the output projection AFTER concatenation, not before, and not to each head separately.
- `weight_o` has shape `(d_model, d_model)`, matching `[03-dl-training/02-layers/01-linear-forward]`'s `(out_features, in_features)` convention.

### Hints

<details>
<summary>Hint 1: concat_heads's two-step reshape</summary>

First, `x.transpose(0, 2, 1, 3)` swaps the `num_heads` and `seq_len` axes back (undoing `split_heads`'s own transpose), giving `(batch_size, seq_len, num_heads, d_k)`. Then, `.reshape(batch_size, seq_len, num_heads * d_k)` flattens the last two axes together into one `d_model`-wide dimension.

</details>

<details>
<summary>Hint 2: Sanity-checking against split_heads</summary>

If you're unsure `concat_heads` is correct, check it directly: `concat_heads(split_heads(x, num_heads))` should produce something numerically identical to the original `x`, for any `x` and any valid `num_heads`.

</details>

<details>
<summary>Hint 3: multi_head_attention</summary>

`per_head_output, weights = multi_head_attention_per_head(query, key, value, num_heads, mask=mask)`, then `concatenated = concat_heads(per_head_output)`, then `output = concatenated @ weight_o.T + bias_o`, exactly `[03-dl-training/02-layers/01-linear-forward]`'s `linear_forward` formula, applied to the concatenated attention output.

</details>

## Theory

### The simple version

A panel of expert reviewers (`[04-mha-split-heads]`'s heads) each producing their OWN independent assessment, and then, rather than simply stapling all their separate reports together and calling it done, an EDITOR reads through all of them and writes a single, coherent, synthesized final summary, one that might weight some reviewers' input more heavily than others depending on what's actually relevant. The output projection `weight_o`/`bias_o` is that editor: a LEARNED transformation specifically trained to combine the heads' separate outputs into the single best final representation, rather than leaving that combination entirely up to a fixed, non-learned concatenation.

### The formula

```
concat_heads(x):                                # inverse of split_heads
    transpose (batch, num_heads, seq_len, d_k) -> (batch, seq_len, num_heads, d_k)
    reshape to (batch, seq_len, num_heads * d_k)

multi_head_attention(Q, K, V):
    per_head_output, weights = multi_head_attention_per_head(Q, K, V, num_heads, mask)
    concatenated = concat_heads(per_head_output)
    output = concatenated @ weight_o.T + bias_o
```

### How PyTorch actually implements this

`torch.nn.MultiheadAttention` implements exactly this split-attend-concatenate-project pipeline internally, with `out_proj` as its own dedicated `nn.Linear` layer applying precisely this output projection step (this question's `weight_o`/`bias_o` correspond directly to `out_proj.weight`/`out_proj.bias`). `d_model` typically STAYS THE SAME size before and after the whole Multi-Head Attention block (input `d_model`, output `d_model`), which is exactly what makes `[05-transformer-block]`'s residual/skip connections (`output + original_input`, later in this curriculum) work at all, an addition requires both operands to share the same shape. Real Transformer implementations very commonly FUSE the output projection with whatever comes immediately after it in the surrounding architecture for efficiency, but the LOGICAL structure, split into heads, attend per head, concatenate, then one learned linear projection back to `d_model`, remains exactly this pipeline regardless of any particular implementation's low-level fusion choices.

## Explanation

`concat_heads` transposes `x`'s `num_heads` and `seq_len` axes back to their pre-split arrangement (`(batch_size, seq_len, num_heads, d_k)`, undoing `split_heads`'s own transpose), then reshapes the last two axes together into one flattened `(batch_size, seq_len, num_heads * d_k)` result, exactly reversing `split_heads`'s reshape-then-transpose sequence in the opposite order.

`multi_head_attention` calls `multi_head_attention_per_head` to get the per-head outputs and attention weights, calls `concat_heads` on those per-head outputs to recombine them into one `d_model`-wide representation per position, and applies `concatenated @ weight_o.T + bias_o`, a standard linear transformation, to that concatenated result, producing the final Multi-Head Attention output alongside the (still per-head) attention weights.
