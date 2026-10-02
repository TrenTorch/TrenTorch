---
name: python-content-addressed-store
title: A Deduplicating Content-Addressed Store
tags: [python-packaging, data-versioning, content-addressing, deduplication]
difficulty: Intermediate
---

## Statement

Write `store_put(store, data)` to save a blob under its own hash and `dedupe_stats(blobs)` to measure how much storage deduplication saved.

## Theory

In a [content-addressable cache](https://doc.dvc.org/user-guide/project-structure/dvc-files) like the one DVC keeps, a blob's **key is its hash**. That gives deduplication for free: saving the same bytes twice computes the same key twice, so the second save finds the entry already there and does nothing.

This is why versioning a dataset that changes by a few files per release stays cheap. Version 2 differs from version 1 in a handful of blobs, and every unchanged blob is already in the store, referenced by hash from the new manifest.

Two rules for `store_put`:

1. The key is the digest of the data (SHA-256 hex), computed by the store, never trusted from the caller.
2. If the key already exists, leave the stored value alone and just return the key.

`dedupe_stats` reports `total_bytes` (what you would store without dedup), `stored_bytes` (what is actually stored) and `unique` (distinct blobs).

## Explanation

The store is a plain dict from digest to bytes, which is all a content-addressed store fundamentally is. `setdefault` expresses "insert only if absent" in one call. `dedupe_stats` reuses `store_put` rather than re-implementing hashing, so the statistics and the real storing path cannot disagree.
