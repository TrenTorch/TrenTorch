---
name: txf-modern-flash-attention
title: 'Note: FlashAttention, the same math computed without materializing the full attention matrix'
tags: [transformers]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`[03-attention-quadratic-complexity]` showed that the fully materialized attention weight matrix, shape `(seq_len, seq_len)` per head, is itself a quadratic-memory cost, separate from the quadratic COMPUTE cost. For long sequences, simply HOLDING that matrix in memory (even briefly) can become the actual bottleneck, especially on GPUs, where moving data between slow, large "HBM" memory and fast, small on-chip "SRAM" is often slower than the arithmetic itself. Dao et al. (2022, "FlashAttention") observed that the FINAL attention output never actually needs the full matrix to exist all at once: it only needs, for every query, a running WEIGHTED SUM over keys/values seen so far, exactly the kind of computation that can be done incrementally, in CHUNKS, never holding more than one chunk's worth of scores in memory at a time.

The trick that makes this work correctly is "online softmax" (Milakov & Gimelshein, 2018): softmax needs to know the MAXIMUM score (for numerical stability, `[01-scaled-dot-product-attention]`'s `- max` trick) and the SUM of exponentiated scores, both computed over the ENTIRE row, before it can produce a single normalized weight. Processing keys in chunks means neither the true max nor the true sum is known until the LAST chunk. Online softmax solves this by maintaining a RUNNING max and running sum, and RESCALING every previously-accumulated partial result whenever a new chunk reveals a larger max than seen so far, mathematically producing the EXACT same final answer as computing the whole row at once, just incrementally.

### From theory to code

Implement `flash_attention(query, key, value, block_size, mask)`, computing EXACTLY `[01-scaled-dot-product-attention]`'s output, but processing `key`/`value` in chunks of `block_size` along the key axis: maintain a running max, running softmax denominator, and running (unnormalized) output, updating all three after each chunk via the online-softmax rescaling rule, and dividing by the final running denominator only at the very end.

### Constraints

- Must produce EXACTLY the same output as computing full, unchunked attention, for ANY `block_size` from `1` up to `seq_len` (all inclusive).
- The running max must be updated with the TRUE maximum seen SO FAR (`max(running_max, this_chunk's_max)`), never a value from just the current chunk alone.
- Whenever the running max changes, every PREVIOUSLY accumulated quantity (the running sum, the running output) must be rescaled by `exp(old_max - new_max)` before adding the new chunk's contribution, or the result is mathematically wrong, not just imprecise.
- Never materialize a `(seq_len_q, seq_len_k)`-shaped score matrix; only ever a `(seq_len_q, block_size)`-shaped one, one chunk at a time.

### Hints

<details>
<summary>Hint 1: Per-chunk scores</summary>

For each chunk of keys/values: `scores = query @ swapaxes(key_chunk, -2, -1) / sqrt(d_k)` (plus the corresponding SLICE of `mask`, if given), exactly `[01-scaled-dot-product-attention]`'s formula, just restricted to this one chunk's keys.

</details>

<details>
<summary>Hint 2: The online-softmax update</summary>

```python
block_max = scores.max(axis=-1, keepdims=True)
new_max = np.maximum(running_max, block_max)
correction = np.exp(running_max - new_max)     # rescales everything accumulated so far
probs = np.exp(scores - new_max)

running_sum = correction * running_sum + probs.sum(axis=-1, keepdims=True)
running_output = correction * running_output + probs @ value_chunk
running_max = new_max
```

Initialize `running_max` to `-inf`, `running_sum` to `0`, `running_output` to `0` before the loop; `exp(-inf - new_max) = 0`, so the very first chunk's `correction` naturally contributes nothing from the (empty) initial state.

</details>

<details>
<summary>Hint 3: The final answer</summary>

After processing every chunk, `return running_output / running_sum`: the running output was accumulated UNNORMALIZED (weighted by un-normalized `exp` scores), and dividing by the final, TRUE softmax denominator at the very end normalizes it correctly, exactly matching what a single, whole-row softmax would have produced.

</details>

## Theory

### The simple version

Computing a class's average test score WITHOUT ever writing down every single score at once: reading scores one small STACK of papers at a time, keeping a running total and a running count, updating both after each stack, and only dividing total by count at the very end. Online softmax does the analogous thing for the "which value best matches this query" question, except each contribution also needs RESCALING whenever a new stack reveals a more extreme score than anything seen before, since softmax's normalization depends on the single largest score across the WHOLE row, not just whatever's been seen so far.

### The formula

```
running_max = -inf, running_sum = 0, running_output = 0
for each chunk of (key, value):
    scores      = Q @ chunk_K^T / sqrt(d_k)
    new_max     = max(running_max, max(scores, axis=-1))
    correction  = exp(running_max - new_max)
    probs       = exp(scores - new_max)
    running_sum    = correction * running_sum    + sum(probs, axis=-1)
    running_output = correction * running_output + probs @ chunk_V
    running_max = new_max
output = running_output / running_sum
```

Mathematically IDENTICAL to computing the whole row's softmax at once; only the memory access PATTERN differs.

### How PyTorch actually implements this

`torch.nn.functional.scaled_dot_product_attention` automatically dispatches to a genuine, highly-optimized FlashAttention kernel on supported GPUs (transparently, no code change required from the caller), specifically because it computes the exact SAME mathematical result as `[01-scaled-dot-product-attention]`'s naive formula while using dramatically less memory bandwidth. This question's chunked NumPy loop is not fast (the whole point of the real kernel is a hand-tuned GPU memory-access pattern, not a Python `for` loop), but it computes EXACTLY the same numbers, which is what actually matters for understanding the algorithm's correctness. `[05-sliding-window-attention]`, immediately following this question, is a genuinely DIFFERENT optimization: it reduces the actual amount of COMPUTE (fewer keys attended to at all), whereas FlashAttention computes the identical full-attention result, just without ever holding the whole thing in memory at once.

## Explanation

`flash_attention` loops over `key`/`value` in chunks of `block_size`, computing that chunk's scores exactly as `[01-scaled-dot-product-attention]` would, then applies the online-softmax update: `new_max` tracks the TRUE running maximum seen across every chunk so far, `correction = exp(running_max - new_max)` rescales everything accumulated BEFORE this chunk to be consistent with the new, larger maximum (this is the step that makes chunking mathematically exact rather than approximate), and both `running_sum` and `running_output` are updated by first applying that correction, then adding this chunk's own (rescaled, via `exp(scores - new_max)`) contribution. After every chunk has been processed, `running_output / running_sum` produces the correctly normalized final answer, identical to computing the whole `(seq_len_q, seq_len_k)` score matrix in one shot, despite never having held more than one `(seq_len_q, block_size)`-shaped chunk of scores in memory at any single point.
