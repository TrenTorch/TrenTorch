---
name: txf-lm-greedy-decoding
title: 'Greedy decoding / generation'
tags: [transformers, nlp]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Everything built so far in this Part produces logits GIVEN a full sequence of tokens; actually GENERATING new text means running the model repeatedly, each time feeding it everything produced SO FAR and asking it what should come next. The simplest possible decision rule: always pick whichever token the model's own logits rank HIGHEST, append it, and repeat, "greedy" decoding, since it greedily takes the single best-looking option at every step with no lookahead, no consideration of how that choice affects future steps.

Every autoregressive generation step must respect causality: `[02-modern-transformer-architecture/01-encoder-decoder-arrangements]`'s decoder framing applies directly here, since the model must never be allowed to "see" a token that hasn't been generated (and appended) yet, exactly `[04-seq-modeling/04-attention/02-causal-mask]`'s causal mask, rebuilt fresh at every step as the sequence GROWS.

### From theory to code

Implement `greedy_decode(token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, num_new_tokens)`: repeatedly call `[04-full-forward-pass]`'s `full_lm_forward` (with a causal mask sized to the CURRENT sequence length) on the sequence so far, take `argmax` of the LAST position's logits, append that token, and repeat `num_new_tokens` times.

### Constraints

- The causal mask is rebuilt at EVERY step, sized to the current (growing) sequence length, never a fixed size computed once upfront.
- Only the LAST position's logits determine the next token (`logits[..., -1, :]`); earlier positions' logits were already used to predict THEIR own next tokens in previous steps, and are not reconsidered.
- `argmax` breaks ties deterministically (NumPy's own convention: the FIRST maximal index), so running the same inputs twice produces IDENTICAL output, no randomness anywhere in greedy decoding.
- The final result's first `token_ids.shape[-1]` positions are exactly the ORIGINAL input, unchanged; only new tokens are appended after it.

### Hints

<details>
<summary>Hint 1: One generation step</summary>

```python
seq_len = token_ids.shape[-1]
mask = build_causal_mask(seq_len)
logits = full_lm_forward(token_ids, token_embedding_table, blocks_params, num_heads, tied, output_weight, mask=mask)
next_token_logits = logits[..., -1, :]
next_token = np.argmax(next_token_logits, axis=-1)
```

</details>

<details>
<summary>Hint 2: Appending and looping</summary>

`token_ids = np.concatenate([token_ids, next_token[..., None]], axis=-1)`, repeated `num_new_tokens` times in a `for` loop, with `token_ids` REASSIGNED each iteration so the next call to `full_lm_forward` sees the newly-grown sequence.

</details>

## Theory

### The simple version

Writing a sentence one word at a time by always picking whatever single word seems MOST likely right now, given everything written so far, never reconsidering a choice once made and never looking more than one word ahead. This is fast and simple, but it's exactly the kind of strategy that can talk itself into a corner: the single most likely word at each individual step doesn't always add up to the single most likely SENTENCE overall, a limitation `[09-beam-search-decoding]`, later in this track, directly addresses by keeping several candidate continuations in play simultaneously instead of committing to just one.

### The formula

```
for step in range(num_new_tokens):
    mask = causal_mask(len(token_ids))
    logits = full_lm_forward(token_ids, ..., mask=mask)
    next_token = argmax(logits[:, -1, :])
    token_ids = concat(token_ids, next_token)
```

Runs the ENTIRE forward pass again at every single step (recomputing every earlier position's attention too, not just the new one), a real, known inefficiency of naive autoregressive generation that production inference systems address with a "KV cache" (caching earlier positions' key/value vectors instead of recomputing them from scratch every step), a technique outside this question's scope but directly motivated by exactly this repeated-recomputation pattern.

### How PyTorch actually implements this

`model.generate(input_ids, do_sample=False)` in Hugging Face `transformers` implements exactly this greedy strategy by default (`do_sample=False` disables `[08-temperature-topk-sampling]`'s randomness entirely), internally using a KV cache for efficiency rather than this question's naive "recompute everything every step" approach, but computing the identical SEQUENCE of chosen tokens either way. `[08-temperature-topk-sampling]`, immediately following this question, replaces the deterministic `argmax` with a genuinely RANDOM choice, weighted by probability, when some variety in the output is actually desired instead of always the single most likely continuation.

## Explanation

`greedy_decode` loops `num_new_tokens` times, and at every iteration: builds a fresh causal mask sized to the CURRENT sequence length (growing by one each iteration), calls `[04-full-forward-pass]`'s `full_lm_forward` on the full sequence generated so far, extracts only the LAST position's logits (`logits[..., -1, :]`, the model's prediction for what comes immediately after everything generated so far), takes their `argmax` to get the single highest-scoring next token, and appends it via `np.concatenate`. Because `token_ids` is reassigned at the end of each loop iteration, the NEXT call to `full_lm_forward` automatically sees the newly-extended sequence, correctly conditioning each new prediction on every token generated so far, including the ones this very function generated in earlier iterations of its own loop.
