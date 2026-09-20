---
name: production-multimodal-atomic-chunking
title: Chunk Multimodal Content Without Splitting Atomic Blocks
tags: [production-systems, multimodal, chunking]
difficulty: Medium
---

## Statement

### The problem, from first principles

Fixed-size chunking (covered elsewhere in this curriculum) cuts text at a size boundary regardless of what's there. That's fine for plain prose, but an image's caption, a table, or a code block is a single indivisible unit -- cutting it in half produces two useless fragments instead of one usable one.

### The task

Write `chunk_with_atomic_blocks(blocks, max_chunk_size)`, where each block is `(content, size)` and is never split. Greedily pack blocks into chunks at or under `max_chunk_size`. A block whose own size already exceeds the limit still becomes its own chunk, since it genuinely can't be made smaller.

## Theory

### The simple version

Walk the blocks in order, adding each one to the current chunk as long as it still fits; the moment adding the next block would overflow, close the current chunk and start a new one with that block. A block never gets cut -- it either fits in the current chunk, or it starts the next one.

### Why oversized blocks aren't dropped or force-split

Discarding an oversized caption or table loses information the system was supposed to index; splitting it anyway defeats the entire reason atomicity was required in the first place. Letting it stand alone as its own (oversized) chunk is the only option that doesn't violate either constraint -- it's a known, visible trade-off rather than a silent one.

### How this shows up in real systems

This is exactly why multimodal ingestion pipelines treat images, tables, and code blocks as chunking-unit boundaries rather than applying character-count chunking uniformly across an entire document -- fixed-size chunking works fine between these atomic units, but never inside one.

## Explanation

Blocks are packed greedily: a running chunk accumulates size until the next block would push it over the limit, at which point the chunk closes and a fresh one starts with that block. Because a block is only ever appended whole, an oversized block simply triggers a chunk boundary on both sides of it -- it opens its own chunk (since it couldn't fit in whatever came before) and, being over the limit by itself, nothing gets added after it either.
