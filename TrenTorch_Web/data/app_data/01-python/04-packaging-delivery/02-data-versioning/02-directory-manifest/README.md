---
name: python-directory-manifest
title: Build a Directory Manifest
tags: [python-packaging, data-versioning, hashing, manifest]
difficulty: Intermediate
---

## Statement

Write `build_manifest(files)`, which summarises a dataset directory as a per-file hash list plus one directory digest that changes if and only if the directory's content changes.

## Theory

A dataset is usually a **directory**, not one file, so versioning it needs one identifier for the whole tree. DVC's [`.dvc` files](https://doc.dvc.org/user-guide/project-structure/dvc-files) record, for a tracked directory, a hash for the whole directory plus its total `size` in bytes and `nfiles`, the file count.

The standard construction is a **manifest**: a list of `(path, file hash)` entries, itself hashed. For that directory hash to be trustworthy it must be **canonical**:

- Entries are **sorted by path**, so the same files listed in a different order (a dict, a filesystem walk) give the same digest.
- The text that is hashed is defined exactly (here, `path<TAB>sha256` lines joined by newlines), so two implementations agree.
- Renaming a file, editing a file, adding or removing one, all change the digest. Reordering does not.

This is the same idea Git uses for trees, and it is why you can tell two dataset versions apart by comparing a single short string.

## Explanation

Sorting by path is what makes the digest canonical; everything downstream (the entries list and the digest text) is derived from that single sorted order. Hashing a defined text form rather than, say, the repr of a dict avoids depending on interpreter details. The path is part of each line, so a rename changes the digest even when the bytes are identical. `size` is the sum of the real byte lengths, matching the meaning of DVC's `size` field.
