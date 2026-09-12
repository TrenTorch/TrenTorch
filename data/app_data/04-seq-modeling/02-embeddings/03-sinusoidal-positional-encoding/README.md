---
name: seq-embeddings-sinusoidal-positional-encoding
title: Sinusoidal positional encoding
tags: [nlp, transformers, embeddings]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Scaled dot-product attention`, later in this Part, processes every position in a sequence essentially in PARALLEL: unlike `[02-recurrent-neural-networks]`'s RNN cell, which processes tokens one at a time IN ORDER (and so implicitly knows position 5 comes after position 4, just from the order it was fed in), attention has no such built-in sense of order at all, if you fed it the SAME set of tokens in a scrambled order, attention's core computation would treat them identically, completely blind to word order. "The dog bit the man" and "the man bit the dog" would look identical to a purely attention-based model unless something explicitly tells it which token came first.

The original Transformer paper's fix: add a POSITIONAL ENCODING vector to each token's embedding (`[04-combine-token-and-positional-embeddings]`, immediately after this question, does exactly that combination) before attention ever sees it, a fixed pattern that's DIFFERENT for every position, so position 0's encoding is distinguishable from position 1's, which is distinguishable from position 2's, and so on. The sinusoidal choice specifically (sine and cosine waves at many different frequencies) has a clever mathematical property that made it especially appealing for the original paper's design: because of the trigonometric angle-addition identities, the encoding for position `pos + k` can be written as a fixed LINEAR function of the encoding for position `pos` (for any fixed offset `k`), which the paper's authors hypothesized would make it easy for the model to learn to attend to RELATIVE positions (e.g. "the token 3 positions back") as well as absolute ones.

### From theory to code

Implement `sinusoidal_positional_encoding(seq_len, d_model)`, building the full `(seq_len, d_model)` table. Even-indexed dimensions (`0, 2, 4, ...`) use `sin`, odd-indexed dimensions (`1, 3, 5, ...`) use `cos`, both driven by the SAME underlying value, `position / 10000^(2i/d_model)`, but each dimension pair `(2i, 2i+1)` uses a progressively LOWER frequency as `i` increases (dimension 0/1 oscillates fastest across positions; the last dimension pair oscillates slowest).

### Constraints

- Row `pos=0` must be exactly `[0, 1, 0, 1, ...]` (`sin(0) = 0`, `cos(0) = 1`, for every dimension pair, since `0 / anything = 0`).
- Even-indexed columns (`0, 2, 4, ...`) use `sin`; odd-indexed columns (`1, 3, 5, ...`) use `cos`.
- The frequency term `10000^(2i/d_model)` must GROW with `i` (making the effective angular frequency, its reciprocal, SHRINK), so lower dimension-pairs oscillate faster across positions than higher ones.
- Output shape must be exactly `(seq_len, d_model)`.

### Hints

<details>
<summary>Hint 1: Building the angle values first</summary>

`position = np.arange(seq_len)[:, None]` gives a `(seq_len, 1)` column of positions. `div_term = np.exp(np.arange(0, d_model, 2) * -(np.log(10000.0) / d_model))` computes `1 / 10000^(2i/d_model)` for every `i`, using the identity `10000^(-2i/d_model) = exp(-2i/d_model * log(10000))`, a numerically stable way to compute the same value. `position * div_term` (broadcasting a `(seq_len, 1)` array against a `(d_model/2,)` array) gives every position's angle at every frequency in one `(seq_len, d_model/2)` matrix.

</details>

<details>
<summary>Hint 2: Filling in sin and cos</summary>

Start with `pe = np.zeros((seq_len, d_model))`. Assign `pe[:, 0::2] = np.sin(position * div_term)` (every EVEN column, via NumPy's step-slicing) and `pe[:, 1::2] = np.cos(position * div_term)` (every ODD column), both driven by the SAME `position * div_term` matrix computed in Hint 1.

</details>

<details>
<summary>Hint 3: Sanity-check row 0</summary>

At `pos=0`, `position * div_term` is all zeros regardless of `div_term`'s actual values, so `sin(0) = 0` fills every even column and `cos(0) = 1` fills every odd column: row 0 should come out as `[0, 1, 0, 1, ...]` exactly, a quick way to sanity-check your implementation by hand.

</details>

## Theory

### The simple version

A clock with many concentric hands, all sharing the same center but spinning at wildly different speeds: a fast second hand, a slower minute hand, an even slower hour hand, and beyond that, hands that take a day, a week, a year to complete one revolution. Reading off the exact combined position of every hand at once uniquely identifies a specific MOMENT in a very long cycle, in a way no single hand alone ever could (the second hand alone repeats every 60 seconds; the SNAPSHOT of all of them together doesn't meaningfully repeat for a very long time). Sinusoidal positional encoding works the same way: each dimension-pair is a "hand" spinning at its own frequency, and the full 512 (or however many) dimensions together uniquely encode a specific POSITION, far beyond what any single frequency alone could distinguish.

### The formula

```
PE(pos, 2i)   = sin(pos / 10000^(2i / d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i / d_model))
```

for `i = 0, 1, ..., d_model/2 - 1`. Equivalently, letting `div_term[i] = 10000^(-2i/d_model)`:

```
angle(pos, i) = pos * div_term[i]
PE(pos, 2i)   = sin(angle(pos, i))
PE(pos, 2i+1) = cos(angle(pos, i))
```

### How PyTorch actually implements this

Nothing in `torch.nn` builds this directly (it's typically a small custom module or buffer in a Transformer implementation, since it's a fixed, non-learned table rather than a trained layer), but it's exactly what the original "Attention Is All You Need" paper (Vaswani et al., 2017) specified, and it's still used as-is or with minor variants in many Transformer implementations today. It's usually registered as a `buffer` (not a `Parameter`, exactly the same distinction `[03-dl-training/05-why-deep-networks-work/04-batchnorm]`'s `running_mean`/`running_var` made: tracked with the model's state, but never updated by an optimizer, since these values are computed once from a formula and never trained). `[04-combine-token-and-positional-embeddings]`, right after this question, adds this table directly to `[01-token-embedding-lookup]`'s token embeddings; `Learned positional embedding`, the alternative approach covered earlier in this same track, replaces this fixed sinusoidal formula with a genuinely trainable embedding table instead (one row per position, learned via gradient descent exactly like a token embedding), a simpler but less naturally length-extrapolating alternative; `RoPE (Rotary Position Embeddings)`, the most advanced approach in this track, takes the "combine multiple rotating frequencies" idea from sinusoidal encoding even further, applying rotation directly to the QUERY and KEY vectors inside attention itself rather than adding a separate table to the embeddings up front.

## Explanation

`sinusoidal_positional_encoding` first computes `position`, a `(seq_len, 1)` column of every position index, and `div_term`, a `(d_model/2,)` array of `1/10000^(2i/d_model)` values (one per dimension-pair, computed via `exp(-2i/d_model * log(10000))` for numerical stability). Broadcasting `position * div_term` produces a `(seq_len, d_model/2)` matrix of every position's angle at every frequency in one shot.

It then fills a `(seq_len, d_model)` zero matrix's EVEN columns (`pe[:, 0::2]`) with `sin` of that angle matrix, and its ODD columns (`pe[:, 1::2]`) with `cos` of the SAME angle matrix, producing the full alternating sin/cos table the formula specifies, with each dimension-pair's own characteristic frequency baked in via `div_term`.
