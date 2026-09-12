---
name: seq-attention-scaled-dot-product
title: 'Scaled dot-product attention, forward'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-recurrent-neural-networks/07-seq2seq-bottleneck]` demonstrated the core weakness of the classic sequence-to-sequence encoder-decoder: forcing an ENTIRE input sequence through one fixed-size hidden state disproportionately preserves LATE information over early information. Attention removes this bottleneck entirely by letting every OUTPUT position directly look at EVERY input position, choosing dynamically, for each output position separately, which input positions actually matter, rather than relying on one compressed summary.

The mechanism: every position produces three vectors, a QUERY ("what am I looking for"), a KEY ("what do I have to offer, for matching purposes"), and a VALUE ("what do I have to offer, for actually being retrieved"). A query's similarity to every position's key (measured via a dot product, the SAME similarity measure `[00-math-and-statistics/01-linear-algebra/02-dot-product-norms]` introduced early in this curriculum) determines how much weight that position's VALUE gets in the final weighted average. This is genuinely just a differentiable, "soft" version of a lookup table: instead of retrieving ONE exact match (`[04-seq-modeling/02-embeddings/01-token-embedding-lookup]`'s hard, exact-id lookup), attention retrieves a WEIGHTED BLEND of every value, weighted by how well each key matched the query.

### From theory to code

Implement `scaled_dot_product_attention(query, key, value, mask)`. Compute raw similarity scores via `query @ key^T`, scale them DOWN by `1/sqrt(d_k)` (`d_k` is the query/key vectors' own dimensionality), optionally add `mask` (large negative values at positions that should never be attended to), apply `softmax` along the LAST axis (so each query position's weights sum to exactly `1`), and use those weights to compute a weighted sum of `value`.

### Constraints

- Scores must be scaled by `1/sqrt(d_k)` BEFORE the mask is added and BEFORE softmax, not after.
- `mask`, when provided, is ADDED to the scaled scores (not multiplied, not applied after softmax).
- `softmax` must be applied along the LAST axis (over KEY positions), so each ROW of `attention_weights` (one query position) sums to exactly `1`.
- Must work for any number of leading batch/head dimensions, not just a single unbatched `(seq_len, d_k)` pair.

### Hints

<details>
<summary>Hint 1: Computing and scaling the scores</summary>

`scores = query @ np.swapaxes(key, -2, -1) / np.sqrt(d_k)`: `np.swapaxes(key, -2, -1)` transposes just the LAST two axes of `key` (so this works correctly regardless of how many leading batch dimensions there are), giving `scores` shape `(..., seq_len_q, seq_len_k)`.

</details>

<details>
<summary>Hint 2: Applying the mask</summary>

`if mask is not None: scores = scores + mask`, a simple conditional addition; when `mask` is `None`, skip it entirely and use the raw scaled scores.

</details>

<details>
<summary>Hint 3: Softmax over the last axis, then the weighted sum</summary>

A numerically-stable softmax over the LAST axis: `scores_shift = scores - np.max(scores, axis=-1, keepdims=True)`, `weights = np.exp(scores_shift) / np.sum(np.exp(scores_shift), axis=-1, keepdims=True)`. Then `output = weights @ value`. Return `(output, weights)`.

</details>

## Theory

### The simple version

A librarian fielding a research question (the QUERY) by comparing it against every book's index card (the KEY) to judge relevance, then pulling a bit from EVERY sufficiently relevant book (the VALUE), weighted by how well each book's index card actually matched the question, rather than retrieving exactly one "best match" book and ignoring everything else. A book whose index card barely matches contributes almost nothing to the final answer; a very well-matching book dominates it, but the answer can genuinely draw on SEVERAL sources at once, in proportions determined entirely by the match quality.

### The formula

```
scores = (Q @ K^T) / sqrt(d_k)
scores = scores + mask                    # if mask given
weights = softmax(scores, axis=-1)         # one row of weights per query position
output = weights @ V
```

The `1/sqrt(d_k)` scaling exists for a concrete numerical reason: for random `Q`/`K` vectors with unit variance per entry, the raw dot product `Q . K` has variance proportional to `d_k` (a sum of `d_k` independent-ish terms), so for a large `d_k`, unscaled dot products can grow large enough to push softmax into its SATURATED regime (extremely close to one-hot, near-zero gradient almost everywhere), exactly the same kind of saturation concern `[03-dl-training/02-layers/04-weight-initialization]`'s careful variance control was designed to avoid for activations. Dividing by `sqrt(d_k)` keeps the scores' variance roughly constant regardless of `d_k`, avoiding this saturation.

### How PyTorch actually implements this

`torch.nn.functional.scaled_dot_product_attention` implements exactly this formula (this question's implementation matches its output precisely, verified directly), and on modern GPUs, PyTorch dispatches this call to a FUSED, highly optimized kernel (FlashAttention or a similar memory-efficient algorithm, `Note: FlashAttention, the same math computed without materializing the full attention matrix`, later in this curriculum, explains the key trick: the full `(seq_len, seq_len)` `weights` matrix, potentially enormous for long sequences, never actually gets fully materialized in GPU memory at once). `[02-causal-mask]`, immediately following this question, builds exactly the kind of `mask` argument this function accepts, to prevent a position from attending to positions that come AFTER it (essential for autoregressive text generation, where a model must never "see" tokens it hasn't generated yet). `Multi-Head Attention: splitting into heads, per-head attention`, later in this track, runs this SAME function multiple times in parallel, once per "head," each with its own learned `query`/`key`/`value` projections, letting the model attend to several DIFFERENT kinds of relationships simultaneously.

## Explanation

`scaled_dot_product_attention` computes `scores = query @ swapaxes(key, -2, -1) / sqrt(d_k)`: the transpose-and-multiply gives every query position's similarity to every key position in one batched matrix multiply, and dividing by `sqrt(d_k)` keeps that similarity's scale controlled regardless of the vectors' dimensionality. If `mask` is given, it's added directly to `scores` (large negative values there push the corresponding softmax weight toward zero). A numerically-stable softmax is then applied along the LAST axis (subtracting each row's max before exponentiating, avoiding overflow, exactly the same stability trick `[01-classical-ml/02-classification/06-softmax-cce]`'s `softmax` used, generalized here to work along an arbitrary trailing axis rather than a fixed `axis=1`), producing `weights`, whose rows each sum to `1`. Finally, `output = weights @ value` computes the weighted blend of value vectors the function returns, alongside `weights` itself (useful for inspection, visualization, or as an input to further computation).
