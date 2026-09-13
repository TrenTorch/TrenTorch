---
name: systems-distributed-benchmark-with-vs-without-cache
title: 'Benchmark: With vs Without Cache'
tags: [transformers, mlops, memoization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-kv-cache-autoregressive-generation` proved caching and no-caching produce identical _results_. That leaves the actual practical question unanswered: exactly how much redundant work does skipping the cache cost, and how does that cost grow as generation gets longer? This question answers it with real, closed-form accounting rather than a hard-to-trust wall-clock timing (which plain NumPy on tiny arrays can't demonstrate reliably).

### From theory to code

Implement `naive_kv_projection_work(prompt_len, num_new_tokens)`, the total "K/V projection" work `generate_without_cache` actually performs (reprojecting the _entire_ sequence-so-far at every step), `cached_kv_projection_work(...)`, the equivalent for the real cached implementation, and `cache_work_reduction_factor(...)`, their ratio.

### Constraints

- Counting one token's `K`/`V` projection as one unit of work: `naive_kv_projection_work` sums `(prompt_len + step)` for `step` from `1` to `num_new_tokens` — at each step, the _entire_ current sequence gets reprojected.
- `cached_kv_projection_work` returns `prompt_len + num_new_tokens` — the prompt once, plus exactly one unit per new token.
- `cache_work_reduction_factor` returns `naive_kv_projection_work / cached_kv_projection_work`.
- `num_new_tokens = 0` gives `naive_kv_projection_work = 0` and `cache_work_reduction_factor = 0.0`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

At step `i` (1-indexed), the current total sequence length is `prompt_len + i` — that's exactly how many tokens `generate_without_cache` reprojects at that step, since it recomputes everything from scratch every time.

</details>

<details>
<summary>Hint 2</summary>

`naive_kv_projection_work` is an arithmetic series: `sum_{i=1}^{N} (P+i) = N*P + N*(N+1)/2` — you can compute it with a loop or with this closed form directly.

</details>

## Theory

### The simple version

Imagine two ways of maintaining a running total across a list of numbers as new ones arrive: one way re-adds every number in the list from scratch every time a new one is appended, the other keeps the running total and just adds the one new number to it. Both give the same final answer, but the first does dramatically more and more redundant work the longer the list gets — exactly the shape of the gap between naive, cache-free generation and real KV-cached generation.

### The formula

```text
naive_kv_projection_work(P, N)  = sum_{i=1}^{N} (P + i) = N*P + N*(N+1)/2
cached_kv_projection_work(P, N) = P + N

cache_work_reduction_factor = naive_kv_projection_work / cached_kv_projection_work
```

The naive approach's work grows _quadratically_ in `N` (the `N*(N+1)/2` term), while the cached approach's work grows only _linearly_ in `N` — for a long enough generation, the naive approach's redundant work dominates completely, which is exactly why KV-caching matters more and more as sequences get longer, not less.

### How PyTorch actually implements this

Context only, untested by your submission: this is the exact, standard justification cited for KV-caching in real LLM serving literature and framework documentation — without a cache, generating `N` tokens autoregressively costs `O(N^2)` total attention-related work (as this accounting shows), while a KV-cache reduces it to `O(N)`, the difference this exercise's `cache_work_reduction_factor` measures directly.

## Explanation

`naive_kv_projection_work` sums `(prompt_len + step)` across every step from `1` to `num_new_tokens` — matching, unit for unit, exactly how many tokens `01-kv-cache-autoregressive-generation`'s real `generate_without_cache` reprojects at each of its steps, verified directly against that real implementation in this exercise's own `tests.py`.

`cached_kv_projection_work` is a flat `prompt_len + num_new_tokens` — the prompt's tokens get projected exactly once during prefill, and each new token contributes exactly one more unit of work for its own projection, with no token ever reprojected twice.

`cache_work_reduction_factor` divides the two, producing a ratio that grows without bound as `num_new_tokens` grows — a direct, quantitative statement of how much worse a cache-free implementation gets, specifically as generations get longer, which is exactly the regime real LLM serving cares about most.
