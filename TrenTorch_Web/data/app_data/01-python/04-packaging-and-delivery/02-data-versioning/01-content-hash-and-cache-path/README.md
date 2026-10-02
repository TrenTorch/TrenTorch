---
name: python-content-hash-and-cache-path
title: Content Hashes and Cache Paths
tags: [python-packaging, data-versioning, hashing, content-addressing]
difficulty: Beginner
---

## Statement

Write `content_hash(chunks)` to hash data that arrives in pieces without loading it all into memory, and `cache_path(digest)` to turn a digest into the sharded path a content-addressed cache stores it under.

## Theory

Git tracks code well, but a 5 GB dataset does not belong in a Git repository. Data versioning tools such as [DVC](https://doc.dvc.org/user-guide/project-structure/dvc-files) solve this by storing a small text placeholder in Git (a `.dvc` file recording the data's hash and size) while the data itself lives in a **content-addressable cache**: the file's name *is* its hash. DVC currently uses MD5 for this; we use SHA-256, the same idea with a stronger hash.

Two properties make this powerful:

1. **Same content, same name.** Two copies of an identical file hash to the same key, so they are stored once.
2. **Content cannot change under a name.** If one byte changes, the hash changes, so you can never silently get a different dataset behind the same identifier.

Large files should be hashed **in chunks**. `hashlib` objects support this: create one, call `.update(chunk)` repeatedly, then read `.hexdigest()`. The result is identical to hashing the whole thing at once, so chunk size is purely a memory choice.

Content-addressed caches also **shard** by the first two hex characters, storing the digest `2cf24dba...` at `2c/f24dba...`, so no single directory ends up holding millions of entries.

## Explanation

`content_hash` uses one running `hashlib.sha256()` and feeds each chunk to `update`, so memory use is bounded by chunk size, not file size. It accepts any iterable of bytes, including generators, because it only iterates once. `cache_path` is a pure string split: the first two characters become the directory, the rest the file name.
