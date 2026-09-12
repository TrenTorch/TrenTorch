---
name: inf-kv-paged-attention
title: 'PagedAttention Block Allocation (as used in vLLM)'
tags: [inference, kv-cache, paged-attention, memory-management]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Naively, each sequence's KV cache is pre-allocated as one contiguous buffer sized for the maximum sequence length, wasting huge amounts of memory whenever actual generations are shorter than the max — extremely common. PagedAttention (as used in vLLM) borrows the operating-system idea of paged virtual memory: the KV cache is divided into fixed-size physical blocks, and each sequence gets a logical-to-physical block table it appends to as it grows, allocating new physical blocks on demand and freeing them when the sequence finishes.

### From theory to code

```
n_blocks_needed = ceil(L / block_size)     -- L = sequence length so far
used_bytes = (sum of allocated_blocks over live sequences) * bytes_per_block
```

### Constraints

- Process a list of events in order: `('append', seq_id)` adds one token to that sequence (allocating a new block only if the current last block is full or the sequence has none yet), and `('free', seq_id)` releases all of that sequence's blocks back to the free pool.
- Report an out-of-memory condition if an append needs a new block but none are free — stop processing further events at that point.
- Return, after processing all events: each live sequence's logical block table (ordered list of physical block ids) and the number of free blocks remaining.

### Hints

<details>
<summary>Hint: When exactly to allocate</summary>

Only allocate a new physical block when the sequence's current block is full AND it needs to grow further — don't allocate ahead of need. A sequence needs a fresh block exactly when its token count is an exact multiple of `block_size` (its current last block just filled up, or it has none yet).

</details>

<details>
<summary>Hint: A simple free list is enough</summary>

Track a free list (e.g. a list of unused block ids). Popping/pushing from it is all "allocate"/"free" really do — no more complex data structure is needed for this simplified version.

</details>

## Theory

### The simple version

Like an operating system's paged virtual memory: instead of reserving one giant contiguous block of RAM per program (wasteful if the program ends up using less than reserved), memory is handed out in small fixed-size pages, on demand, as the program actually needs more. A sequence's KV cache works the same way — physical blocks are handed out lazily as tokens are generated, and returned to the pool the instant a sequence finishes.

### The formula

```
n_blocks_needed(L) = ceil(L / block_size)
new block allocated exactly when current_token_count % block_size == 0
```

New physical blocks are allocated from a free list only when a sequence actually needs more room (lazily, one block at a time) and returned to the free list the moment the sequence finishes — so memory tracks ACTUAL usage instead of worst-case usage, and a free block from a finished sequence can immediately serve a new one.

### How PyTorch actually implements this

This is a pure memory-management simulation over Python data structures — there is no tensor math to port to PyTorch. A real vLLM-style implementation applies this exact logic to index into a physical `torch.Tensor` KV cache pool instead of a Python list, but the block-table bookkeeping itself is framework-agnostic.

## Explanation

A sequence only ever needs a fresh block exactly when its token count is an exact multiple of `block_size` (its current last block just filled up, or it has none yet) — checking `n % block_size == 0` before incrementing `n` captures precisely that moment, so blocks are allocated lazily one at a time rather than reserved up front. This lazy-allocation property is exactly what makes PagedAttention's memory usage track actual generation length instead of a worst-case maximum: a sequence that finishes after 5 tokens with `block_size=16` only ever holds 1 block, never the many blocks a naive pre-allocation scheme sized for the maximum possible length would have reserved.
