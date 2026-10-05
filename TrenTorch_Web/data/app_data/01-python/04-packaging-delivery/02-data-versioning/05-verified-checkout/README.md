---
name: python-verified-checkout
title: Check Out a Dataset Version Safely
tags: [python-packaging, data-versioning, content-addressing, integrity]
difficulty: Advanced
---

## Statement

Write `checkout(manifest, store)`, which rebuilds the files of a dataset version from its manifest and a content-addressed store, refusing to return data that is missing or corrupt.

## Theory

This is the read side of data versioning, what `dvc checkout` does conceptually. A manifest says which hash belongs at each path. The store holds blobs by hash. Checking out means looking each hash up and writing the bytes back at their paths.

Because the store is content-addressed, two things can go wrong, and a safe checkout must detect both **loudly**, never silently produce a partial or wrong dataset:

1. **Missing blob**: the manifest references a hash the store does not have (for example it was never pushed). Raise `FileNotFoundError`.
2. **Corrupt blob**: the bytes stored under a key do not hash to that key (disk corruption, a truncated upload, tampering). Raise `ValueError`.

The second check is what separates a content-addressed system from a plain key-value store. The key is a built-in checksum, so verifying costs one hash and removes an entire class of "my model trained on a subtly different dataset" bugs. The same logic is why pip's hash-checking mode exists for packages.

## Explanation

Iterating in sorted path order means the first error reported is deterministic. The two failures are different exception types on purpose, so callers can react differently (re-fetch a missing blob versus alarm on a corrupt one). The integrity check recomputes the digest of the stored bytes and compares it to the key the manifest asked for, because trusting the store's own labelling would defeat the purpose. Files are only returned if every one passed, so a caller never sees a half-restored version.
