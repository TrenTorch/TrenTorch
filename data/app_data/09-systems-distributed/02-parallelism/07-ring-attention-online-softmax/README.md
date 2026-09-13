---
name: systems-distributed-ring-attention-online-softmax
title: 'Note: Sequence/Context Parallelism, Splitting One Long Sequence Across GPUs'
tags: [transformers, mlops, distributed-training]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`06-tensor-parallel-matmul` could split a matmul cleanly because a matmul's output elements don't depend on each other. Attention is different: softmax is a genuinely GLOBAL operation over the whole key/value sequence — every output row needs to know the max score and the total normalizer across _every_ key, not just the ones on its own GPU — so naively splitting the sequence across GPUs and computing softmax independently on each piece gives the WRONG answer. Sequence/context parallelism needs a smarter algorithm to fix this.

### From theory to code

Implement `attention_chunk_stats` (the "online softmax" running statistics for one key/value chunk), `merge_chunk_stats` (the rescale-and-combine rule for merging two chunks' statistics), and `ring_attention`, which processes key/value chunks one at a time — as if each arrived from the next GPU around a ring — while never materializing the full attention matrix over the whole sequence at once.

### Constraints

- `attention_chunk_stats(query, key_chunk, value_chunk)` returns `(chunk_output, chunk_sum, chunk_max)`: the un-normalized weighted value sum, the un-normalized softmax denominator, and the row-wise max score, computed AS IF this chunk were the only one that existed.
- `merge_chunk_stats` must rescale BOTH the accumulator and the new chunk onto a shared new max (`max(acc_max, chunk_max)`) before adding them — never add stats computed relative to different maxes directly.
- `ring_attention(query, key_chunks, value_chunks)` must produce the exact same result as computing ordinary attention over the full, concatenated key/value sequence directly, for any way of splitting the sequence into chunks (even chunks of size 1).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`attention_chunk_stats` is nearly identical to `01-scaled-dot-product-attention`'s own softmax-stability trick (subtract the row max before exponentiating) — the only difference is it returns the un-normalized numerator and denominator SEPARATELY, instead of dividing them into a final weight matrix right away.

</details>

<details>
<summary>Hint 2</summary>

When merging accumulator state (relative to `acc_max`) with a new chunk's state (relative to `chunk_max`), both need to be multiplied by `exp(their_own_max - new_max)` before being added — this is the exact correction factor that "undoes" each one's own max-subtraction and re-expresses both relative to the same new shared max.

</details>

## Theory

### The simple version

Imagine three separate people each reading a different third of a long list of numbers and, independently, finding their OWN third's maximum and computing `sum(exp(x - their_own_max))` for their third. None of their three sums are directly comparable or addable yet, because each was computed relative to a _different_ max — but if each person first rescales their own sum by `exp(their_max - overall_max)` (once someone tells them the TRUE overall max), all three rescaled sums become directly addable, and the total is exactly what one person computing over the whole list at once would have gotten. This "online softmax" trick is exactly how ring attention combines each GPU's partial attention computation into the one true, globally-correct answer.

### The formula

```text
attention_chunk_stats(q, k_chunk, v_chunk):
    scores = q @ k_chunk.T / sqrt(d_k)
    chunk_max = row-wise max(scores)
    exp_scores = exp(scores - chunk_max)
    chunk_output = exp_scores @ v_chunk        # un-normalized numerator
    chunk_sum = row-wise sum(exp_scores)       # un-normalized denominator

merge_chunk_stats(acc_output, acc_sum, acc_max, chunk_output, chunk_sum, chunk_max):
    new_max = max(acc_max, chunk_max)
    acc_output = acc_output * exp(acc_max - new_max) + chunk_output * exp(chunk_max - new_max)
    acc_sum    = acc_sum    * exp(acc_max - new_max) + chunk_sum    * exp(chunk_max - new_max)

ring_attention(q, key_chunks, value_chunks) = final_acc_output / final_acc_sum
```

The key insight is that this ring-processed, chunk-at-a-time computation is mathematically IDENTICAL to computing attention over the whole concatenated sequence at once — no approximation is involved — while never requiring any single GPU to hold the full key/value sequence, or the full `seq_len × seq_len` attention matrix, in memory simultaneously.

### How PyTorch actually implements this

Context only, untested by your submission: this online-softmax technique was introduced by Milakov & Gimelshein (2018) and is the core trick behind FlashAttention (Dao et al., 2022), which uses it to avoid ever materializing the full attention matrix even on a single GPU (for memory-bandwidth reasons). Ring Attention (Liu, Zaharia & Abbeel, 2023) applies the exact same online-softmax merge rule across GPUs instead of across memory tiles — each GPU holds one chunk of the sequence's K/V, passes its chunk around a logical ring to every other GPU in turn, and every GPU accumulates the running (output, sum, max) state for its own queries exactly as `ring_attention` does here.

## Explanation

`attention_chunk_stats` computes exactly the numerator and denominator a normal softmax-attention computation would produce for one key/value chunk in isolation, subtracting that chunk's own max for numerical stability — matching `01-scaled-dot-product-attention`'s stabilization trick, just without the final division.

`merge_chunk_stats` is the online-softmax correction step: since the accumulator and the new chunk were each computed relative to their OWN max, both get rescaled by `exp(old_max - new_max)` — a factor of exactly `1` when a max didn't change, and correctly less than `1` when it did — before being summed, so the running total always stays expressed relative to a single, consistent, up-to-date max.

`ring_attention` loops over the key/value chunks exactly once each (as a real ring topology would deliver them, one hop at a time), maintaining only the three running accumulators — never touching more than one chunk's worth of keys/values at any moment — and only divides `acc_output` by `acc_sum` at the very end. This exercise's `tests.py` verifies the result matches ordinary full-sequence attention (`01-scaled-dot-product-attention`) exactly, for chunk counts ranging from `1` up to one chunk per token, uneven chunk sizes, and deliberately large-magnitude scores designed to make a "forgot to rescale" mutant produce a visibly wrong answer.
