---
name: python-lists-assemble-inventory-cleanup
title: 'Assemble: In-Place Inventory Cleanup With Snapshots'
tags: [python-lists, mutation, sorting]
difficulty: Advanced
---

## Statement

Implement a single function that filters, sorts, and summarizes a nested list of inventory rows in place, while returning an independent snapshot of the original data.

## Theory

This problem introduces no new concepts. It combines this module's topics: indexing and slicing, in-place removal, sorting with keys and stability, deep copying, and comprehensions, along with the mutation-versus-reassignment rule.

The problem requires you to:

- Take a **deep copy** of the input before changing anything, so the snapshot is unaffected by later changes.
- Remove rows **in place** without the skip-after-removal bug and without repointing the caller's list.
- Order the rows using **two stable sort passes** and key functions written with `def`.
- Read the first few rows with a **slice** and build lists with **comprehensions**.
- Keep the caller's outer list and its row objects as the same objects they were.

No new theory is required beyond re-reading those topics.

## Explanation

`process_inventory` takes the deep copy _before_ touching `rows` at all, so nothing done afterward — filtering, sorting — can retroactively affect what `snapshot` already captured. Filtering uses the "collect what to keep, then replace via slice assignment" pattern (`rows[:] = kept`), keeping `rows` the same object while every surviving row is still its original object (never rebuilt), and the two sort passes run label first, then quantity with `reverse=True`, so stability from the first pass supplies the "ascending label among ties" behavior once the second pass reorders by quantity.
