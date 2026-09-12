---
name: txf-lm-temperature-topk-sampling
title: 'Stretch: temperature + top-k sampling'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[07-greedy-decoding]`'s `argmax` is entirely deterministic: the same input always produces the same output, and it always produces the SINGLE most likely continuation, never anything else, even when several plausible continuations exist with only slightly lower probability. For creative or varied generation (chat responses, story writing, anything where always producing the identical "safest" answer feels repetitive or dull), what's actually wanted is RANDOM sampling from the model's own predicted probability distribution, weighted by that distribution, not a hard argmax.

Two knobs give control over exactly how random: temperature RESHAPES the whole distribution before sampling (dividing logits by `temperature`, exactly `[02-modern-transformer-architecture/10-logit-scaling]`'s scaling operation, but user-chosen here rather than fixed by `d_model`, low temperature sharpens toward argmax-like behavior, high temperature flattens toward uniform randomness), and top-k FILTERS the candidate pool down to only the `k` highest-scoring tokens before sampling at all, preventing the model from ever picking something from deep in its low-probability tail, however unlikely, purely by chance.

### From theory to code

Implement `scale_and_filter_logits(logits_row, temperature, top_k)` (divide by temperature, then mask everything outside the top `k` to `-inf`), `sample_next_token(logits_row, temperature, top_k, rng)` (`scale_and_filter_logits` followed by `[04-seq-modeling/04-attention/03-softmax-last-axis]`'s softmax and a random draw), and `sample_decode`, `[07-greedy-decoding]`'s autoregressive loop with `sample_next_token` replacing `argmax`.

### Constraints

- `temperature` divides the logits BEFORE any top-k filtering; `top_k` filtering happens on the ALREADY-scaled logits.
- `top_k=None` means no filtering at all (sample from the full distribution); `top_k=1` reduces to `[07-greedy-decoding]`'s deterministic `argmax` behavior, since only the single highest-scoring token remains eligible.
- Masked-out (below top-`k`) logits become `-inf`, giving them exactly `0` probability after softmax, never merely a SMALL probability.
- `sample_next_token` draws using `rng.choice` (an explicitly-passed random state, for reproducibility across calls), never NumPy's unseeded global randomness.

### Hints

<details>
<summary>Hint 1: Scaling and filtering</summary>

```python
scaled = logits_row / temperature
if top_k is not None and top_k < len(scaled):
    threshold = np.sort(scaled)[-top_k]
    scaled = np.where(scaled >= threshold, scaled, -np.inf)
return scaled
```

`np.sort(scaled)[-top_k]` finds exactly the `top_k`-th highest value; everything strictly below it gets masked out.

</details>

<details>
<summary>Hint 2: Sampling</summary>

```python
probs = softmax_last_axis(scale_and_filter_logits(logits_row, temperature, top_k))
return int(rng.choice(len(probs), p=probs))
```

</details>

<details>
<summary>Hint 3: The generation loop</summary>

Identical to `[07-greedy-decoding]`'s loop, with `next_token = sample_next_token(logits[0, -1, :], temperature, top_k, rng)` replacing `next_token = np.argmax(logits[..., -1, :], axis=-1)`.

</details>

## Theory

### The simple version

`[07-greedy-decoding]`'s writer who always picks the single most obvious next word. Sampling is that same writer instead rolling a weighted die, where each candidate word's chance of being picked is proportional to how likely the model thinks it is, genuinely varying their output from one attempt to the next. Temperature is how "loaded" that die is (a very low temperature makes it almost always land on the single best word, functionally identical to the deterministic writer; a very high temperature makes it closer to a fair, unweighted die across everything). Top-k is a simpler, blunter restriction: before even rolling, physically remove every face of the die except the `k` most likely words, so however the die lands, it can never come up with something the model considered deeply implausible.

### The formula

```
scaled = logits / temperature
if top_k: scaled = mask_below_top_k(scaled, top_k, fill=-inf)
probs = softmax(scaled)
next_token ~ Categorical(probs)
```

`top_k=1` collapses `Categorical(probs)` down to a distribution with `100%` probability on a single token, exactly `[07-greedy-decoding]`'s `argmax`.

### How PyTorch actually implements this

`model.generate(input_ids, do_sample=True, temperature=T, top_k=K)` in Hugging Face `transformers` implements exactly this pattern, internally using `torch.multinomial` (PyTorch's categorical-sampling primitive) in place of this question's `rng.choice`. Real production sampling code often layers ADDITIONAL filtering on top of top-k (most commonly "top-p"/"nucleus" sampling, keeping the smallest set of tokens whose CUMULATIVE probability exceeds some threshold `p`, adapting the effective candidate pool size to how confident the distribution actually is at each step, rather than a fixed count), outside this question's scope but a direct extension of the exact mechanism built here.

## Explanation

`scale_and_filter_logits` divides every logit by `temperature` (reshaping the distribution's overall sharpness), then, if `top_k` is given, finds the `top_k`-th highest scaled logit via `np.sort(...)[-top_k]` and masks everything strictly below that threshold to `-inf`, guaranteeing exactly `0` probability for anything outside the top `k` after softmax. `sample_next_token` converts the filtered logits to a genuine probability distribution via `[03-softmax-last-axis]`'s `softmax_last_axis`, then draws one token id via `rng.choice(len(probs), p=probs)`, a true random draw weighted by that distribution rather than a deterministic `argmax`. `sample_decode` reuses `[07-greedy-decoding]`'s exact autoregressive loop structure (rebuild the causal mask, call `full_lm_forward`, extract the last position's logits, append the chosen token, repeat), with `sample_next_token` substituted in place of `argmax` as the only change.
