---
name: txf-modern-sliding-window-attention
title: 'Sliding-window / local attention: bounding context to a fixed window'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-attention-quadratic-complexity]` showed attention's compute and memory both scale QUADRATICALLY with sequence length. `[04-flash-attention]` removed the quadratic MEMORY cost without touching the quadratic COMPUTE cost (it computes the exact same full-attention answer, just without materializing the whole matrix at once). Sliding-window (or "local") attention takes a genuinely different approach: it reduces the COMPUTE itself, by simply refusing to let any query attend to keys beyond a fixed distance away. Instead of `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask (attend to EVERYTHING up to and including the current position, an unbounded, growing window as the sequence gets longer), sliding-window attention bounds every position to a FIXED-size window of `window_size` most-recent positions, regardless of how long the overall sequence is.

This turns attention's cost from `O(seq_len^2)` back into `O(seq_len * window_size)`, LINEAR in sequence length (since `window_size` is a small, fixed constant, not something that grows with `seq_len`), a real, direct reduction in the amount of work, at the cost of every position genuinely losing access to anything outside its window (a real modeling tradeoff, not merely an implementation detail: information from far in the past can only reach later positions by being relayed forward, block by block, through intermediate positions still within range).

### From theory to code

Implement `build_sliding_window_mask(seq_len, window_size)`, an additive mask (like `[02-causal-mask]`'s) that permits position `i` to attend ONLY to positions `j` with `i - window_size < j <= i`, and `sliding_window_attention(query, key, value, window_size)`, `[01-scaled-dot-product-attention]`'s attention with that mask applied.

### Constraints

- Sliding-window masking is STILL causal: no position ever attends to the future (`j > i` is always forbidden), exactly like `[02-causal-mask]`.
- Additionally, positions too far in the PAST are forbidden: `j <= i - window_size` is also masked out (`-inf`).
- Every position attends to AT MOST `window_size` positions total (itself plus up to `window_size - 1` earlier ones); positions near the very start of the sequence, with fewer than `window_size - 1` earlier positions available, simply attend to however many exist.
- `window_size == seq_len` must reduce EXACTLY to `[02-causal-mask]`'s ordinary (unbounded) causal mask.

### Hints

<details>
<summary>Hint 1: The allowed-distance condition</summary>

`distance = i - j` (row index minus column index). A position is allowed when `0 <= distance < window_size`: `distance >= 0` is `[02-causal-mask]`'s usual "no future" rule, `distance < window_size` is the NEW "not too far in the past" rule.

</details>

<details>
<summary>Hint 2: Building the mask</summary>

```python
positions = np.arange(seq_len)
distance = positions[:, None] - positions[None, :]
allowed = (distance >= 0) & (distance < window_size)
mask = np.where(allowed, 0.0, -np.inf)
```

</details>

<details>
<summary>Hint 3: Using it</summary>

`sliding_window_attention` is a one-line wrapper: build the mask for `query`'s sequence length, then call `[01-scaled-dot-product-attention]`'s `scaled_dot_product_attention(query, key, value, mask=mask)` exactly as-is.

</details>

## Theory

### The simple version

`[02-causal-mask]`'s causal attention was a reader who, at every point in a book, can reference EVERYTHING read so far, however far back, an unboundedly-growing set of notes to search through as the book gets longer. Sliding-window attention is a reader working from a small stack of only the last few pages, literally discarding earlier pages once they fall out of reach: cheaper to search through at every point (a small, FIXED stack rather than an ever-growing one), but genuinely unable to directly recall anything from further back than that stack currently holds.

### The formula

```
allowed(i, j) = (0 <= i - j < window_size)
mask(i, j) = 0        if allowed(i, j)
           = -inf      otherwise
```

Every row of the mask has AT MOST `window_size` zero entries (the allowed positions), versus `[02-causal-mask]`'s row `i` having `i + 1` zero entries, GROWING with position, unbounded as the sequence lengthens.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements sliding-window masking directly (like `[04-seq-modeling/02-embeddings/06-rope]` and GQA before it, it's specific enough to modern long-context LLM architectures that it lives in model-specific code), but Mistral's original release and several other modern LLMs use exactly this masking pattern, often paired with `torch.nn.functional.scaled_dot_product_attention`'s own optimized kernels (which accept an arbitrary additive mask, this one included, and remain efficient with it). Real, production implementations typically don't build the full `(seq_len, seq_len)` mask explicitly the way this question does for clarity; they skip computing scores for out-of-window key blocks entirely (closer to `[04-flash-attention]`'s chunked approach, restricted to only the in-window chunks), getting the compute savings directly rather than masking AFTER computing the full (wasted) scores.

## Explanation

`build_sliding_window_mask` computes `distance = i - j` for every `(i, j)` pair via broadcasting (`positions[:, None] - positions[None, :]`), then allows a position only when `0 <= distance < window_size`, combining `[02-causal-mask]`'s "no future" rule with a new "not too far past" rule in a single boolean condition, converted to an additive mask (`0.0` where allowed, `-inf` where forbidden) via `np.where`. `sliding_window_attention` builds this mask for the query's own sequence length and hands it straight to `[01-scaled-dot-product-attention]`'s `scaled_dot_product_attention`, unchanged, exactly the same "build a mask, pass it as an ordinary additive mask" pattern `[02-causal-mask]` and `[06-alibi]` both use elsewhere in this curriculum. The softmax step inside `scaled_dot_product_attention` handles the rest automatically: `-inf` entries become exactly `0` probability after exponentiating, so masked-out positions contribute nothing to the output, regardless of how the mask itself was constructed.
