---
name: python-sets-assemble-analyze-events
title: 'Assemble: Analyze Unique Events Across Datasets'
tags: [python-sets, aggregation]
difficulty: Advanced
---

## Statement

Implement a single function that analyzes event IDs appearing across multiple datasets, combining set creation, mutation, membership testing, set operations, set comprehensions, and the decision to use lists and sets together when both order and uniqueness matter.

## Theory

This problem introduces no new concepts. It combines this module's topics into one data-processing task. The input contains several batches of event IDs — each batch is a list, so its original order and duplicate occurrences exist, but the analysis needs both sequence information and set-based information:

```text
List -> preserves input order and duplicate occurrences
Set  -> represents unique membership
```

A single structure can't represent both requirements at once, so the solution uses the appropriate structure for each result: a set to track membership while scanning, a list to preserve first-seen order, and set intersection/comprehension to derive the common/non-common groups.

## Explanation

`analyze_events` builds one real `set` per batch first (`set(batch)`, collapsing each batch's own internal duplicates), then intersects all of them together to get `common_ids` — this is the direct translation of "appears in every batch," and per-batch duplicates can never inflate or distort that intersection since each batch only contributes its distinct members once. `non_common_ids` is built with a set comprehension over the overall `seen` set, filtering out whatever ended up in `common_ids` — the spec's own required set-comprehension use, and a direct complement rather than a second pass over the batches. The single-batch case falls out of the same intersection loop with no special-casing: intersecting one set with nothing more than itself is just that set, so `common_ids` becomes the whole distinct batch and `non_common_ids` is empty automatically.
