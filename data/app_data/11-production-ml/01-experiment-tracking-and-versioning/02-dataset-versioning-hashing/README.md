---
name: production-ml-dataset-versioning-hashing
title: 'Dataset Versioning: Why "the Same CSV" Is Not Reproducible Without a Hash'
tags: [mlops]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-experiment-tracking` logged which hyperparameters and metrics produced a given model — but a training run also depends on WHICH DATA it saw, and "training_data_v3.csv" is a dangerously unreliable answer to "which data": the same filename can silently point to different bytes over time (re-exported, re-sorted, accidentally edited), and there's no way to tell just by looking at it. A content HASH is the only trustworthy answer to "is this really the same dataset?"

### From theory to code

Implement `compute_content_hash` (the real fingerprint of raw bytes), `hash_rows_naive` (which inherits a genuine, non-obvious flaw), `hash_rows_canonical` (which fixes it), and `datasets_are_identical`.

### Constraints

- `compute_content_hash(data_bytes)` returns a SHA-256 hex digest — identical bytes always produce an identical hash.
- `hash_rows_naive(rows)` hashes the rows' representation directly, in whatever order they're given — reordering the SAME rows produces a DIFFERENT hash.
- `hash_rows_canonical(rows)` sorts the rows before hashing, so reordering the same rows produces the SAME hash.
- `datasets_are_identical(hash_a, hash_b)` is a plain equality check.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

A hash function has no concept of "these rows mean the same thing in a different order" — it only ever sees the exact bytes it's given, so `hash_rows_naive` inherits whatever order the input list happens to be in, faithfully and unhelpfully.

</details>

<details>
<summary>Hint 2</summary>

`sorted(rows)` before hashing is the entire fix — as long as the rows are sortable (comparable to each other), this guarantees any two lists containing the exact same rows, in ANY order, produce identical input to the hash function.

</details>

## Theory

### The simple version

Imagine two people each photographing the exact same pile of 100 coins, but one arranges them left-to-right by year before photographing, while the other just snaps the pile as it fell — the two PHOTOGRAPHS look completely different pixel-for-pixel, even though the underlying pile of coins is identical. A naive content hash is exactly like comparing those raw photographs: it only "sees" the literal arrangement it was given. Sorting the coins by some fixed rule FIRST (canonicalizing), then photographing, is what actually lets you compare "is this the same pile of coins?" reliably.

### The formula

```text
compute_content_hash(bytes) = sha256(bytes).hexdigest()

hash_rows_naive(rows)     = compute_content_hash(repr(rows))              -- order-SENSITIVE
hash_rows_canonical(rows) = compute_content_hash(repr(sorted(rows)))      -- order-INDEPENDENT

datasets_are_identical(h1, h2) = (h1 == h2)
```

This is a real, non-obvious gotcha in dataset versioning practice: two exports of "the same underlying data" from a database can easily come back in a different row order (depending on query execution plans, parallelism, or an unspecified `ORDER BY`), and a naive hash would flag them as completely different datasets — even though nothing about the actual content changed.

### How PyTorch actually implements this

Context only, untested by your submission: real dataset-versioning tools (DVC, Git LFS content hashing, Hugging Face `datasets`' fingerprinting) grapple with exactly this class of problem — deciding what counts as "the same data" often requires canonicalizing before hashing (sorting rows, normalizing whitespace, fixing column order) specifically because raw byte-for-byte hashing is too strict for what practitioners actually mean by "the same dataset."

## Explanation

`compute_content_hash` is a direct SHA-256 hash of raw bytes — `tests.py` confirms it's deterministic (same bytes, same hash, every call) and sensitive to any genuine content change.

`hash_rows_naive` hashes the row list's representation as-is — `tests.py` confirms this genuinely differs when the SAME rows are reordered, demonstrating the real flaw this exercise is illustrating, not just asserting it exists.

`hash_rows_canonical` sorts first, and `tests.py`'s final oracle test directly contrasts the two: the same reordered dataset must produce a DIFFERENT naive hash but an IDENTICAL canonical hash, confirming canonicalization is doing genuine, order-independent work rather than being a no-op wrapper around the naive version — while a separate test confirms canonicalization still correctly detects data that's genuinely DIFFERENT (not just reordered).

`datasets_are_identical` is the trivial equality check that gives the whole exercise its payoff: once you have a reliable hash, "are these the same dataset?" becomes a one-line, unambiguous answer.
