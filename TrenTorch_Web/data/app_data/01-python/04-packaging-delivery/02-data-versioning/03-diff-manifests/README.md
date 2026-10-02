---
name: python-diff-manifests
title: Diff Two Dataset Versions
tags: [python-packaging, data-versioning, manifest, diff]
difficulty: Beginner
---

## Statement

Write `diff_manifests(old, new)`, which compares two dataset versions (path to file hash) and reports what was added, removed and modified.

## Theory

Once every dataset version is a manifest (a mapping from path to content hash), "what changed between v1 and v2?" becomes a cheap dictionary comparison, **without reading any file contents**. That is the whole point of hashing: equal hash means equal content, so you only need to compare short strings.

Three categories cover every difference:

- **added**: the path exists in the new version only
- **removed**: the path exists in the old version only
- **modified**: the path exists in both, but the hash differs

A path whose hash is unchanged appears in none of them. This is the logic behind `git status`, `dvc status` and `dvc diff`, and behind incremental uploads, where only the added and modified files need transferring.

## Explanation

Set operations on the key sets give added and removed directly. Modified is the intersection filtered by hash inequality. Returning sorted lists keeps results deterministic and easy to assert on. Note the function never touches file contents, only the hashes, which is what makes it fast on large datasets.
