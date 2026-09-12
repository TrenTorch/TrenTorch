---
name: txf-modern-attention-quadratic-complexity
title: "Attention's quadratic complexity, and why context length is expensive"
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[04-seq-modeling/04-attention/01-scaled-dot-product-attention]`'s core computation, `scores = Q @ K^T`, produces a `(seq_len, seq_len)` matrix: EVERY position's query compared against EVERY position's key. Doubling the sequence length doesn't just double the amount of work this involves, it QUADRUPLES it, since both the number of queries AND the number of keys being compared against doubled simultaneously. This is fundamentally different from `[01-transformer-block/04-feedforward-sublayer]`'s FFN, which processes each position independently: doubling the sequence length there simply doubles the number of (identical, independent) positions to process, a LINEAR cost.

This asymmetry has real, practical consequences. At the SHORT sequence lengths most models were historically trained at, the FFN's cost usually dominates (it has a large HIDDEN dimension, `d_ff`, typically `4x d_model`, doing real work per position). But as sequence length grows, attention's quadratic term eventually overtakes it, and at the very long context lengths modern LLMs increasingly support (hundreds of thousands of tokens), attention can become THE dominant cost of running the model at all, both in raw compute AND in the memory needed to hold the `(seq_len, seq_len)` attention matrix itself. This is exactly the pressure `[04-flash-attention]` and `[05-sliding-window-attention]`, immediately following this question, are each independently designed to relieve.

### From theory to code

Implement three cost-estimation functions: `attention_compute_cost(seq_len, d_model)`, the multiply-add count for attention's two big matrix multiplies (`Q @ K^T` and `weights @ V`); `attention_memory_elements(seq_len, num_heads)`, the number of scalars in the fully materialized attention weight tensor; and `ffn_compute_cost(seq_len, d_model, d_ff)`, the multiply-add count for the feed-forward sublayer's two linear layers.

### Constraints

- `attention_compute_cost` scales as `seq_len^2 * d_model` (QUADRATIC in sequence length): `2` (two matrix multiplies of equal size) `* seq_len * seq_len * d_model`.
- `attention_memory_elements` scales as `seq_len^2` (also quadratic): `num_heads * seq_len * seq_len`.
- `ffn_compute_cost` scales as `seq_len * d_model * d_ff` (LINEAR in sequence length): `2 * seq_len * d_model * d_ff`.

### Hints

<details>
<summary>Hint 1: Counting the attention multiply-adds</summary>

`Q @ K^T` multiplies a `(seq_len, d_model)` matrix by a `(d_model, seq_len)` matrix, `seq_len * seq_len * d_model` multiply-adds. `weights @ V` is the same shape of work again. Total: `2 * seq_len * seq_len * d_model`.

</details>

<details>
<summary>Hint 2: The FFN's cost, for comparison</summary>

Each of the two linear layers processes `seq_len` INDEPENDENT positions, each one a `d_model`-by-`d_ff` (or `d_ff`-by-`d_model`) matrix-vector product: `seq_len * d_model * d_ff` multiply-adds per layer, `2 * seq_len * d_model * d_ff` total. Notice `seq_len` appears just ONCE here, not squared.

</details>

## Theory

### The simple version

A conference where the FFN's cost is like each attendee independently preparing their own notes beforehand (more attendees, proportionally more prep time, LINEAR). Attention's cost is like a mandatory session where every single attendee has a one-on-one conversation with every OTHER attendee: double the attendees, and the number of PAIRS of people who need to talk doesn't double, it roughly QUADRUPLES, since both "who's talking" and "who they're talking to" doubled at once.

### The formula

```
attention_compute_cost(seq_len, d_model) = 2 * seq_len^2 * d_model     # quadratic in seq_len
ffn_compute_cost(seq_len, d_model, d_ff)  = 2 * seq_len   * d_model * d_ff   # linear in seq_len
```

For a fixed model, there is always some CROSSOVER sequence length past which the quadratic term overtakes the linear one, regardless of how large `d_ff` is, simply because `seq_len^2` eventually outgrows any fixed multiple of `seq_len`.

### How PyTorch actually implements this

`torch.nn.functional.scaled_dot_product_attention` performs exactly these two `(seq_len, seq_len)`-shaped matrix multiplies internally, and PyTorch's own attention-related documentation and profiling tools routinely surface this exact quadratic-vs-linear distinction when explaining WHY long-context inference is disproportionately expensive. `[04-flash-attention]`, immediately following this question, doesn't actually reduce the quadratic COMPUTE cost (the same number of multiply-adds still happens), but eliminates the quadratic MEMORY cost by never materializing the full `(seq_len, seq_len)` matrix at once. `[05-sliding-window-attention]` takes the opposite approach: it genuinely reduces the compute itself, by making each query only attend to a bounded WINDOW of keys rather than the entire sequence, turning the quadratic term back into a linear one.

## Explanation

`attention_compute_cost` returns `2 * seq_len * seq_len * d_model`, directly reflecting the two `(seq_len, seq_len, d_model)`-shaped matrix multiplies attention performs (`Q @ K^T` and `weights @ V`), a cost that scales with the SQUARE of the sequence length. `attention_memory_elements` returns `num_heads * seq_len * seq_len`, the size of the fully materialized attention weight tensor, also quadratic. `ffn_compute_cost` returns `2 * seq_len * d_model * d_ff`, scaling only LINEARLY with sequence length, since the FFN, `[01-transformer-block/04-feedforward-sublayer]`, processes every position identically and independently, with no position ever needing to be compared against any other. This asymmetry (quadratic vs. linear) is precisely why, past some sequence-length crossover point, attention comes to dominate a Transformer's total compute and memory cost, motivating essentially every efficient-attention technique this track goes on to cover.
