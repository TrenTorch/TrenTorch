---
name: dsa-hashtable
title: 'Implement a Hash Table / HashMap'
tags: [dsa]
difficulty: Intermediate
---

## Statement

Build a key-value store that resolves collisions via chaining. Implement put(key, value), get(key), remove(key) with average O(1) time. Handle collisions by storing multiple entries in each bucket.

## Theory

### Hash tables map keys to values via hashing

A hash table uses a hash function to map keys to array indices. If two keys hash to the same index (collision), they're stored in a linked list (chaining).

`Example:
index 0: [('Alice', 25)]
index 1: [('Bob', 30), ('Bella', 28)]  <- collision, stored in chain
index 2: []`

### Hash function requirements

- Fast to compute O(1)
- Distribute keys evenly across buckets (minimize collisions)
- Deterministic (same key always hashes to same value)

### Collision resolution

- Chaining: store collisions in a linked list per bucket
- Open addressing: probe for next empty slot (linear probing, double hashing)

### Why hash tables matter

- Dictionaries/maps in all languages
- Caching: O(1) lookups
- Deduplication: check if value seen before
- Grouping: count word frequencies

### Load factor and resizing

As the table fills, collision rates increase. Resizing the array and rehashing keeps operations O(1) on average.

## Explanation

The solution uses an array of linked lists. put() computes hash(key) % capacity to find the bucket, then inserts/updates in that bucket's chain. get() and remove() follow the same path.
