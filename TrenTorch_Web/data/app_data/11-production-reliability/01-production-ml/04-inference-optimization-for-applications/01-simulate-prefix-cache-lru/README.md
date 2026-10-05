---
name: production-inference-simulate-prefix-cache-lru
title: Simulate an LRU-Evicted Prefix Cache
tags: [production-systems, inference-optimization]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Recomputing a prompt's shared prefix (a system prompt, a long set of instructions, the start of a multi-turn conversation) on every single request wastes compute that was already spent producing the exact same result moments earlier. Caching the computation for recently seen prefixes avoids that -- but the cache has finite room, so something has to give when it fills up.

### The task

Write `simulate_prefix_cache(capacity, requests)`, simulating a prefix cache holding at most `capacity` distinct prefixes with least-recently-used (LRU) eviction. For each request in order, return whether it was a hit (already cached) or a miss, and update recency accordingly.

## Theory

### The simple version

The cache tracks which prefixes it holds and, among them, which was used most recently. A hit just refreshes that recency. A miss adds the new prefix and, if the cache is already full, evicts whichever entry hasn't been touched in the longest time.

### Why LRU, specifically

LRU is a cheap, effective proxy for "likely to be needed again soon": a prefix used a moment ago (a system prompt shared by every request in a burst, say) is far more likely to be requested again shortly than one that hasn't been touched in a while. Other eviction policies exist, but LRU is the standard default because it needs no advance knowledge of future access patterns to make a reasonable call.

### How this shows up in real systems

Real inference servers maintain exactly this kind of cache for shared prompt prefixes (a technique often called prefix caching or KV-cache reuse) -- when many requests share a system prompt or few-shot examples, computing that shared portion once and reusing it across requests measurably cuts both latency and compute cost, as long as the cache is large enough to keep the hot prefixes resident.

## Explanation

An `OrderedDict` keyed by prefix doubles as both the membership set and the recency ordering: `move_to_end` on a hit marks that prefix as most-recently-used, and `popitem(last=False)` on a full cache removes whichever entry sits at the front -- the least-recently-used one -- before the new prefix is inserted at the end.
