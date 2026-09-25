---
name: systems-distributed-kv-cache-autoregressive-generation
title: 'KV-Cache for Autoregressive Generation (Reuses the Inference Section Directly)'
tags: [transformers, mlops, memoization]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`06-inference/02-kv-cache-and-decoding` already built a real, working KV-cache: it computes `K`/`V` for the prompt once during prefill, then for every new generated token, projects only that _one_ new token's `K`/`V` and appends them to a running cache — it never recomputes `K`/`V` for tokens that were already processed. This question makes the _reason_ that matters concrete: implement the naive alternative (recompute everything, every step) and prove the two produce numerically identical results, which is exactly what makes caching a pure optimization rather than an approximation.

### From theory to code

Implement `generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens)`, the same autoregressive generation task with no cache at all, and `outputs_match(...)`, which verifies it against `06-inference`'s real `autoregressive_decode_with_cache` directly.

### Constraints

- `generate_without_cache` returns the exact same dict shape as `autoregressive_decode_with_cache`: `{"prefill_output", "generated_outputs", "final_cache_len"}`.
- At every new token, `generate_without_cache` recomputes `Q`, `K`, `V` for the _entire_ sequence-so-far from scratch (no incremental reuse of any previous computation).
- `outputs_match` returns `True` iff both implementations agree, within floating-point tolerance, on both `prefill_output` and `generated_outputs`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Write one helper — a plain, full causal-attention forward pass over an arbitrary-length sequence — and call it fresh, on the whole growing sequence, at every single step. Nothing from a previous call should be reused.

</details>

<details>
<summary>Hint 2</summary>

After appending each new token and re-running the full forward pass over the now-longer sequence, only the _last row_ of that pass's output is this step's actual generated output — every earlier row is being needlessly recomputed, which is exactly the point.

</details>

## Theory

### The simple version

Imagine re-reading an entire book from page one, every single time you want to know what happens on the next new page someone hands you — versus keeping a bookmark and your notes from what you've already read, and only reading the one new page. Both approaches eventually tell you what the new page says; one of them just redoes an enormous, entirely unnecessary amount of work to get there. A KV-cache is exactly the bookmark-and-notes approach applied to attention: the keys and values for tokens already processed never change, so recomputing them at every step is pure waste.

### The formula

```text
generate_without_cache(X_prompt, W_Q, W_K, W_V, new_tokens):
    prefill_output = full_causal_attention(X_prompt)
    sequence = X_prompt
    for x_new in new_tokens:
        sequence = append(sequence, x_new)
        full_output = full_causal_attention(sequence)     # recomputes EVERYTHING, every step
        generated_outputs.append(full_output[-1])          # only the new row is actually needed
```

### How PyTorch actually implements this

Context only, untested by your submission: real production LLM serving (`vLLM`, Hugging Face `transformers`' `generate()` with `use_cache=True`, and every serious inference engine) uses exactly the incremental scheme `06-inference`'s `autoregressive_decode_with_cache` implements — `02-benchmark-with-vs-without-cache`, this track's next question, quantifies exactly how much redundant work a naive, cache-free implementation like this one actually wastes as generation gets longer.

## Explanation

`generate_without_cache` defines one inner helper, `full_forward`, that computes `Q, K, V` for whatever sequence it's given, applies causal masking, and returns the full attention output — this is the _entire_ forward pass, run completely fresh every time it's called. `prefill_output` is exactly one call to this helper on `X_prompt`. Then, for each new token, the sequence grows by one row and `full_forward` runs again on the _whole_ now-longer sequence — every previous token's `Q`, `K`, `V`, and attention output get recomputed identically to what was already computed in the previous step, and only `full_output[-1]` (the newest position's result) is actually kept.

`outputs_match` calls both `autoregressive_decode_with_cache` (the real, cached implementation) and `generate_without_cache` with identical inputs, and compares `prefill_output` and `generated_outputs` with `np.allclose` — since both implementations compute the mathematically identical attention operation, just with different amounts of redundant recomputation, any genuine implementation of either one must produce matching numbers, within ordinary floating-point tolerance.
