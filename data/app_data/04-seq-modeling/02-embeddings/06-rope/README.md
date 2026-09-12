---
name: seq-embeddings-rope
title: RoPE (Rotary Position Embeddings)
tags: [nlp, transformers, embeddings]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`[05-combine-token-positional-embeddings]`'s approach, add a positional vector to the token embedding once, right at the input, has a subtle limitation: that positional information has to survive, unmodified in spirit, through every subsequent layer of the network for attention to still make use of it many layers deep. RoPE (Su et al., 2021) takes a fundamentally different approach: instead of adding position information to the EMBEDDING, it applies a ROTATION directly to the query and key vectors INSIDE every attention layer, right before the attention score (`Scaled dot-product attention`, later in this Part) is computed from them. This isn't just a different place to inject the same information, it produces a genuinely different, and in practice very useful, mathematical property: the dot product between a rotated query at position `m` and a rotated key at position `n` depends ONLY on their RELATIVE distance, `m - n`, not on their absolute positions `m` and `n` individually.

This relative-position property matters enormously in practice: a model trained mostly on short sequences, where it only ever sees absolute positions up to, say, 2048, can often still handle a MUCH longer sequence at inference time, because what it actually learned to respond to is relative offsets ("the token 3 positions back"), a pattern that's exactly as valid at position 50000 as it is at position 50, whereas `[04-learned-positional-embedding]`'s fixed lookup table simply has no learned row at all for a position index it's never seen. This is a major reason RoPE, or close variants of it, is the standard positional scheme in most modern large language models (Llama, GPT-NeoX, and many others).

### From theory to code

Implement `compute_rope_angles(seq_len, dim)`, computing the rotation angle for every `(position, dimension-pair)` combination (same underlying frequency formula as `[03-sinusoidal-positional-encoding]`'s `div_term`). Implement `apply_rope(x, angles)`, rotating every consecutive PAIR of dimensions in `x` by that pair's own angle, treating `(x[..., 2i], x[..., 2i+1])` as the coordinates of a 2D point being rotated counterclockwise by `angles[..., i]` radians.

### Constraints

- `compute_rope_angles` returns shape `(seq_len, dim // 2)`: one angle per position, per dimension-PAIR (not per individual dimension).
- `apply_rope` must rotate `(x[..., 2i], x[..., 2i+1])` pairs using the standard 2D rotation matrix, applied independently to each pair with its own angle.
- Rotation must preserve each pair's VECTOR NORM exactly (a genuine rotation never changes a vector's length, only its direction).
- The dot product between two rotated vectors at different positions must depend only on their POSITIONS' DIFFERENCE, not on the absolute position values themselves.

### Hints

<details>
<summary>Hint 1: compute_rope_angles</summary>

Identical structure to `[03-sinusoidal-positional-encoding]`'s `div_term`/`position` computation: `freq = 10000.0 ** (-np.arange(0, dim, 2) / dim)` gives one frequency per dimension-pair, and `position * freq` (broadcasting a `(seq_len, 1)` column against a `(dim//2,)` row) gives every position's angle at every pair's frequency.

</details>

<details>
<summary>Hint 2: Splitting into pairs</summary>

`x1 = x[..., 0::2]` and `x2 = x[..., 1::2]` split `x`'s last dimension into its even-indexed and odd-indexed halves, EXACTLY the two coordinates of each consecutive pair, ready to rotate as 2D points.

</details>

<details>
<summary>Hint 3: The rotation itself</summary>

`np.empty_like(x)` for the output, then fill `rotated[..., 0::2] = x1 * cos(angles) - x2 * sin(angles)` and `rotated[..., 1::2] = x1 * sin(angles) + x2 * cos(angles)`, the standard 2D counterclockwise rotation matrix formula applied to each `(x1, x2)` pair independently.

</details>

## Theory

### The simple version

A row of clock hands, each starting pointed in some particular direction (the query or key vector's own learned "content"), and then EACH hand gets physically turned by an amount that depends on WHERE in the sequence it is, hand 1 (position 1) turns a little, hand 50 (position 50) turns a lot more. Comparing two hands' directions (the dot product attention actually computes) after they've both been turned still tells you something meaningful about how similar their ORIGINAL directions were, but now that comparison is also sensitive to how much MORE one hand was turned relative to the other, which is exactly the RELATIVE distance between their positions, this is the geometric intuition behind why rotating query/key vectors by a position-dependent angle makes their dot product depend on relative position.

### The formula

For a 2D pair `(x1, x2)` rotated by angle `theta`:

```
x1' = x1 * cos(theta) - x2 * sin(theta)
x2' = x1 * sin(theta) + x2 * cos(theta)
```

the standard 2D rotation matrix, `[x1' ; x2'] = [[cos, -sin], [sin, cos]] @ [x1 ; x2]`. Applied independently to every consecutive pair `(x[2i], x[2i+1])` in a `dim`-dimensional vector, with pair `i`'s own angle `theta_i(pos) = pos * 10000^(-2i/dim)` (identical frequency schedule to `[03-sinusoidal-positional-encoding]`).

The key property this achieves, stated precisely: for query `q` at position `m` and key `k` at position `n`, `RoPE(q, m) . RoPE(k, n)` depends on `q`, `k`, and `(m - n)` only, never on `m` and `n` individually. This follows from the rotation matrices' own algebra: rotating `q` by angle `m*theta` and `k` by angle `n*theta`, then taking their dot product, is mathematically equivalent to NOT rotating `q` at all and rotating `k` by angle `(n - m)*theta` instead, the SAME relative rotation, regardless of where `m` and `n` individually started.

### How PyTorch actually implements this

Nothing in core `torch.nn` implements RoPE directly (it's specific enough to Transformer/LLM architectures that it lives in model-specific code, like Hugging Face `transformers`' Llama implementation, or dedicated libraries), but every modern implementation computes exactly this pairwise rotation, typically fused into a single efficient kernel rather than the explicit even/odd-slice-and-recombine approach used here for clarity. RoPE is applied ONLY to queries and keys, never to values, since attention's actual output is a weighted SUM of value vectors (`Scaled dot-product attention`, next in this track), and rotating the values themselves would need to be carefully undone afterward, whereas rotating only q and k affects the attention SCORES (which token attends to which), leaving the values' own content completely untouched. A practical detail worth knowing: some real implementations (Llama's, notably) split `x` into its FIRST half and SECOND half (`x[..., :dim//2]` and `x[..., dim//2:]`) rather than the INTERLEAVED even/odd pairing used in this question and the original RoFormer paper; both are valid, mathematically equivalent (up to a fixed permutation of which dimensions get paired together) formulations of the same underlying rotation idea, and the choice between them is purely an implementation convention, not a difference in what RoPE actually accomplishes.

## Explanation

`compute_rope_angles` computes `position * freq`, where `position` is a `(seq_len, 1)` column of position indices and `freq` is a `(dim // 2,)` array of `10000^(-2i/dim)` values, one per dimension-pair, exactly mirroring `[03-sinusoidal-positional-encoding]`'s frequency schedule, producing a `(seq_len, dim // 2)` matrix of every position's rotation angle at every pair.

`apply_rope` splits `x`'s last dimension into `x1 = x[..., 0::2]` and `x2 = x[..., 1::2]` (the two coordinates of each consecutive pair), computes `cos(angles)` and `sin(angles)`, and fills a fresh output array's even positions with `x1*cos - x2*sin` and odd positions with `x1*sin + x2*cos`, the standard 2D rotation matrix applied independently to every pair, each pair rotated by its own angle from `angles`.
