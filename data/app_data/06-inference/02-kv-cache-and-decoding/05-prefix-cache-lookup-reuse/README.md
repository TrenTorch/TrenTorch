---
name: inf-kv-prefix-cache
title: 'Prefix Cache Lookup and Reuse'
tags: [inference, kv-cache, prefix-caching, serving]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Many real workloads repeatedly send requests that share a long common prefix — a system prompt, a few-shot template, a long document being asked multiple questions about. Recomputing that shared prefix's KV cache from scratch every request wastes both compute and time-to-first-token. Implement automatic prefix caching: given a store of previously computed KV-cache blocks keyed by the hash of the token sequence they represent, find the longest matching prefix of a new request's tokens already in the store, and report how many tokens (and blocks) of prefill computation can be skipped by reusing it.

### From theory to code

```
hash_i = H(hash_{i-1}, block_i)   with hash_{-1} = SEED   -- chained hash per block
reused_tokens = block_size * (number of leading blocks whose chained hash is a cache hit)
```

### Constraints

- Tokens are grouped into non-overlapping blocks of `block_size` (a trailing partial block never counts as reusable and is not added to the store as a partial hash).
- Use a hash chained across blocks so a match at block `i` requires every earlier block to also match.
- Report the number of tokens/blocks reused from the cache and the exact token ids that still need prefilling.
- After processing, insert the new request's full block hashes into the store for future reuse.

### Hints

<details>
<summary>Hint: Chaining is what makes it a prefix match</summary>

Chain the hash across blocks (`hash_i` depends on `hash_{i-1}`) so a match at block `i` can only happen if every earlier block matched too — this is what makes it a genuine PREFIX match rather than a coincidental match of an isolated block deeper in the sequence.

</details>

<details>
<summary>Hint: Stop at the first miss</summary>

Stop walking forward at the first block whose chained hash is not already in the store — every block after a miss must be treated as new regardless of its own content, since the chaining means a later "match" would be coincidental, not a genuine shared prefix.

</details>

## Theory

### The simple version

Two students who both start their essay with the exact same opening paragraph can share that paragraph's "already graded" status — but if their second paragraphs diverge, nothing about a coincidentally similar THIRD paragraph later on should count as shared, since it wasn't reached by the same path. Prefix caching keeps track of "graded so far" checkpoints chained in order, so only genuine shared beginnings count as reusable.

### The formula

```
hash_i = H(hash_{i-1}, block_i),  hash_{-1} = SEED
walk hashes forward while each is in cache_store; matched_blocks = count before first miss
reused_tokens = block_size * matched_blocks
```

A new request walks its own token blocks, checks each chained hash against the store, and stops at the first miss: everything before that miss can reuse a previously computed cache instead of being prefilled again.

### How PyTorch actually implements this

This is cache/string bookkeeping, not tensor math — the same routine sits in front of whichever framework (NumPy or PyTorch) actually stores and reuses the KV tensors for the matched blocks. vLLM's "automatic prefix caching" feature implements exactly this chained-hash scheme in production.

## Explanation

Because each block's hash is computed from `(previous_hash, this_block)`, a hit at block index `i` is only possible if the identical chain of blocks `0..i` occurred in some earlier request — an isolated identical block deeper in the sequence cannot produce a false hit, which is exactly the difference between prefix matching and plain block deduplication. This chaining property is what lets `[04-paged-attention-block-allocation]`'s physical blocks be safely shared between two sequences with a common prefix: because a hash match guarantees the entire prefix leading to it is identical, the underlying KV values are guaranteed byte-identical too, so reusing the physical block (rather than recomputing it) never changes the model's output.
