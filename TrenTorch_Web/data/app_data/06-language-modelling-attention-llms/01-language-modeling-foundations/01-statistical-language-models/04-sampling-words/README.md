---
name: lm-sampling-words
title: Sampling Words from a Bigram Model
tags: [language-modeling, sampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

A probability table is also a generator. Start at the boundary symbol, draw the next symbol from that row's distribution, move to it, and repeat until the model draws the boundary again, which is how it says "this word is finished". The only primitive you need is a way to draw an index from a discrete distribution given one uniform random number. The clean way is inverse-transform sampling: lay the probabilities end to end along the interval from 0 to 1 as a cumulative sum, and the symbol whose segment contains the random number is the draw.

### From theory to code

Implement `sample_word(probs, itos, rng, max_len)`, which generates one word.

### Constraints

- `probs` is a row-stochastic `(V, V)` array and `itos[0]` is the boundary `.`. Start in row 0.
- Each step makes exactly one call `u = rng.random_sample()` and picks the first index `j` whose cumulative probability is strictly greater than `u`. Clamp to `V - 1` in case rounding leaves the last cumulative value just below `u`.
- Stop as soon as the drawn index is 0 and return the characters drawn so far joined into a string (the boundary is not included).
- Stop early with the characters so far if `max_len` characters have been generated.
- `rng` is a `np.random.RandomState`.

### Hints

<details>
<summary>Hint 1</summary>

`np.cumsum(probs[state])` gives the segment edges. `np.searchsorted(cum, u, side='right')` returns the first edge strictly greater than `u`.

</details>

<details>
<summary>Hint 2</summary>

Pinning one draw per step is what makes the output reproducible from a seed, so do not call `rng` anywhere else.

</details>

## Theory

### The simple version

Picture a dartboard split into slices whose widths are the probabilities. You throw one dart uniformly along the rim and read off the slice it lands in. Wide slices are hit often, thin slices rarely, and the process never needs to know anything about the other rows.

### The formula

With $F_j = \sum_{k \le j} p_k$ the cumulative distribution and $u \sim \text{Uniform}[0, 1)$,

$$
j = \min\{\, j : F_j > u \,\}
$$

has $P(j) = p_j$ exactly, since the event has length $F_j - F_{j-1} = p_j$. Starting from the boundary state and stopping on the boundary gives words of random length.

### How this is done in practice

`np.random.Generator.choice(p=...)` and `torch.multinomial` do the same draw. For large vocabularies the cumulative sum is replaced by faster alias tables or by sorting-based truncation (top-k, top-p), which later questions in this track build on. Sampling with a seed is how researchers make a generation reproducible.

## Explanation

The loop keeps a current state. Each iteration draws one uniform number, converts it to a symbol through the cumulative distribution and either stops on the boundary or appends the symbol. The `max_len` guard matters because a model can in principle keep drawing non-boundary symbols for a long time, and real systems always cap the generation length.
