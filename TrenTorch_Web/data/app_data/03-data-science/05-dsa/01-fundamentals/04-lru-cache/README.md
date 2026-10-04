---
name: dsa-lru-cache
title: 'LRU Cache (Least Recently Used)'
tags: [dsa]
difficulty: Intermediate
---

## Statement

Implement a fixed-capacity cache that evicts the least recently used item when full. Implement get(key) and put(key, value) both in O(1). Use a hash map + doubly-linked list.

## Theory

### LRU caches manage capacity via eviction policy

An LRU cache keeps frequently accessed items and evicts unused ones. Implementation uses:
- HashMap: O(1) key-to-node lookup
- Doubly-linked list: O(1) reordering (move accessed item to front)

`
Recent → [node1] ↔ [node2] ↔ [node3] → Least Recent
         (most accessed)              (evict next)
`

### Operations

- get(key): return value, move node to front (mark as recently used)
- put(key, value): update value, move to front; if new key and full, evict tail (least recent)

Both O(1) via HashMap + linked list.

### Why LRU matters

- CPU caches: keep recently accessed memory
- Web caches: serve popular pages quickly
- Database query caching: memoize recent results
- CDNs: cache frequently requested content

### Trade-offs

- LRU assumes temporal locality (recent = likely useful)
- Other policies: LFU (least frequently used), FIFO, random

## Explanation

The solution uses a HashMap<key, node> for O(1) access and a doubly-linked list ordered by recency. get() moves the node to front; put() inserts at front and evicts the tail if at capacity.
